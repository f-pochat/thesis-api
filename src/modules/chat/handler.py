import json

from fastapi import Request, APIRouter

from src.modules.chat import services

router = APIRouter(prefix="/chat")


@router.post("/")
async def chat(request: Request, class_id: str):
    body = await request.json()

    if "prompt" not in body:
        return {
            "statusCode": 400,
            "message": "Prompt is required"
        }

    prompt = body["prompt"]

    res = services.chat(prompt, class_id)

    return {
        "statusCode": 200,
        "body": res
    }
