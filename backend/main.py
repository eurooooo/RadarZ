from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()


origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Project(BaseModel):
    id: str
    title: str
    authors: str
    date: str
    description: str
    tags: list[str]
    stars: int
    forks: int


mock_projects: list[Project] = [
    Project(
        id="1",
        title="facebook/react",
        authors="Facebook",
        date="2 days ago",
        description=(
            "A declarative, efficient, and flexible JavaScript library for building "
            "user interfaces. React makes it painless to create interactive UIs."
        ),
        tags=["javascript", "react", "ui", "frontend"],
        stars=234_000,
        forks=46_000,
    ),
    Project(
        id="2",
        title="vercel/next.js",
        authors="Vercel",
        date="1 day ago",
        description=(
            "The React Framework for Production. Next.js gives you the best developer "
            "experience with all the features you need for production."
        ),
        tags=["javascript", "react", "nextjs", "framework"],
        stars=125_000,
        forks=25_000,
    ),
    Project(
        id="3",
        title="microsoft/typescript",
        authors="Microsoft",
        date="3 days ago",
        description=(
            "TypeScript is a superset of JavaScript that compiles to clean JavaScript "
            "output. It adds static type definitions to JavaScript."
        ),
        tags=["typescript", "language", "compiler"],
        stars=98_000,
        forks=12_800,
    ),
]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/projects", response_model=List[Project])
async def get_projects() -> list[Project]:
    return mock_projects