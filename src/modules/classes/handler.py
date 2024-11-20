import json

from src.logger import log
from src.modules.classes import services, models
from fastapi import Request, APIRouter, BackgroundTasks

from src.modules.classes.services import get_presigned_url, process_audio_file

router = APIRouter()

@router.post("/")
async def save_class(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()

    class_data = models.ClassData(**body)

    res = services.save_class(class_data)

    background_tasks.add_task(process_audio_file, res.audio, res.id)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Class data saved successfully!",
            "data": res.dict()
        }, default=str)
    }


@router.get("/get_presigned")
async def get_presigned(file_name: str, file_type: str):
    presigned_url = get_presigned_url(file_name, file_type)

    return {
        "statusCode": 200,
        "url": presigned_url,
        "message": "Presigned URL generated successfully!"
    }


# GetClass
@router.get("/")
async def get_class(class_id: str):
    class_data, processed_class_data = services.get_class(class_id)
    return {
        "statusCode": 200,
        "body": {
            "class": class_data,
            "processed_class": processed_class_data
        }
    }


# GetClasses
@router.get("/all")
async def get_classes():
    classes = services.get_classes()
    return {
        "statusCode": 200,
        "body": classes
    }