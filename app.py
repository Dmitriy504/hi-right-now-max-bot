from fastapi import FastAPI

app = FastAPI(title="Hi Right Now MAX Bot")


@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "Hi Right Now MAX Bot is running 🚀"
    }


@app.get("/health")
async def health():
    return {"ok": True}
