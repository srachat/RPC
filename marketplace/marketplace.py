import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import grpc

from recommendations_pb2 import BookCategory, RecommendationRequest
from recommendations_pb2_grpc import RecommendationsStub


app = FastAPI()

recommendations_host = os.getenv("RECOMMENDATION_HOST", "localhost")
recommendations_channel = grpc.insecure_channel(f"{recommendations_host}:50051")
recommendations_client = RecommendationsStub(recommendations_channel)

templates = Jinja2Templates(directory="templates")


@app.get("/",  response_class=HTMLResponse)
async def render_homepage(request: Request):
    recommendations_request = RecommendationRequest(
        user_id=1, category=BookCategory.MYSTERY, max_results=3)
    recommendations_response = recommendations_client.Recommend(recommendations_request)
    return templates.TemplateResponse(
        "homepage.html",
        {
            "request": request,
            "recommendations": recommendations_response.recommendations,
        }
    )
