from fastapi import APIRouter, Query, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.db.queries import get_promotions, get_promotion_by_id

router = APIRouter(prefix="/promotions", tags=["promotions"])


@router.get("/")
def read_promotions(
    page: int = Query(1, gt=0),
    page_size: int = Query(5, gt=0),
    restaurant_name: str = None,
    region: str = None,
):
    data = get_promotions(page, page_size, restaurant_name, region)
    return JSONResponse(content=jsonable_encoder(data))


@router.get("/{promotion_id}")
def read_promotion(promotion_id: int):
    data = get_promotion_by_id(promotion_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return JSONResponse(content=jsonable_encoder(data))
