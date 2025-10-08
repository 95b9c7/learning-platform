from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import UserProfile, Category, Course, Module, Lesson, Quiz, QuizQuestion, QuizOption

class Command(BaseCommand):
    help = 'Populate database with sample safety training data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample safety training data...')
        
        # Create categories
        categories_data = [
            {'name': 'Equipment Safety', 'slug': 'equipment-safety', 'description': 'Training for operating various types of equipment safely'},
            {'name': 'Commercial Driving', 'slug': 'commercial-driving', 'description': 'Commercial driver training and certifications'},
            {'name': 'Workplace Safety', 'slug': 'workplace-safety', 'description': 'General workplace safety and OSHA compliance'},
            {'name': 'Heavy Equipment', 'slug': 'heavy-equipment', 'description': 'Training for heavy machinery and construction equipment'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories[cat_data['slug']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create instructor users
        instructors_data = [
            {'username': 'mike_rodriguez', 'first_name': 'Mike', 'last_name': 'Rodriguez', 'email': 'mike@example.com'},
            {'username': 'jennifer_walsh', 'first_name': 'Jennifer', 'last_name': 'Walsh', 'email': 'jennifer@example.com'},
            {'username': 'robert_chen', 'first_name': 'Robert', 'last_name': 'Chen', 'email': 'robert@example.com'},
            {'username': 'david_thompson', 'first_name': 'David', 'last_name': 'Thompson', 'email': 'david@example.com'},
        ]
        
        instructors = {}
        for inst_data in instructors_data:
            user, created = User.objects.get_or_create(
                username=inst_data['username'],
                defaults=inst_data
            )
            if created:
                user.set_password('password123')
                user.save()
            
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'user_type': 'instructor'}
            )
            instructors[inst_data['username']] = user
            if created:
                self.stdout.write(f'Created instructor: {user.get_full_name()}')
        
        # Create courses
        courses_data = [
            {
                'title': 'Forklift Operator Safety Training',
                'slug': 'forklift-operator-safety',
                'description': 'Complete OSHA-compliant forklift operation and safety training with hands-on assessments. Learn proper operation techniques, load handling, and safety protocols.',
                'short_description': 'OSHA-compliant forklift operation and safety training',
                'instructor': instructors['mike_rodriguez'],
                'category': categories['equipment-safety'],
                'difficulty': 'beginner',
                'duration_hours': 8,
                'price': 149.99,
                'status': 'published',
                'is_featured': True,
                'meta_description': 'Professional forklift operator safety training meeting OSHA standards',
                'tags': 'forklift, OSHA, equipment safety, certification'
            },
            {
                'title': 'CDL Hazmat Endorsement Training',
                'slug': 'cdl-hazmat-endorsement',
                'description': 'Department of Transportation hazmat certification for commercial drivers. Comprehensive training on handling and transporting hazardous materials safely.',
                'short_description': 'DOT hazmat certification for commercial drivers',
                'instructor': instructors['jennifer_walsh'],
                'category': categories['commercial-driving'],
                'difficulty': 'advanced',
                'duration_hours': 12,
                'price': 199.99,
                'status': 'published',
                'is_featured': True,
                'meta_description': 'DOT hazmat endorsement training for commercial drivers',
                'tags': 'CDL, hazmat, DOT, commercial driving, certification'
            },
            {
                'title': 'Confined Space Entry Safety',
                'slug': 'confined-space-entry-safety',
                'description': 'OSHA 1910.146 compliant training for confined space entry procedures and rescue operations. Essential for construction and industrial workers.',
                'short_description': 'OSHA compliant confined space entry procedures',
                'instructor': instructors['robert_chen'],
                'category': categories['workplace-safety'],
                'difficulty': 'intermediate',
                'duration_hours': 6,
                'price': 129.99,
                'status': 'published',
                'is_featured': False,
                'meta_description': 'OSHA confined space entry safety training',
                'tags': 'confined space, OSHA, workplace safety, rescue'
            },
            {
                'title': 'Crane Operation & Rigging Safety',
                'slug': 'crane-operation-rigging',
                'description': 'Professional crane operation training with load calculation and safety protocols. Learn proper rigging techniques and equipment inspection.',
                'short_description': 'Professional crane operation and rigging safety',
                'instructor': instructors['david_thompson'],
                'category': categories['heavy-equipment'],
                'difficulty': 'advanced',
                'duration_hours': 16,
                'price': 299.99,
                'status': 'published',
                'is_featured': True,
                'meta_description': 'Professional crane operation and rigging safety training',
                'tags': 'crane, rigging, heavy equipment, construction'
            }
        ]
        
        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                slug=course_data['slug'],
                defaults=course_data
            )
            if created:
                self.stdout.write(f'Created course: {course.title}')
                
                # Create modules for each course
                if course.slug == 'forklift-operator-safety':
                    modules_data = [
                        {'title': 'Introduction to Forklift Safety', 'description': 'Basic safety principles and regulations'},
                        {'title': 'Forklift Operations', 'description': 'Proper operation techniques and procedures'},
                        {'title': 'Load Handling', 'description': 'Safe load handling and transportation'},
                        {'title': 'Maintenance & Inspection', 'description': 'Daily inspection and maintenance procedures'},
                        {'title': 'Final Assessment', 'description': 'Comprehensive safety assessment'},
                    ]
                elif course.slug == 'cdl-hazmat-endorsement':
                    modules_data = [
                        {'title': 'Hazmat Regulations', 'description': 'DOT and federal hazmat regulations'},
                        {'title': 'Hazard Classes', 'description': 'Understanding different hazard classes'},
                        {'title': 'Packaging & Labeling', 'description': 'Proper packaging and labeling requirements'},
                        {'title': 'Emergency Procedures', 'description': 'Emergency response and incident reporting'},
                        {'title': 'Final Exam', 'description': 'DOT hazmat endorsement exam'},
                    ]
                elif course.slug == 'confined-space-entry-safety':
                    modules_data = [
                        {'title': 'Confined Space Identification', 'description': 'Identifying confined spaces and hazards'},
                        {'title': 'Entry Procedures', 'description': 'Safe entry procedures and permits'},
                        {'title': 'Atmospheric Testing', 'description': 'Air quality monitoring and testing'},
                        {'title': 'Rescue Operations', 'description': 'Emergency rescue procedures'},
                        {'title': 'Assessment', 'description': 'Final safety assessment'},
                    ]
                else:  # crane-operation-rigging
                    modules_data = [
                        {'title': 'Crane Types & Components', 'description': 'Understanding different crane types'},
                        {'title': 'Load Calculations', 'description': 'Load calculation and capacity limits'},
                        {'title': 'Rigging Fundamentals', 'description': 'Proper rigging techniques and equipment'},
                        {'title': 'Operation Procedures', 'description': 'Safe operation procedures and hand signals'},
                        {'title': 'Final Certification', 'description': 'Final certification assessment'},
                    ]
                
                for i, module_data in enumerate(modules_data):
                    module = Module.objects.create(
                        course=course,
                        title=module_data['title'],
                        description=module_data['description'],
                        order=i + 1
                    )
                    
                    # Create lessons for each module
                    lesson_data = [
                        {'title': f'{module_data["title"]} - Part 1', 'content_type': 'video', 'content': 'Introduction video content'},
                        {'title': f'{module_data["title"]} - Part 2', 'content_type': 'text', 'content': 'Detailed text content and procedures'},
                    ]
                    
                    for j, lesson_info in enumerate(lesson_data):
                        lesson = Lesson.objects.create(
                            module=module,
                            title=lesson_info['title'],
                            content_type=lesson_info['content_type'],
                            content=lesson_info['content'],
                            duration_minutes=30,
                            order=j + 1
                        )
                        
                        # Create a quiz for the final lesson of each module
                        if j == 1:  # Last lesson in module
                            quiz = Quiz.objects.create(
                                lesson=lesson,
                                title=f'{module.title} Quiz',
                                description=f'Assessment for {module.title}',
                                time_limit_minutes=15,
                                max_attempts=3,
                                passing_score=80
                            )
                            
                            # Create quiz questions
                            questions_data = [
                                {
                                    'question': 'What is the most important safety rule when operating equipment?',
                                    'question_type': 'multiple_choice',
                                    'options': [
                                        {'text': 'Speed', 'is_correct': False},
                                        {'text': 'Safety first', 'is_correct': True},
                                        {'text': 'Efficiency', 'is_correct': False},
                                        {'text': 'Cost', 'is_correct': False},
                                    ]
                                },
                                {
                                    'question': 'You should always inspect equipment before use.',
                                    'question_type': 'true_false',
                                    'correct_answer': True
                                }
                            ]
                            
                            for q_data in questions_data:
                                question = QuizQuestion.objects.create(
                                    quiz=quiz,
                                    question_text=q_data['question'],
                                    question_type=q_data['question_type'],
                                    order=len(quiz.questions.all()) + 1
                                )
                                
                                if q_data['question_type'] == 'multiple_choice':
                                    for opt_data in q_data['options']:
                                        QuizOption.objects.create(
                                            question=question,
                                            option_text=opt_data['text'],
                                            is_correct=opt_data['is_correct']
                                        )
                                elif q_data['question_type'] == 'true_false':
                                    QuizOption.objects.create(
                                        question=question,
                                        option_text='True',
                                        is_correct=q_data['correct_answer']
                                    )
                                    QuizOption.objects.create(
                                        question=question,
                                        option_text='False',
                                        is_correct=not q_data['correct_answer']
                                    )
        
        self.stdout.write(self.style.SUCCESS('Successfully populated database with sample safety training data!'))
        self.stdout.write('You can now access the Django admin at: http://127.0.0.1:8000/admin/')
        self.stdout.write('Username: admin, Password: [set via ADMIN_PASSWORD environment variable]')
