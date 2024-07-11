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

current_temperature: int = 20


@rt("/", methods=["GET"])
async def get():
    return Title("Pulling"), Body(
        Div(
            H1("Weather in New York", cls="text-xl mb-4"),
            P(Span("Loading...", hx_get="/get-temperature", hx_trigger="every 0.5s"),cls="text-center"),
            cls="text-center",
        ),
        cls="bg-blue-900 text-white min-h-screen flex items-center justify-center",
    )


@rt("/get-temperature", methods=["GET"])
async def poll():
    import random

    global current_temperature
    current_temperature += random.randint(-1, 1) * 2 - 0.5  # Random change in temperature
    return Div(f"Temperature: {current_temperature}°C", cls="text-center")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
