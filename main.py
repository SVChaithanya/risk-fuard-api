from fastapi import FastAPI
from db import Base,engine
from router import login,reg,transaction,refresh
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reg.router)
app.include_router(login.router)
app.include_router(refresh.router)
app.include_router(transaction.router)

@app.get("/")
def root():
    return {
        "message": "Finance Tracker API is running"
    }
