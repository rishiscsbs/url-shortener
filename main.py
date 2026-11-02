import random
import string

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl

app = FastAPI(title="URL Shortener")

# Temporary storage: short code -> long URL (moves to Neon tomorrow)
links = {}


class ShortenRequest(BaseModel):
    url: HttpUrl          # FastAPI checks this is a real URL for you


def make_code(length=6):
    chars = string.ascii_letters + string.digits   # a-z, A-Z, 0-9
    return "".join(random.choice(chars) for _ in range(length))


@app.post("/shorten", status_code=201)
def shorten(req: ShortenRequest):
    code = make_code()
    while code in links:          # tiny chance the code already exists
        code = make_code()
    links[code] = str(req.url)
    return {"code": code, "short_url": f"http://127.0.0.1:8000/{code}"}


@app.get("/{code}")
def redirect(code: str):
    if code not in links:
        raise HTTPException(status_code=404, detail="Short link not found")
    return RedirectResponse(links[code])