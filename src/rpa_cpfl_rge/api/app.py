from fastapi import FastAPI

app = FastAPI(
    title="RPA: CPFL RGE",
    description="API para extração de faturas CPFL RGE",
    version="0.0.1",
)


@app.get("/")
def read_root():
    print(' -> "Hello": "World"')
    return {"Hello": "World"}


@app.get("/hello")
def read_root():
    print(' -> "Hello": "Mundooo"')
    return {"Hello": "Mundooo"}


@app.get("/healthcheck")
def read_root():
    print(' -> "WORKING"')
    return {"WORKING"}
