# FastAPI Project with Authentication

This is a sample FastAPI project demonstrating user authentication using FastAPI-Users.

## Getting Started

### Prerequisites

- Python 3.7+
- MySQL database

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/fastapi-authentication.git
   ```

2. Navigate to the project directory:

   ```bash
   cd fastapi-authentication
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
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
```

