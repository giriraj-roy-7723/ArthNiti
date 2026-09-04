from pydantic import BaseModel
from typing import List, Optional

class Issue(BaseModel):
    id: int
    title: str
    description: str
    status: str

class IssuesList(BaseModel):
    issues: List[Issue]

class NotebookData(BaseModel):
    content: str
    metadata: Optional[dict] = None

class InferenceResult(BaseModel):
    result: str
    confidence: float

class DataPipelineInput(BaseModel):
    data: List[NotebookData]
    parameters: Optional[dict] = None

class DataPipelineOutput(BaseModel):
    processed_data: List[NotebookData]
    errors: Optional[List[str]] = None