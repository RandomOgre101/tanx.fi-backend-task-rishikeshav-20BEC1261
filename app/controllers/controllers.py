from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash the password
def hash(password: str):
    return pwd_context.hash(password)

# Function to verify hashed passsword against input password
def verify(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)