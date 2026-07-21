from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.dependencies import get_current_user

from app.services.dashboard import (
    buscar_dashboard_service
)


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def dashboard(
    db: Session = Depends(get_db),
    usuario = Depends(get_current_user)
):

    return buscar_dashboard_service(
        db,
        usuario
    )