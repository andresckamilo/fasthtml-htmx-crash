from dataclasses import dataclass

from fasthtml.common import *
from fasthtml.core import FastHTML
from starlette.staticfiles import StaticFiles
import httpx

app = FastHTMLWithLiveReload(
    hdrs=(Link(rel="stylesheet", href="/public/css/tailwind.css"),)
)
app.mount("/public", StaticFiles(directory="../public"), name="static")


rt: app.route = app.route

current_temperature: int = 20


@dataclass
class Contact:
    name: str
    email: str

    def __xt__(self):
        return Tr(
            Td(Div(self.name, cls="my-4 p-2")),
            Td(Div(self.email, cls="my-4 p-2")),
        )


@rt("/", methods=["GET"])
async def get():
    return Title("Search"), Body(
        Div(
            Div(
                Span(
                    Img(
                        src="/public/img/loader.gif",
                        cls="m-auto h-10",
                        alt="Loading...",
                    ),
                    cls="htmx-indicator",
                    id="loading",
                ),
                H3("Search Contacts", cls="text-2xl mb-3 text-center"),
                Input(
                    type="search",
                    name="search",
                    placeholder="Beding Typing Too Search Users...",
                    cls="border border-gray-600 bg-gray-800 p-2 rounded-lg \
                w-full mb-5",
                    hx_post="/search-api",
                    hx_trigger="input changed delay:100ms, search",
                    hx_target="#search-results",
                    hx_indicator="#loading",
                ),
                Table(
                    Thead(
                        Tr(
                            Th(
                                "Name",
                                scope="col",
                                cls="px-4 py-3 text-center text-xs font-medium uppercase \
                           tracking-wider",
                            ),
                            Th(
                                "Email",
                                scope="col",
                                cls="px-6 py-3 text-center text-xs font-medium uppercase \
                           tracking-wider",
                            ),
                        ),
                        cls="bg-gray-800 text-white",
                    ),
                    Tbody(id="search-results", cls="divide-y divide-gray-600"),
                    cls="min-w-full divide-y divide-gray-200",
                ),
                cls="bg-gray-900 text-white p-4 border \
             border-gray-600 rounded-lg",
            ),
            cls="container mx-auto py-8 max-w-lg",
        ),
        cls="bg-blue-900",
    )


def search_contacts(contacts: list[dict[str:str]], search: str) -> list[dict[str:str]]:
    filtered = [
        Contact(contact["name"], contact["email"]).__xt__()
        for contact in contacts
        if search in contact["name"].lower() or search in contact["email"].lower()
    ]
    return filtered


# Handle post request for user search
@rt("/search", methods=["POST"])
async def search(search: str):
    contacts = [
        {"name": "John Doe", "email": "john@example.com"},
        {"name": "Jane Doe", "email": "jane@example.com"},
        {"name": "Alice Smith", "email": "alice@example.com"},
        {"name": "Bob Williams", "email": "bob@example.com"},
        {"name": "Mary Harris", "email": "mary@example.com"},
        {"name": "David Mitchell", "email": "david@example.com"},
    ]
    import time

    time.sleep(0.2)
    if search:
        result_search = search_contacts(contacts, search.lower())
    else:
        result_search = [Tr("")]

    print(Tr(*result_search))

    return Tbody(*result_search, id="search-results", cls="divide-y divide-gray-600")


@rt("/search-api", methods=["POST"])
async def search(search: str):
    response = httpx.get("https://jsonplaceholder.typicode.com/users")
    contacts = response.json()
    import time

    time.sleep(0.2)
    if search:
        result_search = search_contacts(contacts, search.lower())
    else:
        result_search = []

    return Tbody(*result_search, id="search-results", cls="divide-y divide-gray-600")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)