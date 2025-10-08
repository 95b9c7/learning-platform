from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth import views as auth_views
from .views import (
    CategoryViewSet, CourseViewSet, ModuleViewSet, LessonViewSet,
    EnrollmentViewSet, QuizViewSet, QuizAttemptViewSet, UserProfileViewSet,
    RegisterView, LoginView
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'modules', ModuleViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')
router.register(r'quizzes', QuizViewSet)
router.register(r'quiz-attempts', QuizAttemptViewSet, basename='quizattempt')
router.register(r'profiles', UserProfileViewSet, basename='profile')

app_name = 'core'

urlpatterns = [
    path('api/', include(router.urls)),
    # Authentication endpoints
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/token/', obtain_auth_token, name='obtain_token'),
]
