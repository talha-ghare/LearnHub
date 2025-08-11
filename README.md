# LearnHub - Django E-Learning Platform

LearnHub is a full-featured online learning platform built with Django. It provides a space for teachers to create courses and upload video content, and for students to browse, watch, rate, and engage with educational materials.


*(Replace the placeholder above with a real screenshot of your application)*

## About The Project

This project is a comprehensive web application designed to simulate a modern e-learning environment like Udemy or Coursera. It features distinct user roles, content management capabilities, and interactive elements to create an engaging user experience.

### Key Features

*   **Dual User Roles:** A robust authentication system that distinguishes between **Students** and **Teachers**, providing different permissions and dashboard views for each.
*   **Course Management:** Teachers can create, update, and manage their courses, including titles, descriptions, and thumbnails.
*   **Video Content:** Teachers can upload videos to their courses. The system is designed to handle video files, thumbnails, and ordering.
*   **Topic Organization:** Courses are categorized by topics, allowing for easy browsing and filtering.
*   **Student Dashboard:** Students get a personalized dashboard showing their bookmarked videos and recently added courses.
*   **Teacher Dashboard:** Teachers have a dedicated dashboard to view their created courses and total video count.
*   **Interactive Video Player Page:**
    *   **Commenting System:** Users can post comments on video pages.
    *   **Bookmarking:** Students can bookmark videos for later viewing.
*   **Rating and Reviews:** Students can give a star rating to courses they have viewed.
*   **Search Functionality:** Users can search for courses by title, description, topic, or teacher.

### Built With

This project is built with a modern Python and Django stack.

*   **Backend:**
    *   [Django](https://www.djangoproject.com/)
    *   [Django REST Framework](https://www.django-rest-framework.org/)
*   **Frontend:**
    *   Django Templates
    *   [Tailwind CSS](https://tailwindcss.com/)
    *   [Crispy Forms](https://django-crispy-forms.readthedocs.io/) & Crispy-Tailwind
*   **Database:**
    *   SQLite (for development)
*   **Image Handling:**
    *   [Pillow](https://python-pillow.org/)

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

You need to have Python and Pip installed on your machine.

*   Python 3.8+
*   Pip package manager

### Installation

1.  **Clone the repository**
    ```sh
    git clone https://github.com/your_username/learnhub.git
    cd learnhub
    ```
2.  **Create and activate a virtual environment**
    *   On macOS/Linux:
        ```sh
        python3 -m venv venv
        source venv/bin/activate
        ```
    *   On Windows:
        ```sh
        python -m venv venv
        .\venv\Scripts\activate
        ```
3.  **Install the required packages**
    ```sh
    pip install -r requirements.txt
    ```
4.  **Apply database migrations**
    ```sh
    python manage.py migrate
    ```
5.  **Create a superuser to access the admin panel**
    ```sh
    python manage.py createsuperuser
    ```
6.  **Run the development server**
    ```sh
    python manage.py runserver
    ```
7.  Open your browser and navigate to `http://127.0.0.1:8000/`.

## Usage

*   Visit the homepage to see an overview of the platform.
*   Register as a **"Teacher"** to gain access to the teacher dashboard and the ability to create courses and upload videos.
*   Register as a **"Student"** to browse courses, watch videos, and use features like bookmarking and commenting.
*   Access the Django admin panel at `/admin/` to manage all data directly.

## Roadmap

Here are some potential features for future development:

*   [ ] Implement a full student enrollment system.
*   [ ] Track and display video watching progress for students (`VideoProgress` model is already created).
*   [ ] Create quizzes and assignments for courses.
*   [ ] Add payment gateway integration for premium courses.
*   [ ] Develop API endpoints using the installed Django REST Framework.

See the [open issues](https://github.com/your_username/learnhub/issues) for a full list of proposed features (and known issues).

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

## Contact

Your Name - [@your_twitter](https://twitter.com/your_twitter) - email@example.com

Project Link: [https://github.com/your_username/learnhub](https://github.com/your_username/learnhub)

***

**Remember to replace the placeholder information** (like the screenshot URL, your username, contact details, etc.) with your own. This README provides a very solid foundation for your project's documentation

[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/91034166/00b17a66-1595-4427-8d26-0a3b6eb49c82/learnhub_complete_code.txt
