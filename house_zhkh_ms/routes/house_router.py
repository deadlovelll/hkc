from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from controllers.house_controller.house_controller import HouseController
from schemas.house_schema import HouseInfo, NewHouseRequest

router = APIRouter (
    prefix="/houses",
    tags=["Houses"]
)

def get_house_controller() -> HouseController:
    """
    Dependency injection for the HouseController.
    """
    return HouseController()

@router.get("/info", response_model=HouseInfo)
async def get_house_info (
    house_street: str, 
    controller: HouseController = Depends(get_house_controller),
) -> JSONResponse:
    
    try:
        return await controller.get_house_info(house_street)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/new", response_model=HouseInfo, status_code=201)
async def add_new_house (
    request: NewHouseRequest, 
    controller: HouseController = Depends(get_house_controller),
)-> JSONResponse:
    
    try:
        return await controller.add_new_house(request.house_street)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{house_id}/flats", response_class=JSONResponse, status_code=501)
async def add_new_flat (
    house_id: int
)-> JSONResponse:
    
    """
    Endpoint stub for adding a new flat. Returns a 501 Not Implemented status.
    """
    
    return JSONResponse({"message": "Not implemented"}, status_code=501)
