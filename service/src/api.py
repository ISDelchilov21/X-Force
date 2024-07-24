from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, users, organisation, clasess, themes, homeworks, grades

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(organisation.router)
app.include_router(clasess.router)
app.include_router(themes.router)
app.include_router(homeworks.router)
app.include_router(grades.router)