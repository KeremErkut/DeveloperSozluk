# DeveloperSözlük

**DeveloperSözlük** is an interactive dictionary and discussion platform for developers, built with Django. Users can create topics related to software and technology, add entries to these topics, and exchange information with other developers.

![DeveloperSözlük Homepage](https://i.imgur.com/your-homepage-screenshot.png ) <!-- You can add a screenshot link here -->

## 🚀 Project Goal

This project aims to create a central platform where developers can discuss the problems they face, learn about new technologies, and share their experiences. It adapts the popular dictionary format specifically for the needs of the software development world.

## ✨ Features

*   **User Management:**
    *   User registration and secure login/logout processes.
    *   User profile page (showing the user's latest entries).
*   **Topic and Entry System:**
    *   Users can create new topics.
    *   Users can add new entries to existing topics.
    *   Users can edit or delete their own entries.
*   **Search Functionality:**
    *   Search for topics by keywords.
*   **Modern and Responsive Interface:**
    *   A user-friendly interface developed with Bootstrap 5, compatible with mobile and desktop devices.
    *   Enhanced with Font Awesome icons for a better user experience.
*   **Pagination:**
    *   Pagination support for topics on the homepage and entries under topics, improving performance and user experience.

## 🛠️ Technologies Used

*   **Backend:**
    *   **Python 3**
    *   **Django 5.2**: Web framework
    *   **SQLite**: Database for the development environment
*   **Frontend:**
    *   **HTML5 / CSS3**
    *   **Bootstrap 5**: CSS framework
    *   **Font Awesome**: Icon library
*   **Development Tools:**
    *   **Git & GitHub**: Version control

## 📦 Installation and Setup

You can follow the steps below to run the project on your local machine.

### 1. Clone the Project

```bash
git clone https://github.com/KeremErkut/DeveloperSozluk.git
cd DeveloperSozluk
```

### 2. Create and Activate a Virtual Environment

Creating a virtual environment allows you to isolate project dependencies from your system.

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Database Setup (Migrations )

Run the migration commands for Django to create the database schema.

```bash
python manage.py migrate
```

### 5. Create a Superuser

Create an administrator account to access the Django admin panel.

```bash
python manage.py createsuperuser
```
The command will prompt you for a username, email, and password.

### 6. Start the Development Server

Everything is ready! Start the development server.

```bash
python manage.py runserver
```

The project will run by default at `http://127.0.0.1:8000/`. You can access the admin panel at `http://127.0.0.1:8000/admin/`.

## 📂 Project Structure

```
DeveloperSozluk/
├── devsozluk/          # Django Project Configuration Directory
│   ├── settings.py     # Project settings
│   ├── urls.py         # Main URL routing
│   └── ...
├── main/               # Main Application Directory
│   ├── models.py       # Database models (Topic, Entry )
│   ├── views.py        # View functions (logic)
│   ├── urls.py         # App-specific URL routing
│   ├── forms.py        # Django forms
│   ├── admin.py        # Admin panel configuration
│   └── migrations/
├── templates/          # HTML templates
│   ├── base.html       # Base template
│   └── ...
├── manage.py           # Django command-line utility
└── requirements.txt    # Project dependencies
```

## 🚀 Future Plans and Improvements

*   [ ] **Entry Voting:** Allow users to upvote/downvote entries.
*   [ ] **Enhanced User Profile:** Add a profile picture, an "about me" section, and social media links.
*   [ ] **Unit Tests:** Write tests to increase the stability of the project.
*   [ ] **Asynchronous Operations (AJAX/Fetch):** Implement actions like voting without a page reload.
*   [ ] **`.env` Integration:** Manage sensitive information like `SECRET_KEY` with environment variables.
*   [ ] **Markdown Support:** Add Markdown support for rich text formatting in entries.

## 🤝 Contributing

This project is open for development. If you would like to contribute:
1.  Fork the project.
2.  Create a new feature branch (`feature/new-feature`) or a bugfix branch (`fix/bug-name`).
3.  Commit your changes.
4.  Push your branch to GitHub.
5.  Open a Pull Request (PR).

Thank you in advance for all your contributions!

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
