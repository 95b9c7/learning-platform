from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    UserProfile, Category, Course, Module, Lesson, 
    Enrollment, LessonProgress, Quiz, QuizQuestion, 
    QuizOption, QuizAttempt
)


class UserSerializer(serializers.ModelSerializer):
    """User serializer for API responses"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    """User profile serializer with user data"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'user_type', 'profile_picture', 'bio', 
                 'phone_number', 'date_of_birth', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CategorySerializer(serializers.ModelSerializer):
    """Category serializer"""
    course_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'slug', 'course_count', 'created_at']
        read_only_fields = ['id', 'course_count', 'created_at']
    
    def get_course_count(self, obj):
        return obj.course_set.count()


class CourseListSerializer(serializers.ModelSerializer):
    """Course serializer for list views (lightweight)"""
    instructor_name = serializers.CharField(source='instructor.get_full_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    total_modules = serializers.ReadOnlyField()
    total_lessons = serializers.ReadOnlyField()
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'short_description', 'instructor_name', 
                 'category_name', 'thumbnail', 'difficulty', 'duration_hours', 
                 'price', 'status', 'is_featured', 'total_modules', 'total_lessons', 
                 'created_at']
        read_only_fields = ['id', 'total_modules', 'total_lessons', 'created_at']


class CourseDetailSerializer(serializers.ModelSerializer):
    """Course serializer for detail views (full data)"""
    instructor = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    modules = serializers.SerializerMethodField()
    enrollment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'description', 'short_description', 
                 'instructor', 'category', 'thumbnail', 'difficulty', 'duration_hours', 
                 'price', 'status', 'is_featured', 'meta_description', 'tags', 
                 'modules', 'enrollment_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_modules(self, obj):
        modules = obj.modules.all()
        return ModuleSerializer(modules, many=True, context=self.context).data
    
    def get_enrollment_count(self, obj):
        return obj.enrollments.count()


class ModuleSerializer(serializers.ModelSerializer):
    """Module serializer"""
    lessons = serializers.SerializerMethodField()
    
    class Meta:
        model = Module
        fields = ['id', 'title', 'description', 'order', 'lessons', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_lessons(self, obj):
        lessons = obj.lessons.all()
        return LessonSerializer(lessons, many=True, context=self.context).data


class LessonSerializer(serializers.ModelSerializer):
    """Lesson serializer"""
    quiz = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()
    
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'content_type', 'content', 
                 'video_url', 'duration_minutes', 'order', 'is_free', 
                 'quiz', 'progress', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_quiz(self, obj):
        if hasattr(obj, 'quiz'):
            return QuizSerializer(obj.quiz, context=self.context).data
        return None
    
    def get_progress(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                progress = obj.progress.get(student=request.user)
                return LessonProgressSerializer(progress).data
            except LessonProgress.DoesNotExist:
                return None
        return None


class EnrollmentSerializer(serializers.ModelSerializer):
    """Enrollment serializer"""
    student = UserSerializer(read_only=True)
    course = CourseListSerializer(read_only=True)
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrolled_at', 'completed_at', 
                 'is_completed', 'progress_percentage']
        read_only_fields = ['id', 'enrolled_at']
    
    def get_progress_percentage(self, obj):
        if obj.is_completed:
            return 100
        
        course = obj.course
        total_lessons = course.total_lessons
        if total_lessons == 0:
            return 0
        
        completed_lessons = LessonProgress.objects.filter(
            student=obj.student,
            lesson__module__course=course,
            is_completed=True
        ).count()
        
        return round((completed_lessons / total_lessons) * 100, 2)


class LessonProgressSerializer(serializers.ModelSerializer):
    """Lesson progress serializer"""
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)
    lesson_order = serializers.IntegerField(source='lesson.order', read_only=True)
    
    class Meta:
        model = LessonProgress
        fields = ['id', 'lesson', 'lesson_title', 'lesson_order', 'completed_at', 
                 'is_completed', 'time_spent_minutes', 'last_accessed']
        read_only_fields = ['id', 'last_accessed']


class QuizOptionSerializer(serializers.ModelSerializer):
    """Quiz option serializer"""
    class Meta:
        model = QuizOption
        fields = ['id', 'option_text', 'is_correct', 'order']


class QuizQuestionSerializer(serializers.ModelSerializer):
    """Quiz question serializer"""
    options = QuizOptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = QuizQuestion
        fields = ['id', 'question_text', 'question_type', 'points', 'order', 'options']


class QuizSerializer(serializers.ModelSerializer):
    """Quiz serializer"""
    questions = QuizQuestionSerializer(many=True, read_only=True)
    questions_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'time_limit_minutes', 
                 'passing_score', 'max_attempts', 'questions', 'questions_count', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_questions_count(self, obj):
        return obj.questions.count()


class QuizAttemptSerializer(serializers.ModelSerializer):
    """Quiz attempt serializer"""
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    quiz_title = serializers.CharField(source='quiz.title', read_only=True)
    
    class Meta:
        model = QuizAttempt
        fields = ['id', 'student', 'student_name', 'quiz', 'quiz_title', 
                 'started_at', 'completed_at', 'score', 'passed']
        read_only_fields = ['id', 'started_at']


# Serializers for creating/updating objects
class CourseCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating courses"""
    class Meta:
        model = Course
        fields = ['title', 'slug', 'description', 'short_description', 
                 'category', 'thumbnail', 'difficulty', 'duration_hours', 
                 'price', 'status', 'is_featured', 'meta_description', 'tags']
    
    def create(self, validated_data):
        validated_data['instructor'] = self.context['request'].user
        return super().create(validated_data)


class LessonCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating lessons"""
    class Meta:
        model = Lesson
        fields = ['title', 'description', 'content_type', 'content', 
                 'video_url', 'duration_minutes', 'order', 'is_free']


class QuizCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating quizzes"""
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'time_limit_minutes', 
                 'passing_score', 'max_attempts']


class QuizQuestionCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating quiz questions"""
    options = QuizOptionSerializer(many=True)
    
    class Meta:
        model = QuizQuestion
        fields = ['question_text', 'question_type', 'points', 'order', 'options']
    
    def create(self, validated_data):
        options_data = validated_data.pop('options')
        question = QuizQuestion.objects.create(**validated_data)
        
        for option_data in options_data:
            QuizOption.objects.create(question=question, **option_data)
        
        return question
    
    def update(self, instance, validated_data):
        options_data = validated_data.pop('options')
        
        # Update question fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update options
        instance.options.all().delete()
        for option_data in options_data:
            QuizOption.objects.create(question=instance, **option_data)
        
        return instance
