# Network service simulates some close to real life io work
# by just slleeping a bit on each request

import asyncio
from sanic import Sanic
from sanic.response import text


app = Sanic("some_job")


@app.route("<path:path>")
async def test(request, path):
    await asyncio.sleep(0.1)  # This is the work
    return text('OK')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, workers=8)
