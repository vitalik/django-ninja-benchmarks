import aiohttp
from datetime import datetime
from typing import List
from ninja import NinjaAPI
from ninja.schema import Schema
from pydantic import PositiveInt, constr


class Location(Schema):
    latitude: float = None
    longitude: float = None


class Skill(Schema):
    subject: str
    subject_id: int
    category: str
    qual_level: str
    qual_level_id: int
    qual_level_ranking: float = 0


class Model(Schema):
    id: int
    client_name: constr(max_length=255)
    sort_index: float
    client_phone: constr(max_length=255) = None

    location: Location = None

    contractor: PositiveInt = None
    upstream_http_referrer: constr(max_length=1023) = None
    grecaptcha_response: constr(min_length=20, max_length=1000)
    last_updated: datetime = None

    skills: List[Skill] = []


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
