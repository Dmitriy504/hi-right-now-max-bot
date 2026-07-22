from fastapi import FastAPI, Request

app = FastAPI(title="Hi Right Now MAX Bot")


@app.get("/")
async def root():
    return {"status": "ok"}


@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    print("=" * 60)
    print("UPDATE:")
    print(data)
    print("=" * 60)

    return {"ok": True}
