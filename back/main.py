from fastapi import FastAPI
from routes.rout_items import router as items
from routes.auth_rout import router as auth
from fastapi.middleware.cors import CORSMiddleware
from lim import limiter
from slowapi.middleware import SlowAPIMiddleware
from database import engine, Base
from db_models import UserDB, ItemDB
from routes.logs_route import router as logs
from logs_middleware import LogMiddleware
from routes.sub_items_rout import router as sub_items


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth)
app.include_router(items)
app.include_router(sub_items)
app.include_router(logs)

app.state.limiter = limiter
app.add_middleware(LogMiddleware)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )

@app.get("/")
def root():
    return{"message": "HELLO To MY API"}
