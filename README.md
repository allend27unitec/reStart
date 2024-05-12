# FastAPI Project with Authentication

This is a sample FastAPI project demonstrating user authentication using FastAPI-Users. Borrowed heavily from https://thedmitry.pw/blog/2023/08/fastapi-async-sqlalchemy-pytest-and-alembic/
as a way to learn more quickly and easily. Here's a brief overview of how you can bring together Pydantic, Alembic, pytest, SQLAlchemy, and other tools in a Python project:

Pydantic: Use Pydantic for data validation and serialization. Define Pydantic models to represent your application's data structures and ensure their integrity.

SQLAlchemy: Use SQLAlchemy for database interactions. Define SQLAlchemy ORM models to represent your database tables and relationships. Use Alembic for database migrations to manage changes to your database schema over time.

Alembic: Use Alembic to generate and manage database migrations based on changes to your SQLAlchemy models. Alembic can help automate the process of creating and applying database schema changes as your application evolves.

pytest: Use pytest for testing your application. Write test cases to ensure the correctness and reliability of your codebase. pytest provides a powerful and flexible framework for writing and running tests in Python.

Pydantic-Settings: Use Pydantic-Settings for managing application settings and configuration. Define Pydantic models to represent your application's settings, and use Pydantic-Settings to load and validate configuration values from various sources (e.g., environment variables, configuration files).
 

## Getting Started

The standalone program authorize.py is a starting point that deals with some of the concepts and functionality present in this project.

The standalone programs [tutorial.py, tutorial_models.py] are part of the YouTube tutorial by AmigosCode, which is referenced in the documents/Week 1 Instructional Objectives.

### Prerequisites

- Python 3.7+
- MySQL database
- Postgres database

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/allend27unitec/reStart.git
   ```

2. Navigate to the project directory:

   ```bash
   cd reStart 
   ```

3. Install dependencies:

   ```bash
   pipenv update
   ```

4. Set up your MySQL database and update the connection URL in `main.py`:

   ```python
   SQLALCHEMY_DATABASE_URL = "mysql://user:password@localhost/db_name"
   ```

5. Run the FastAPI server:

   ```bash
   uvicorn main:app --reload
   ```

## Usage

1. Register a new user:
   - Send a `POST` request to `/users/register` with the following JSON payload:
     ```json
     {
       "email": "user@example.com",
       "password": "password",
       "username": "username"
     }
     ```

2. Login to obtain an access token:
   - Send a `POST` request to `/token` with the following JSON payload:
     ```json
     {
       "username": "username",
       "password": "password"
     }
     ```
   - The response will include an access token.

3. Access protected endpoints:
   - Include the access token in the `Authorization` header of your requests:
     ```bash
     curl -X GET "http://localhost:8000/users/me" -H "Authorization: Bearer <access_token>"
     ```

## API Endpoints

- `/users/register`: Register a new user.
- `/token`: Obtain an access token.
- `/users/me`: Access user profile information (protected endpoint).

## Dependencies

- FastAPI: Web framework for building APIs with Python.
- FastAPI-Users: Library for user authentication and management in FastAPI applications.
- SQLAlchemy: SQL toolkit and Object-Relational Mapping (ORM) library for Python.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

