from fastapi import APIRouter, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.db.queries import get_promotions  # new helper function

router = APIRouter(prefix="/promotions", tags=["promotions"])


@router.get("")
def read_promotions(
    page: int = Query(1, gt=0),
    page_size: int = Query(5, gt=0),
    restaurant_name: str = None,
    region: str = None,
):
    data = get_promotions(page, page_size, restaurant_name, region)
    return JSONResponse(content=jsonable_encoder(data))
