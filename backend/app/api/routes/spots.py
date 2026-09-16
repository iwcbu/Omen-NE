from fastapi import APIRouter

router = APIRouter()

fakeSpotDb = [
    { "item_name": "Foo" },
    { "item_name": "Bk" }, 
    { "item_name": "Ld" },
    { "item_name": "Mp" },
    { "item_name": "We" },
    { "item_name": "Vqp" },
    { "item_name": "Paa" },
    ]


@router.get("/spots")
async def get_all_spots(skip: int = 0, limit: int = 3):
    '''
        Returns a list of spots

        Query Params: 
            skip -> index where the returns items start in the db
            limit -> number of items per return
    
    '''
    return fakeSpotDb[skip : skip + limit]




@router.get("/spot/{spot_id}")
async def spot_id_of_spot(spot_id: str):
    '''
        Returns id of a spot
    '''
    return {"spot_id": spot_id}