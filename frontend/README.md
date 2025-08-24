# Denormies - A Fest Management System

This is a comprehensive full-stack application designed to manage college festivals and events. It handles all aspects of the event lifecycle, from user authentication and event registration to dynamic scheduling and administrative oversight.

This was a collaborative team project that I was a key part of, showcasing a robust architecture using modern web technologies.

## Key Features

* **User Authentication**: A secure and streamlined system for students, volunteers, and administrators to sign up and log in.
* **Dynamic Event Management**: Administrators can create, update, and manage all festival events through a dedicated interface. Participants can browse and register for events they are interested in.
* **Interactive Scheduling**: A live, day-by-day schedule of all events, allowing users to easily track activities and plan their attendance.
* **Role-Based Access Control**: Different user roles (participant, volunteer, admin) have specific permissions, ensuring data integrity and a tailored user experience.
* **Containerized Environment**: The entire application is containerized using Docker, ensuring consistency and simplifying the development and deployment process.

## Technical Architecture

The project is built on a modern, decoupled architecture to ensure scalability and maintainability.

### Frontend

The user interface is a responsive single-page application (SPA) built with **Next.js** and **React**.

* **Language**: **TypeScript**
* **Styling**: **Tailwind CSS** for a utility-first styling approach.
* **UI Components**: A custom component library ensures a consistent look and feel across the application.

### Backend

The backend is a powerful and efficient RESTful API built with **FastAPI**.

* **Language**: **Python**
* **Database**: **PostgreSQL** is used for robust and reliable data storage.
* **Asynchronous Operations**: FastAPI's asynchronous capabilities ensure that the application is fast and can handle many concurrent users.

### DevOps

The application is fully containerized for seamless deployment.

* **Containerization**: **Docker** and **Docker Compose** are used to create isolated and reproducible environments for both the frontend and backend services.