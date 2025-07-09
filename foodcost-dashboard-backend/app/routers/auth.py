from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from .. import schemas, models
from ..core.security import hash_password, create_access_token
from ..database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=schemas.auth.TokenResponse, status_code=status.HTTP_201_CREATED)
def register(req: schemas.auth.RegisterRequest, db: Session = Depends(get_db)):
    # 1. Verifica che l’email non esista già
    existing = db.query(models.user.User).filter(models.user.User.email == req.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email già registrata"
        )

    # 2. Crea utente con password hashata
    new_user = models.user.User(
        email=req.email,
        hashed_password=hash_password(req.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 3. Genera JWT e ritorna token
    token = create_access_token(subject=str(new_user.id))
    return {"access_token": token}
