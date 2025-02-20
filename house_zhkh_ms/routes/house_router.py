from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv
from controllers.house_controller.house_controller import HouseController
from schemas.house_schema import HouseInfo, NewHouseRequest

router = APIRouter(
    prefix="/houses",
    tags=["Houses"]
)

def get_house_controller() -> HouseController:
    """
    Dependency injection for the HouseController.
    """
    return HouseController()

@cbv(router)
class HouseRouter:
    controller: HouseController = Depends(get_house_controller)

    @router.get("/info", response_model=HouseInfo)
    async def get_house_info (
        self, 
        house_street: str
    ) -> HouseInfo:
        
        """
        Retrieve house information based on the provided street.
        """
        
        try:
            return await self.controller.get(house_street)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.post("/new", response_model=HouseInfo, status_code=201)
    async def add_new_house (
        self, 
        request: NewHouseRequest
    ) -> HouseInfo:
        
        """
        Create a new house resource.
        """
        
        try:
            return await self.controller.create(request.dict())
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.post("/{house_id}/flats", status_code=501)
    async def add_new_flat (
        self, 
        house_id: int
    ):
        """
        Endpoint stub for adding a new flat. Returns a 501 Not Implemented status.
        """
        return {"message": "Not implemented"}
