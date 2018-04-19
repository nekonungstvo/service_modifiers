from aiohttp import web
from aiohttp.web_exceptions import HTTPNotFound

from modifiers.model import database
from modifiers.model.schema import Wound

wound_app = web.Application()


async def fetch_wound(request):
    wound_id = request.match_info.get('id')

    wound = await database.get_wound(wound_id)

    if not wound:
        raise HTTPNotFound

    return web.json_response(wound.dict())


async def update_wound(request):
    data = await request.json()
    wound = Wound(**data)

    await database.save_wound(wound)

    return web.json_response({
        "status": "ok"
    })


wound_app.router.add_get('/{id}/fetch', fetch_wound)
wound_app.router.add_post('/create', update_wound)
wound_app.router.add_post('/update', update_wound)
