from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/create")
async def root(request: Request):
    json_data = await request.json()
    print(json_data)
    return {"message": "Hello World"}


@app.get("/get")
async def root():
    return "not implemented"


@app.post("/update")
async def root():
    return "not implemented"
