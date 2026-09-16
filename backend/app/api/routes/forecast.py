from fastapi import APIRouter

router = APIRouter()

@router.get("/forecast")
def root():
    return {"forecast": "yuh"}
