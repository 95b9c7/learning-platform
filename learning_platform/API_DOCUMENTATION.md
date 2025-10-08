# Learning Platform API Documentation

## 🚀 **API Endpoints Overview**

Your learning platform now has a comprehensive REST API with the following endpoints:

### **Base URL**: `/api/`

---

## 📚 **Course Management**

### **Courses**
- `GET /api/courses/` - List all courses
- `GET /api/courses/{slug}/` - Get course details
- `POST /api/courses/` - Create new course (authenticated)
- `PUT /api/courses/{slug}/` - Update course (instructor only)
- `DELETE /api/courses/{slug}/` - Delete course (instructor only)

**Query Parameters:**
- `?category=slug` - Filter by category
- `?difficulty=beginner|intermediate|advanced` - Filter by difficulty
- `?featured=true` - Show only featured courses
- `?search=term` - Search in title, description, tags

**Custom Actions:**
- `POST /api/courses/{slug}/enroll/` - Enroll in course
- `GET /api/courses/{slug}/modules/` - Get course modules
- `GET /api/courses/{slug}/progress/` - Get user's progress

### **Categories**
- `GET /api/categories/` - List all categories
- `GET /api/categories/{slug}/` - Get category details
- `GET /api/categories/{slug}/courses/` - Get courses in category

### **Modules**
- `GET /api/modules/` - List all modules
- `GET /api/modules/{id}/` - Get module details

### **Lessons**
- `GET /api/lessons/` - List all lessons
- `GET /api/lessons/{id}/` - Get lesson details
- `POST /api/lessons/` - Create lesson (authenticated)
- `PUT /api/lessons/{id}/` - Update lesson (authenticated)
- `DELETE /api/lessons/{id}/` - Delete lesson (authenticated)

**Custom Actions:**
- `POST /api/lessons/{id}/complete/` - Mark lesson as completed
- `POST /api/lessons/{id}/track_time/` - Track time spent

---

## 👥 **User Management**

### **User Profiles**
- `GET /api/profiles/` - List user profiles (authenticated)
- `GET /api/profiles/{id}/` - Get profile details
- `POST /api/profiles/` - Create profile (authenticated)
- `PUT /api/profiles/{id}/` - Update profile (own profile only)
- `DELETE /api/profiles/{id}/` - Delete profile (own profile only)

### **Enrollments**
- `GET /api/enrollments/` - List user's enrollments (authenticated)
- `GET /api/enrollments/{id}/` - Get enrollment details

---

## 🧠 **Assessment System**

### **Quizzes**
- `GET /api/quizzes/` - List all quizzes
- `GET /api/quizzes/{id}/` - Get quiz details
- `POST /api/quizzes/` - Create quiz (authenticated)
- `PUT /api/quizzes/{id}/` - Update quiz (authenticated)
- `DELETE /api/quizzes/{id}/` - Delete quiz (authenticated)

**Custom Actions:**
- `POST /api/quizzes/{id}/submit/` - Submit quiz attempt

### **Quiz Attempts**
- `GET /api/quiz-attempts/` - List user's quiz attempts (authenticated)
- `GET /api/quiz-attempts/{id}/` - Get attempt details

---

## 🔐 **Authentication**

### **Token Authentication**
- Use Django REST Framework token authentication
- Include token in header: `Authorization: Token <your_token>`

### **Session Authentication**
- Use Django's built-in session authentication for web interfaces

---

## 📊 **API Features**

### **Pagination**
- All list endpoints are paginated (20 items per page)
- Use `?page=2` to get next page

### **Filtering & Search**
- Course filtering by category, difficulty, featured status
- Search functionality across course titles, descriptions, and tags

### **File Upload**
- Support for image uploads (profile pictures, course thumbnails)
- Use `multipart/form-data` for file uploads

### **Progress Tracking**
- Automatic progress calculation
- Time tracking for lessons
- Quiz scoring and attempts

---

## 🎯 **Example API Calls**

### **Get All Courses**
```bash
GET /api/courses/
```

### **Search Courses**
```bash
GET /api/courses/?search=python&difficulty=beginner
```

### **Enroll in Course**
```bash
POST /api/courses/python-basics/enroll/
Authorization: Token <your_token>
```

### **Complete Lesson**
```bash
POST /api/lessons/123/complete/
Authorization: Token <your_token>
```

### **Submit Quiz**
```bash
POST /api/quizzes/456/submit/
Authorization: Token <your_token>
Content-Type: application/json

{
    "answers": [
        {
            "question_id": 1,
            "option_id": 3
        },
        {
            "question_id": 2,
            "option_id": 5
        }
    ]
}
```

---

## 🔧 **Development Features**

### **Admin Interface**
- Access at `/admin/` for content management
- Full CRUD operations for all models
- Rich admin interface with inline editing

### **Media Files**
- Course thumbnails: `/media/course_thumbnails/`
- Profile pictures: `/media/profile_pictures/`
- Static files: `/static/`

### **CORS Configuration**
- CORS enabled for cross-origin requests
- Configurable via environment variables

---

## 🚀 **Next Steps**

1. **Database Setup** - Create PostgreSQL database and run migrations
2. **Create Superuser** - Set up admin access
3. **Test API Endpoints** - Use tools like Postman or curl
4. **Frontend Development** - Build React/Vue.js frontend
5. **Authentication UI** - Create login/register forms
6. **Payment Integration** - Connect Stripe for course purchases

---

## 📝 **API Response Examples**

### **Course List Response**
```json
{
    "count": 25,
    "next": "http://localhost:8000/api/courses/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Python Basics",
            "slug": "python-basics",
            "short_description": "Learn Python from scratch",
            "instructor_name": "John Doe",
            "category_name": "Programming",
            "difficulty": "beginner",
            "price": "99.00",
            "total_modules": 5,
            "total_lessons": 25
        }
    ]
}
```

### **Course Detail Response**
```json
{
    "id": 1,
    "title": "Python Basics",
    "description": "Complete Python course...",
    "instructor": {
        "id": 1,
        "username": "johndoe",
        "first_name": "John",
        "last_name": "Doe"
    },
    "modules": [
        {
            "id": 1,
            "title": "Introduction",
            "lessons": [
                {
                    "id": 1,
                    "title": "What is Python?",
                    "content_type": "video",
                    "duration_minutes": 15
                }
            ]
        }
    ]
}
```

Your learning platform API is now fully functional and ready for frontend development! 🎉
