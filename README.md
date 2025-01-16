# Flask Strategy Management API

## Overview
This is a Flask-based REST API that allows users to manage trading strategies. The API provides functionality for creating, retrieving, updating, and deleting strategies, as well as simulating their performance with user-provided data.

The project incorporates caching, user authentication, and RabbitMQ messaging to ensure efficient and robust operations.

---

## Features
1. **Authentication**: JWT-based authentication for secure access.
2. **Strategy Management**:
   - Create, retrieve, update, and delete trading strategies.
   - Associate strategies with specific users.
3. **Caching**:
   - Strategies are cached for performance optimization.
   - Cache invalidation is implemented after updates or deletions.
4. **RabbitMQ Messaging**:
   - Notify about strategy changes via RabbitMQ.
5. **Simulation**:
   - Simulate strategy performance with user-provided data.
6. **Database Integration**:
   - SQLAlchemy is used for ORM to manage database interactions.

---

## Prerequisites
Ensure the following are installed:

- Python 3.12+
- Docker and Docker Compose
- RabbitMQ
- Redis
- PostgreSQL

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Set Up Environment Variables**:
   Create a `.env` file in the project root with the following variables or download from the [Google Drive](https://drive.google.com/file/d/1ymIqvPUWKuIvuLItEIkMideL1rjEeAz6/view?usp=sharing):
   ```env
   SECRET_KEY=your_secret_key
   JWT_SECRET_KEY=your_jwt_secret_key
   DATABASE_URI=postgresql://user:111@db/stock_db
   FLASK_APP=your_flask_app
   ```

3. **Build and Run Docker Containers**:
   ```bash
   docker-compose up --build
   ```

4. **Access the Application**:
   - API: `http://localhost:5000`
   - RabbitMQ Management Interface: `http://localhost:15672`

---

## API Endpoints

### **Authentication**
- `POST /login/`: Authenticate a user and obtain a JWT.
- `POST /register/`: Register a new user.
- `POST /refresh/`: Get new access token based on refresh token.

### **Strategy Management**
- `GET /strategies/`: Retrieve all strategies for the authenticated user.
- `POST /strategies/`: Create a new strategy.
- `GET /strategies/<pk>/`: Retrieve details of a specific strategy.
- `PATCH /strategies/<pk>/`: Update a specific strategy.
- `DELETE /strategies/<pk>/`: Delete a specific strategy.

### **Simulation**
- `POST /strategies/<pk>/simulate/`: Simulate the performance of a strategy with user-provided data.

