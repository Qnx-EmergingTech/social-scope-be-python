from fastapi import FastAPI
from routers import facebook_api
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",  # your frontend
    # "https://yourdomain.com",  # production frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # domains allowed
    allow_credentials=True,
    allow_methods=["*"],         # allow all HTTP methods
    allow_headers=["*"],         # allow all headers
)

app.include_router(facebook_api.router, prefix="/facebook", tags=["facebook"])

