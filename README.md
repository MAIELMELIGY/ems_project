# Employee Management System (EMS)

This project is a full-stack Employee Management System built with a Django REST API and a Vue 3 TypeScript frontend.

## Project Structure

* **backend_django/**: Django application handling the API, database models, and authentication.
* **frontend/**: Vue 3 application built with Vite, TypeScript, and Pinia.

---

## Backend Setup (Django)

The backend manages core entities such as Employees, Organizations, and Users.

### Prerequisites
* Python 3.x
* `pip` (Python package manager)

### Installation & Running
1.  **Navigate to the backend directory**:
    ```bash
    cd backend_django
    ```
2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *Key packages include Django 6.0.1, djangorestframework, and djangorestframework_simplejwt.*
4.  **Run migrations**:
    ```bash
    python manage.py migrate
    ```
5.  **Start the server**:
    ```bash
    python manage.py runserver
    ```
    The API will be available at `http://127.0.0.1:8000/`.

---

## Frontend Setup (Vue.js)

The frontend is a modern Single Page Application (SPA) using the Composition API (`<script setup>`).

### Prerequisites
* Node.js (Latest LTS)
* npm

### Installation & Running
1.  **Navigate to the frontend directory**:
    ```bash
    cd frontend
    ```
2.  **Install dependencies**:
    ```bash
    npm install
    ```
    *Dependencies include axios, pinia, and vue-router.*
3.  **Start the development server**:
    ```bash
    npm run dev
    ```
    The application will be available at `http://localhost:5173/`.
4.  **Build for production**:
    ```bash
    npm run build
    ```

---

## Tech Stack & Features

* **Backend**: Django 6.0, Django REST Framework, JWT Authentication (SimpleJWT), and API schema generation via `drf-spectacular`.
* **Frontend**: Vue 3.5, TypeScript, Vite, Pinia (State Management), and Axios (HTTP client).
* **Key Modules**: 
    * **Employees**: Management of staff records and details.
    * **Organizations**: Management of company and department structures.
    * **Users**: Custom user models and permission handling.