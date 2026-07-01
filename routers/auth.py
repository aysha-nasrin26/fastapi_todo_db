from fastapi import APIRouter,Depends,HTTPException
from models import User
from schemas import Token, UserCreate, UserLogin, UserResponse
from sqlalchemy.orm import Session
from database import get_db
from auth import create_access_token, hash_password, verify_password, SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
#APIRouter helps organize related endpoints into separate modules. It improves code readability, maintainability, and scalability for larger FastAPI applications.
#Register endpoint logic
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    #Password hash
    hashed_pw = hash_password(user.password)
    
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
        
    #SQLAlchemy User object create
    new_user = User(
    email=user.email,
    hashed_password=hashed_pw
)

    db.add(new_user)
    db.commit()
    
    return{
        "message":"register  successfully"
    }
    
#Login Endpoint
@router.post("/login",response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == form_data.username).first()
    # 401 Unauthorized raise pannuvom
    if not db_user:
        raise HTTPException(
        status_code=401,
        detail="Invalid email or password"
    )

    if not verify_password(
        form_data.password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    token = create_access_token(
        {"sub": db_user.email}
    )
    return{
    "access_token":token,
    "token_type": "bearer"
    }

#endpoint usage
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )
    try:#decode,getmail,mail check
        payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
        )
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        
#401
    except JWTError:
        raise credentials_exception
#db query
    current_user = db.query(User).filter(
        User.email == email
    ).first()
#user check
    if current_user is None:
        raise credentials_exception
    return current_user

#protected route
@router.get("/me", response_model=UserResponse)#api scure,ext field remove,resp validate
def read_me(
    current_user: User = Depends(get_current_user)
):
    return current_user