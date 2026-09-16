from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def root():
    return {"status": "All good"}
