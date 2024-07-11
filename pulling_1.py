from dataclasses import dataclass
from typing import Callable

import httpx
import uvicorn
from fastcore.all import patch
from fasthtml.common import *
from fasthtml.core import FastHTML
from starlette.staticfiles import StaticFiles

app: FastHTML = FastHTMLWithLiveReload(
    hdrs=(Script(src="https://cdn.tailwindcss.com"),)
)

app.mount("/public", StaticFiles(directory="public"), name="public")


rt: app.route = app.route

counter:int = 0

@rt("/", methods=["GET"])
async def get():
    return Title("Pulling"), Body(
        Div(
            Span("Loading",hx_get="/poll", hx_trigger="every 5s")
            ,cls="text-center"
        )

    )

@rt("/poll", methods=["GET"])
async def poll():
    global counter
    counter += 1
    return Div(f"Polled {counter} times", cls="text-center")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
