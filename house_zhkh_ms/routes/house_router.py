from fastapi import APIRouter, HTTPException
from fastapi_utils.cbv import cbv
from controllers.house_controller.house_controller import HouseController
from schemas.house_schema import HouseInfo, NewHouseRequest

router = APIRouter (
    prefix="/houses",
    tags=["Houses"]
)

@cbv(router)
class HouseRouter:
    controller: HouseController = HouseController()

    @router.get("/info", response_model=HouseInfo)
    async def get_house_info(
        self, 
        house_street: str
    ) -> HouseInfo:
        
        """
        Retrieve house information based on the provided street.

        Args:
            house_street (str): The street name where the house is located.

        Returns:
            HouseInfo: Information about the house located on the specified street.

        Raises:
            HTTPException: If the house information cannot be retrieved, a 400 status is raised.
        """
        
        try:
            return await self.controller.get(house_street)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.post("/new", response_model=HouseInfo, status_code=201)
    async def add_new_house(
        self, 
        request: NewHouseRequest
    ) -> HouseInfo:
        
        """
        Create a new house resource.

        Args:
            request (NewHouseRequest): The data for the new house to be created.

        Returns:
            HouseInfo: The newly created house information.

        Raises:
            HTTPException: If the house creation fails, a 400 status is raised.
        """
        
        try:
            return await self.controller.create(request.dict())
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.post("/{house_id}/flats", status_code=501)
    async def add_new_flat(
        self, 
        house_id: int
    ):
        """
        Endpoint stub for adding a new flat. Returns a 501 Not Implemented status.

        Args:
            house_id (int): The ID of the house to which the flat will be added.

        Returns:
            dict: A message indicating that the functionality is not implemented.
        """
        
        return {"message": "Not implemented"}
