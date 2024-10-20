from typing import Optional, List, Literal
from pydantic import BaseModel, Field
from datetime import datetime


class ClassData(BaseModel):
    id: Optional[str] = Field(None, description="Class id")
    date: datetime
    classroom: str
    audio: Optional[str] = Field(None, description="Audio url")
    status: Literal['failed', 'running', 'completed'] = Field("running", description="Status of the class")


class ProcessedClass(BaseModel):
    id: Optional[str] = Field(None, description="Process id")
    class_id: str = Field(None, description="Class id")
    audio_text: str = Field(None, description="Audio text")
    summary_text: str = Field(None, description="Summary text")
    embeddings: List[float] = Field(None, description="Ollama Embeddings")
