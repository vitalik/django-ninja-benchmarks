import aiohttp
import datetime
from typing import List
from ninja import NinjaAPI
from ninja.schema import Schema
from pydantic import PositiveInt, constr, BaseModel, Field


class Location(BaseModel):
    latitude: float | None = None
    longitude: float | None = None


class Skill(BaseModel):
    subject: str
    subject_id: int
    category: str
    qual_level: str
    qual_level_id: int
    qual_level_ranking: float = 0


class Model(BaseModel):
    id: int
    client_name: str = Field(max_length=255)
    sort_index: float
    client_phone: str | None = Field(None, max_length=255)
    location: Location
    contractor: int | None = Field(None, gt=0)
    upstream_http_referrer: str | None = Field(None, max_length=1023)
    grecaptcha_response: str = Field(min_length=20, max_length=1000)
    last_updated: datetime.datetime | None
    skills: List[Skill]



api = NinjaAPI()


@api.post("/create")
def create(request, model: Model):
    return {"success": True}


@api.get("/iojob")
async def iojob(request):
    async with aiohttp.ClientSession() as http_client:
        r = await http_client.get('http://network_service:8000/job')
        data = await r.text()
    return {"success": True}
