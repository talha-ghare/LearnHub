# courses/management/commands/load_sample_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Topic, Course
from videos.models import Video, Comment, Bookmark
import random
from datetime import timedelta
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = 'Load sample data for LearnHub'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to load sample data...'))
        
        # Create sample data
        self.create_users()
        self.create_topics()
        self.create_courses()
        self.create_videos()
        self.create_interactions()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully loaded sample data!')
        )
    
    def create_users(self):
        self.stdout.write('Creating users...')
        
        # Teachers
        teachers_data = [
            {
                'username': 'john_teacher',
                'email': 'john@learnhub.com',
                'first_name': 'John',
                'last_name': 'Smith',
                'user_type': 'teacher',
                'bio': 'Web development expert with 10+ years experience'
            },
            {
                'username': 'sarah_dev',
                'email': 'sarah@learnhub.com',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'user_type': 'teacher',
                'bio': 'Data science and Python specialist'
            },
            {
                'username': 'mike_designer',
                'email': 'mike@learnhub.com',
                'first_name': 'Mike',
                'last_name': 'Chen',
                'user_type': 'teacher',
                'bio': 'UX/UI design and creative professional'
            },
            {
                'username': 'lisa_mobile',
                'email': 'lisa@learnhub.com',
                'first_name': 'Lisa',
                'last_name': 'Garcia',
                'user_type': 'teacher',
                'bio': 'Mobile app development and React Native expert'
            }
        ]
        
        # Students
        students_data = [
            {
                'username': 'alex_student',
                'email': 'alex@student.com',
                'first_name': 'Alex',
                'last_name': 'Wilson',
                'user_type': 'student'
            },
            {
                'username': 'emma_learner',
                'email': 'emma@student.com',
                'first_name': 'Emma',
                'last_name': 'Brown',
                'user_type': 'student'
            },
            {
                'username': 'david_coder',
                'email': 'david@student.com',
                'first_name': 'David',
                'last_name': 'Lee',
                'user_type': 'student'
            },
            {
                'username': 'sophia_designer',
                'email': 'sophia@student.com',
                'first_name': 'Sophia',
                'last_name': 'Taylor',
                'user_type': 'student'
            }
        ]
        
        for user_data in teachers_data + students_data:
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(
                    password='password123',
                    **user_data
                )
                self.stdout.write(f"Created user: {user.username}")
    
    def create_topics(self):
        self.stdout.write('Creating topics...')
        
        topics_data = [
            {
                'name': 'Web Development',
                'description': 'Frontend and backend web development technologies'
            },
            {
                'name': 'Data Science',
                'description': 'Data analysis, machine learning, and statistics'
            },
            {
                'name': 'Mobile Development',
                'description': 'iOS, Android, and cross-platform mobile app development'
            },
            {
                'name': 'Design',
                'description': 'UI/UX design, graphic design, and creative tools'
            },
            {
                'name': 'Programming Fundamentals',
                'description': 'Basic programming concepts and languages'
            },
            {
                'name': 'Cloud Computing',
                'description': 'AWS, Azure, Google Cloud, and DevOps'
            }
        ]
        
        for topic_data in topics_data:
            topic, created = Topic.objects.get_or_create(
                name=topic_data['name'],
                defaults=topic_data
            )
            if created:
                self.stdout.write(f"Created topic: {topic.name}")
    
    def create_courses(self):
        self.stdout.write('Creating courses...')
        
        courses_data = [
            {
                'title': 'Complete React.js Course for Beginners',
                'description': 'Learn React from scratch with hands-on projects. Build modern web applications using React hooks, components, and state management.',
                'teacher_username': 'john_teacher',
                'topic_name': 'Web Development'
            },
            {
                'title': 'Python Data Science Masterclass',
                'description': 'Master data science with Python. Learn pandas, numpy, matplotlib, and machine learning algorithms with real-world datasets.',
                'teacher_username': 'sarah_dev',
                'topic_name': 'Data Science'
            },
            {
                'title': 'React Native Mobile App Development',
                'description': 'Build cross-platform mobile apps with React Native. Create iOS and Android apps with a single codebase.',
                'teacher_username': 'lisa_mobile',
                'topic_name': 'Mobile Development'
            },
            {
                'title': 'UX/UI Design Fundamentals',
                'description': 'Learn user experience and interface design principles. Master Figma, design thinking, and user research.',
                'teacher_username': 'mike_designer',
                'topic_name': 'Design'
            },
            {
                'title': 'JavaScript ES6+ Modern Features',
                'description': 'Advanced JavaScript concepts including async/await, modules, destructuring, and modern ES6+ features.',
                'teacher_username': 'john_teacher',
                'topic_name': 'Programming Fundamentals'
            },
            {
                'title': 'AWS Cloud Practitioner Certification',
                'description': 'Comprehensive AWS cloud computing course covering EC2, S3, Lambda, and core AWS services.',
                'teacher_username': 'sarah_dev',
                'topic_name': 'Cloud Computing'
            },
            {
                'title': 'Full Stack Django Development',
                'description': 'Build complete web applications with Django. Learn models, views, templates, and deployment.',
                'teacher_username': 'john_teacher',
                'topic_name': 'Web Development'
            },
            {
                'title': 'Machine Learning with Python',
                'description': 'Practical machine learning course covering algorithms, scikit-learn, and real-world applications.',
                'teacher_username': 'sarah_dev',
                'topic_name': 'Data Science'
            }
        ]
        
        for course_data in courses_data:
            try:
                teacher = User.objects.get(username=course_data['teacher_username'])
                topic = Topic.objects.get(name=course_data['topic_name'])
                
                course, created = Course.objects.get_or_create(
                    title=course_data['title'],
                    defaults={
                        'description': course_data['description'],
                        'teacher': teacher,
                        'topic': topic
                    }
                )
                if created:
                    self.stdout.write(f"Created course: {course.title}")
            except (User.DoesNotExist, Topic.DoesNotExist) as e:
                self.stdout.write(f"Error creating course: {e}")
    
    def create_videos(self):
        self.stdout.write('Creating videos...')
        
        # Sample video data for each course
        videos_data = {
            'Complete React.js Course for Beginners': [
                'Introduction to React and Setup',
                'React Components and JSX',
                'State and Props Management',
                'Event Handling in React',
                'React Hooks - useState and useEffect',
                'Building a Todo App Project',
                'React Router for Navigation',
                'API Integration with Fetch'
            ],
            'Python Data Science Masterclass': [
                'Python Fundamentals for Data Science',
                'Introduction to Pandas DataFrames',
                'Data Cleaning and Preprocessing',
                'Data Visualization with Matplotlib',
                'Statistical Analysis Basics',
                'Machine Learning Introduction',
                'Linear Regression Project',
                'Model Evaluation and Metrics'
            ],
            'React Native Mobile App Development': [
                'React Native Setup and Environment',
                'Navigation in React Native',
                'Building Native Components',
                'State Management in Mobile Apps',
                'API Integration and Networking',
                'Camera and Media Features',
                'Publishing to App Stores',
                'Performance Optimization'
            ],
            'UX/UI Design Fundamentals': [
                'Design Thinking Process',
                'User Research Methods',
                'Wireframing and Prototyping',
                'Color Theory and Typography',
                'Figma Masterclass',
                'Mobile-First Design',
                'Usability Testing',
                'Design System Creation'
            ]
        }
        
        for course_title, video_titles in videos_data.items():
            try:
                course = Course.objects.get(title=course_title)
                for i, video_title in enumerate(video_titles):
                    video, created = Video.objects.get_or_create(
                        title=video_title,
                        course=course,
                        defaults={
                            'description': f"Learn {video_title.lower()} in this comprehensive lesson.",
                            'order': i + 1
                        }
                    )
                    if created:
                        self.stdout.write(f"Created video: {video.title}")
            except Course.DoesNotExist:
                continue
    
    def create_interactions(self):
        self.stdout.write('Creating interactions...')
        
        # Create bookmarks
        students = User.objects.filter(user_type='student')
        videos = Video.objects.all()
        
        if students.exists() and videos.exists():
            for student in students:
                # Each student bookmarks 3-7 random videos
                bookmark_count = random.randint(3, min(7, len(videos)))
                random_videos = random.sample(list(videos), bookmark_count)
                
                for video in random_videos:
                    Bookmark.objects.get_or_create(
                        user=student,
                        video=video
                    )
        
        # Create comments
        comment_templates = [
            "Great explanation! This helped me understand the concept much better.",
            "Could you provide more examples for this topic?",
            "Excellent tutorial! Very clear and easy to follow.",
            "This is exactly what I was looking for. Thank you!",
            "Can you make a follow-up video on advanced topics?",
            "Perfect pacing and great examples throughout.",
            "I've been struggling with this concept, but now it makes sense!",
            "Really appreciate the practical approach in this video."
        ]
        
        for video in videos:
            # Each video gets 1-4 random comments
            comment_count = random.randint(1, 4)
            for _ in range(comment_count):
                if students.exists():
                    student = random.choice(students)
                    comment_text = random.choice(comment_templates)
                    
                    Comment.objects.get_or_create(
                        user=student,
                        video=video,
                        content=comment_text,
                        defaults={
                            'created_at': timezone.now() - timedelta(
                                days=random.randint(1, 30)
                            )
                        }
                    )
        
        self.stdout.write("Created sample interactions (bookmarks and comments)")
