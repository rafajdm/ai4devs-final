from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.db.queries import get_promotions  # new helper function

router = APIRouter(prefix="/promotions", tags=["promotions"])


@router.get("/")
def read_promotions():
    data = get_promotions()
    return JSONResponse(content=jsonable_encoder(data))
