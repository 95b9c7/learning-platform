from django.contrib import admin
from .models import (
    UserProfile, Category, Course, Module, Lesson, 
    Enrollment, LessonProgress, Quiz, QuizQuestion, 
    QuizOption, QuizAttempt
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'created_at']
    list_filter = ['user_type', 'created_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1
    ordering = ['order']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'category', 'difficulty', 'price', 'status', 'created_at']
    list_filter = ['status', 'difficulty', 'category', 'is_featured', 'created_at']
    search_fields = ['title', 'description', 'instructor__username']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'short_description', 'instructor')
        }),
        ('Course Details', {
            'fields': ('category', 'thumbnail', 'difficulty', 'duration_hours', 'price')
        }),
        ('Status & Settings', {
            'fields': ('status', 'is_featured')
        }),
        ('SEO', {
            'fields': ('meta_description', 'tags'),
            'classes': ('collapse',)
        }),
    )


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    ordering = ['order']


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'created_at']
    list_filter = ['course', 'created_at']
    search_fields = ['title', 'course__title']
    inlines = [LessonInline]
    ordering = ['course', 'order']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'content_type', 'duration_minutes', 'is_free', 'order']
    list_filter = ['content_type', 'is_free', 'module__course']
    search_fields = ['title', 'module__title', 'module__course__title']
    ordering = ['module', 'order']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrolled_at', 'is_completed']
    list_filter = ['is_completed', 'enrolled_at', 'course']
    search_fields = ['student__username', 'course__title']
    readonly_fields = ['enrolled_at']


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['student', 'lesson', 'is_completed', 'time_spent_minutes', 'last_accessed']
    list_filter = ['is_completed', 'last_accessed']
    search_fields = ['student__username', 'lesson__title']
    readonly_fields = ['last_accessed']


class QuizOptionInline(admin.TabularInline):
    model = QuizOption
    extra = 2
    ordering = ['order']


class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 1
    ordering = ['order']
    inlines = [QuizOptionInline]


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'time_limit_minutes', 'passing_score', 'max_attempts']
    list_filter = ['passing_score', 'max_attempts']
    search_fields = ['title', 'lesson__title']
    inlines = [QuizQuestionInline]


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'quiz', 'question_type', 'points', 'order']
    list_filter = ['question_type', 'quiz']
    search_fields = ['question_text', 'quiz__title']
    ordering = ['quiz', 'order']


@admin.register(QuizOption)
class QuizOptionAdmin(admin.ModelAdmin):
    list_display = ['option_text', 'question', 'is_correct', 'order']
    list_filter = ['is_correct', 'question__quiz']
    search_fields = ['option_text', 'question__question_text']


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['student', 'quiz', 'started_at', 'score', 'passed']
    list_filter = ['passed', 'started_at', 'quiz']
    search_fields = ['student__username', 'quiz__title']
    readonly_fields = ['started_at']
