# Django Backend for Image File Manager

This is the backend service for the Image File Manager application, providing a RESTful API for managing user authentication, folders, and file storage. It is built using Django and Django REST Framework.

<strong>It is highly recommended to run the client side with this application.</strong>

## Features

- User authentication (Login, Signup, Logout, Token Refresh)

- Folder management (Create, List, Update, Delete)

- File management (Upload, Retrieve, Update, Delete)

- Token-based authentication for security

- API documentation available in the [client-side project](https://github.com/tjaung/image_manager_client).

## Project Structure

```
backend/
│── authentication/    # User authentication & JWT
│── files/             # Folder & File management
│── server/     # Main Django app configuration
│── requirements.txt   # Dependencies
│── manage.py          # Django management script
│── test.rest          # API test requests
│── README.md          # This file
```

## Installation & Setup

### 1️. Clone the Repository

```
git clone https://github.com/your-username/image-manager-backend.git
cd image_manager_django
```

### 2️. Create a Virtual Environment

```
# For Python 3
python3 -m venv env
source env/bin/activate  # On macOS/Linux
env\Scripts\activate     # On Windows
```

### 3️. Install Dependencies

```
pip install -r requirements.txt
```

### 4️. Run Database Migrations

```
python3 manage.py migrate
```

### 5️. Create a Superuser (Optional, for Admin Panel)

```
python3 manage.py createsuperuser
```

### 6️. Start the Server

```
python3 manage.py runserver  # or python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`. If it does not run at that port, run:

```
python3 manage.py runserver 127.0.0.1:8000 # this is the configuration for the client app
```

## Running Tests

Run all tests using:

```
python3 manage.py test
```

You can also test API requests using the provided `test.rest` file inside your VS Code REST Client or Postman.

## REST API

This Django backend provides a REST API that is documented **on the client-side project**. To learn more about available endpoints, request/response formats, and authentication methods, refer to the client-side documentation in the Documentation page inside of the app. Instructions on how to run the app are in the repo.

**Client-Side Repository**: [Vue.js Frontend](https://github.com/tjaung/image_manager_client)

## Running the Full Application

This backend is required to run the **Vue.js client-side** of the application. Ensure that this backend is running before starting the client.

Once the backend is up, start the Vue.js frontend with:

```
cd image-manager-client/client
npm run serve
```

## Troubleshooting

- If migrations fail, run `python3 manage.py makemigrations` before `migrate`

- If a dependency issue occurs, ensure your virtual environment is activated

- If running on Windows and `source env/bin/activate` doesn't work, try `env\Scripts\activate`

- Use `python manage.py shell` for debugging and testing API calls interactively

---
