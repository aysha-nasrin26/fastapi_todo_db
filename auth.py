from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

#Password Context create
#CryptContext Password hashing manager.
pwd_context = CryptContext(
    #bcrypt algorithm use
    schemes=["bcrypt"],
    #Old algorithms irundha automatically handled
    deprecated="auto"
)

# JWT Configuration
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#Password Hash Func
def hash_password(password: str):
    return pwd_context.hash(password)

#Password Verify Func
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

#token le store aare infor
def create_access_token(data: dict):
    to_encode = data.copy()#Original data dictionary-a modify panna koodad
    #Expiry Time Create
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})#exp add
    
    #JWT Encode
    encoded_jwt = jwt.encode(
    to_encode,
    SECRET_KEY,
    algorithm=ALGORITHM
)
    return encoded_jwt

    #JWT Decode
    payload = jwt.decode(
    token,
    SECRET_KEY,
    algorithms=[ALGORITHM]
    )