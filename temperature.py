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


@rt("/", methods=["GET"])
async def get():
    return Title("Temperature"), Body(
        Div(
            Div(
                H1("Temperature converter", cls="text-2xl font-bold mb-4"),
                Form(
                    Label("Fahrenheit:", fr="fahrenheit"),
                    Input(
                        type="number",
                        name="fahrenheit",
                        cls="border p-2 rounded",
                        value="32",
                        required="",
                        # hx_post="/convert",
                        # hx_target="#result",
                        # hx_indicator="#loading",
                        # hx_trigger="keyup changed delay:5ms",
                    ),
                    Button(
                        "Convert",
                        type="submit",
                        cls="bg-blue-500 text-white px-4 py-2 rounded",
                    ),
                    Div(id="result", cls="mt-6 text-xl"),
                    Span(
                        Img(
                            src="/public/img/loader.gif",
                            cls="m-auto h-10",
                            alt="Loading...",
                        ),
                        id="loading",
                        cls="htmx-indicator",
                    ),
                    hx_trigger="submit",
                    hx_post="/convert",
                    hx_target="#result",
                    hx_indicator="#loading",
                ),
                cls="bg-white p-4 border rounded-lg max-w-lg m-auto",
            ),
            cls="container mx-auto mt-8 text-center",
        ),
        cls="bg-gray-100",
    )


## Handle post request for temp conversion
@rt("/convert", methods=["POST"])
async def convert(fahrenheit: str):
    import time
    time.sleep(0.25)
    fahrenheit = fahrenheit or 0
    celsius = (float(fahrenheit) - 32) * 5/9
    return P(
        f"{fahrenheit}°F is {celsius:.2f}°C",
        cls="text-2xl font-bold my-5",
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
