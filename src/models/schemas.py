from typing import List, Literal, Optional, Union
from pydantic import BaseModel, Field


class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class CompletionRequest(BaseModel):
    model: str = Field(..., example="llama3-8b-ft-v2")
    messages: List[Message]
    max_tokens: Optional[int] = Field(None, ge=1, le=8192)
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    top_p: Optional[float] = Field(None, ge=0.0, le=1.0)
    stream: bool = False
    stop: Optional[Union[str, List[str]]] = None
    n: int = Field(1, ge=1, le=4)


class ChoiceMessage(BaseModel):
    role: Literal["assistant"] = "assistant"
    content: str


class Choice(BaseModel):
    index: int
    message: ChoiceMessage
    finish_reason: Literal["stop", "length", "content_filter"]


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class CompletionResponse(BaseModel):
    id: str
    object: Literal["chat.completion"] = "chat.completion"
    model: str
    choices: List[Choice]
    usage: Usage


class DeltaMessage(BaseModel):
    role: Optional[Literal["assistant"]] = None
    content: Optional[str] = None


class StreamChoice(BaseModel):
    index: int
    delta: DeltaMessage
    finish_reason: Optional[Literal["stop", "length"]] = None


class CompletionChunk(BaseModel):
    id: str
    object: Literal["chat.completion.chunk"] = "chat.completion.chunk"
    model: str
    choices: List[StreamChoice]


class ModelCard(BaseModel):
    id: str
    object: Literal["model"] = "model"
    owned_by: str = "mlops-team"


class ModelList(BaseModel):
    object: Literal["list"] = "list"
    data: List[ModelCard]
