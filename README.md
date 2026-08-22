# File Tracking System (FTS)

**FTS** is a robust web application designed for seamless file movement and tracking between departments within an organization. It provides real-time status updates, secure file handling, and comprehensive dashboards for administrators and users.

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git (optional, for source control)

### Installation

1.  **Clone the repository (if using Git):**
    ```bash
    git clone <repository-url>
    cd ftsapp
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment:**
    -   **Windows:**
        ```bash
        venv\Scripts\activate
        ```
    -   **Linux/Mac:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Apply Migrations:**
    This sets up the database schema required for the application.
    ```bash
    python manage.py migrate
    ```

6.  **Create a Superuser (Admin):**
    You'll need an admin account to manage the system.
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to enter your admin credentials.

7.  **Run the Development Server:**
    ```bash
    python manage.py runserver
    ```

8.  **Access the Application:**
    Open your browser and navigate to:
    
    -   **User Portal:** `http://localhost:8000/`

## 📂 Project Structure

```
ftsapp/
├── userapp/            # User authentication and dashboard logic
├── adminapp/           # Admin management logic
├── fts_core/           # Core Django project settings and configuration
├── templates/          # Global HTML templates
├── static/             # CSS, JavaScript, and static assets
└── media/              # User-uploaded files and documents
```

## 🔐 Security & Credentials

### Environment Variables
For production environments, it is crucial to manage sensitive information using environment variables. Create a `.env` file in the root directory:

```env
SECRET_KEY=your_secret_key_here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database Configuration
DB_ENGINE=django.db.backends.postgresql
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=[IP_ADDRESS]
DB_PORT=5432

# Email Configuration (for password resets, notifications)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_password
DEFAULT_FROM_EMAIL=webmaster@yourdomain.com
```

**Note:** Never commit the `.env` file to version control (it is already listed in `.gitignore`).

## 🛠️ Development

### Running Migrations
Ensure your database schema is up to date with the following commands:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Creating a New User
To create a regular user (non-admin):
```bash
python manage.py createsuperuser
```
*(Follow the prompts for the desired user)*

### Static Files
If you make changes to CSS or JavaScript files, collect static files:
```bash
python manage.py collectstatic
```

## 👥 User Roles

### Standard Users
-   **Login:** Registered email and password.
-   **Dashboard:** View assigned files and tasks.
-   **File Management:** Upload, download, and track file status.

### Administrators
-   **Full Access:** Complete control over the system.
-   **Department Management:** Create and manage departments.
-   **File Tracking:** Monitor all file movements across the organization.

## 📝 Additional Features

-   **Real-time Status Tracking:** Monitor the progress of files in real-time.
-   **Secure File Handling:** All file uploads and downloads are securely managed through the Django backend.
-   **Responsive Design:** Optimized for both desktop and mobile devices.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1.  Create a feature branch (`git checkout -b feature/AmazingFeature`).
2.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
3.  Push to the branch (`git push origin feature/AmazingFeature`).
4.  Open a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For issues or questions, please open an issue on GitHub or contact the development team.
