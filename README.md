# Booking API

This is a Django-based booking API that allows users to make reservations. It uses Django REST Framework to expose API endpoints and includes user authentication with Simple JWT.

## Project Idea

The core idea of this project is to provide a flexible and scalable booking system that can be adapted to various business needs. Whether it's for scheduling appointments, booking services, or reserving items, the system is designed to be customizable. The API-first approach allows for easy integration with different front-end applications, such as web or mobile clients.

Key features include:
-   **Dynamic Booking Types**: Create different types of bookings (e.g., "doctor's appointment," "consultation call," "equipment rental") with custom fields for each type.
-   **User-Centric Reservations**: Registered users can create, view, and manage their reservations.
-   **Admin Interface**: A comprehensive admin panel to manage booking types, reservations, and users.

## Project Structure

-   `booking`: The main Django project directory, containing the global settings and URL configurations.
-   `book`: This app is the heart of the booking system. It defines the `BookingType` model, which allows administrators to create different kinds of bookable items or services, and the `Booking` model, which represents a specific instance of a booking.
-   `reservations`: This app handles the user-facing reservation process. It connects a `User` with a `Booking`, creating a `Reservation`. It also manages the status and payment details of each reservation.
-   `users`: Manages user accounts, authentication, and profiles. It is built to support user registration, login, and token-based authentication for API access.
-   `requirements.txt`: A list of the project's Python dependencies.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8+
- pip
- Virtualenv (recommended)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/booking-api.git
    cd booking-api
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply the database migrations:**

    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser to access the admin panel:**

    ```bash
    python manage.py createsuperuser
    ```

### Running the Application

To run the development server, use the following command:

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000`.

## API Endpoints

The following are the main API endpoints available in this project:

-   **Admin Panel**: ` /admin`
-   **Reservations**: ` /api/reservations/`
-   **Users**: ` /api/users/`

For more details on the available endpoints and their usage, you can explore the browsable API at `http://127.0.0.1:8000/api/`. 