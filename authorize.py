from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import (
    DeclarativeBase,
    Session,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
    scoped_session
)

from passlib.context import CryptContext
from jose import JWTError, jwt
from app.settings import settings

# Set up database connection
try:
    engine = settings.mysql_engine()
    print(f"MySql Connection successful")
except Exception as e:
    print(f"MySql Connection Exception {e}")

def create_session():
    try:
        engine = settings.postgresql_engine()
        session_factory = sessionmaker(bind=engine)
        print(f"Postgresql Connection successful")
        return scoped_session(session_factory)
    except Exception as e:
         print(f"Postgresql Connection Exception {e}")
    return e

Session = create_session()

# Set up ORM
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "Users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    last_name: Mapped[str] = mapped_column(String(30))
    first_name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))

    def __repr__(self) -> str:
       return f"User(id={self.id}, name={self.last_name}', '{self.first_name}"

# Set up password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dependency to get DB session
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def get_users():
    session = Session()
    users = session.query(User).all()
    session.close()
    return users

# FastAPI app
app = FastAPI()

# OAuth2 configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Authenticate user against database
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user

# Issue access token
def create_access_token(data: dict):
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return access_token

# Token endpoint
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Protected endpoint example
@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return {"username": username}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

if __name__ == '__main__':
    users = get_users()
    for user in users:
        print(user.username, user.last_name, user.first_name)

