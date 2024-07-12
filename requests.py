from typing import Callable

import uvicorn
from fastcore.all import patch
from fasthtml.common import *
from fasthtml.core import FastHTML
from starlette.staticfiles import StaticFiles
from dataclasses import dataclass
import httpx

app: FastHTML = FastHTMLWithLiveReload(
    hdrs=(Script(src="https://cdn.tailwindcss.com"), )
)

app.mount("/public", StaticFiles(directory="public"), name="public")

@dataclass
class Person:
    id: int
    name: str

    def __xt__(self):
      return Li(self.name)


rt: app.route = app.route


@rt("/", methods=["GET"])
async def get():
    return Title("Users"),Body(
        Div(
            H1("Simple request example", cls="text-2xl font-bold my-5"),
            Button(
                "Fetch users",
                hx_get="/users",
                hx_trigger="mouseover",
                hx_target="#users",
                hx_indicator="#loading",
                hx_vals='{"limit":3}',
              #  hx_confirm='Are you sure you want to fetch users?',
                cls="bg-blue-500 text-white py-2 px-3 my-5\
                rounded-lg",
            ),
            Span( 
                Img(src="/public/img/loader.gif", cls="m-auto h-10", alt="Loading..."),
                id="loading", cls="htmx-indicator"),
            Div(id="users"),
            cls="text-center",

        )
    )


@rt("/users", methods=["GET"])
async def get_users(limit: int):
    limit = int(limit) or 10
    response = httpx.get(f"https://jsonplaceholder.typicode.com/users?_limit={limit}")
    users = response.json()
    return Div(
        H1("Users", cls="text-2xl font-bold my-4"),
        Ul(*[Person(user["id"], user["name"]) for user in users]),
        cls="text-center",
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
