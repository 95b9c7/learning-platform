from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Q, Count, Avg
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import (
    UserProfile, Category, Course, Module, Lesson, 
    Enrollment, LessonProgress, Quiz, QuizQuestion, 
    QuizOption, QuizAttempt
)
from .serializers import (
    UserSerializer, UserProfileSerializer, CategorySerializer,
    CourseListSerializer, CourseDetailSerializer, ModuleSerializer,
    LessonSerializer, EnrollmentSerializer, LessonProgressSerializer,
    QuizSerializer, QuizAttemptSerializer, CourseCreateUpdateSerializer,
    LessonCreateUpdateSerializer, QuizCreateUpdateSerializer,
    QuizQuestionCreateUpdateSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for categories (read-only)"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    
    @action(detail=True, methods=['get'])
    def courses(self, request, slug=None):
        """Get all courses in a category"""
        category = self.get_object()
        courses = Course.objects.filter(category=category, status='published')
        serializer = CourseListSerializer(courses, many=True, context={'request': request})
        return Response(serializer.data)


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet for courses"""
    queryset = Course.objects.all()
    lookup_field = 'slug'
    parser_classes = [MultiPartParser, FormParser]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return CourseCreateUpdateSerializer
        return CourseDetailSerializer
    
    def get_queryset(self):
        queryset = Course.objects.select_related('instructor', 'category').prefetch_related('modules__lessons')
        
        # Filter by status for non-owners
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status='published')
        elif not self.request.user.is_staff:
            # Show published courses + user's own courses
            queryset = queryset.filter(
                Q(status='published') | Q(instructor=self.request.user)
            )
        
        # Apply filters
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        featured = self.request.query_params.get('featured')
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)
        
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search) |
                Q(tags__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)
    
    def perform_update(self, serializer):
        # Only allow instructors to update their own courses
        if serializer.instance.instructor != self.request.user and not self.request.user.is_staff:
            raise permissions.PermissionDenied("You can only edit your own courses.")
        serializer.save()
    
    @action(detail=True, methods=['post'])
    def enroll(self, request, slug=None):
        """Enroll in a course"""
        course = self.get_object()
        user = request.user
        
        if not user.is_authenticated:
            return Response({'error': 'Authentication required'}, 
                          status=status.HTTP_401_UNAUTHORIZED)
        
        if course.status != 'published':
            return Response({'error': 'Course is not available for enrollment'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        enrollment, created = Enrollment.objects.get_or_create(
            student=user,
            course=course,
            defaults={'enrolled_at': timezone.now()}
        )
        
        if created:
            serializer = EnrollmentSerializer(enrollment, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Already enrolled in this course'}, 
                          status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def modules(self, request, slug=None):
        """Get course modules with lessons"""
        course = self.get_object()
        modules = course.modules.all()
        serializer = ModuleSerializer(modules, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def progress(self, request, slug=None):
        """Get user's progress in the course"""
        course = self.get_object()
        user = request.user
        
        if not user.is_authenticated:
            return Response({'error': 'Authentication required'}, 
                          status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            enrollment = Enrollment.objects.get(student=user, course=course)
            serializer = EnrollmentSerializer(enrollment, context={'request': request})
            return Response(serializer.data)
        except Enrollment.DoesNotExist:
            return Response({'error': 'Not enrolled in this course'}, 
                          status=status.HTTP_404_NOT_FOUND)


class ModuleViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for modules (read-only)"""
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    
    def get_queryset(self):
        return Module.objects.select_related('course').prefetch_related('lessons')


class LessonViewSet(viewsets.ModelViewSet):
    """ViewSet for lessons"""
    queryset = Lesson.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return LessonCreateUpdateSerializer
        return LessonSerializer
    
    def get_queryset(self):
        return Lesson.objects.select_related('module__course').prefetch_related('quiz__questions__options')
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark lesson as completed"""
        lesson = self.get_object()
        user = request.user
        
        if not user.is_authenticated:
            return Response({'error': 'Authentication required'}, 
                          status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if user is enrolled in the course
        course = lesson.module.course
        try:
            enrollment = Enrollment.objects.get(student=user, course=course)
        except Enrollment.DoesNotExist:
            return Response({'error': 'Not enrolled in this course'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        # Update or create progress
        progress, created = LessonProgress.objects.get_or_create(
            student=user,
            lesson=lesson,
            defaults={'is_completed': True, 'completed_at': timezone.now()}
        )
        
        if not created:
            progress.is_completed = True
            progress.completed_at = timezone.now()
            progress.save()
        
        serializer = LessonProgressSerializer(progress)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def track_time(self, request, pk=None):
        """Track time spent on lesson"""
        lesson = self.get_object()
        user = request.user
        time_spent = request.data.get('time_spent_minutes', 0)
        
        if not user.is_authenticated:
            return Response({'error': 'Authentication required'}, 
                          status=status.HTTP_401_UNAUTHORIZED)
        
        progress, created = LessonProgress.objects.get_or_create(
            student=user,
            lesson=lesson,
            defaults={'time_spent_minutes': time_spent}
        )
        
        if not created:
            progress.time_spent_minutes += time_spent
            progress.save()
        
        serializer = LessonProgressSerializer(progress)
        return Response(serializer.data)


class EnrollmentViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for enrollments (read-only for students)"""
    serializer_class = EnrollmentSerializer
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Enrollment.objects.filter(student=self.request.user).select_related('course', 'student')
        return Enrollment.objects.none()


class QuizViewSet(viewsets.ModelViewSet):
    """ViewSet for quizzes"""
    queryset = Quiz.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return QuizCreateUpdateSerializer
        return QuizSerializer
    
    def get_queryset(self):
        return Quiz.objects.select_related('lesson').prefetch_related('questions__options')
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit quiz attempt"""
        quiz = self.get_object()
        user = request.user
        
        if not user.is_authenticated:
            return Response({'error': 'Authentication required'}, 
                          status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if user is enrolled in the course
        course = quiz.lesson.module.course
        try:
            enrollment = Enrollment.objects.get(student=user, course=course)
        except Enrollment.DoesNotExist:
            return Response({'error': 'Not enrolled in this course'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        # Check attempt limit
        attempts = QuizAttempt.objects.filter(student=user, quiz=quiz)
        if attempts.count() >= quiz.max_attempts:
            return Response({'error': 'Maximum attempts reached'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate score
        answers = request.data.get('answers', [])
        correct_answers = 0
        total_questions = quiz.questions.count()
        
        for answer in answers:
            question_id = answer.get('question_id')
            selected_option_id = answer.get('option_id')
            
            try:
                question = QuizQuestion.objects.get(id=question_id, quiz=quiz)
                if question.question_type == 'multiple_choice':
                    correct_option = question.options.filter(is_correct=True).first()
                    if correct_option and str(correct_option.id) == str(selected_option_id):
                        correct_answers += 1
                elif question.question_type == 'true_false':
                    # Handle true/false logic here
                    pass
            except QuizQuestion.DoesNotExist:
                continue
        
        score = round((correct_answers / total_questions) * 100) if total_questions > 0 else 0
        passed = score >= quiz.passing_score
        
        # Create attempt
        attempt = QuizAttempt.objects.create(
            student=user,
            quiz=quiz,
            score=score,
            passed=passed,
            completed_at=timezone.now()
        )
        
        serializer = QuizAttemptSerializer(attempt)
        return Response(serializer.data)


class QuizAttemptViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for quiz attempts (read-only for students)"""
    serializer_class = QuizAttemptSerializer
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return QuizAttempt.objects.filter(student=self.request.user).select_related('quiz', 'student')
        return QuizAttempt.objects.none()


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for user profiles"""
    serializer_class = UserProfileSerializer
    parser_classes = [MultiPartParser, FormParser]
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return UserProfile.objects.all()
            return UserProfile.objects.filter(user=self.request.user)
        return UserProfile.objects.none()
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        # Only allow users to update their own profile (unless staff)
        if serializer.instance.user != self.request.user and not self.request.user.is_staff:
            raise permissions.PermissionDenied("You can only edit your own profile.")
        serializer.save()


# Authentication Views
class LoginView(APIView):
    """Custom login view that accepts email and password"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response(
                {'error': 'Email and password are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Find user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Authenticate user
        user = authenticate(username=user.username, password=password)
        
        if user:
            # Create or get token
            token, created = Token.objects.get_or_create(user=user)
            
            # Get or create user profile
            profile, created = UserProfile.objects.get_or_create(user=user)
            
            return Response({
                'token': token.key,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            })
        else:
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )


class RegisterView(APIView):
    """User registration view"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        
        if not all([username, email, password]):
            return Response(
                {'error': 'Username, email, and password are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username already exists'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'Email already exists'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create token
        token = Token.objects.create(user=user)
        
        # Create user profile
        UserProfile.objects.create(user=user)
        
        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        }, status=status.HTTP_201_CREATED)


