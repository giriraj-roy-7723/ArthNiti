from fastapi import APIRouter
from app.services.notebook_adapter import get_notebook_data
from app.services.data_pipeline import process_data
from app.services.inference import run_inference

router = APIRouter()

@router.get("/notebook-data")
async def fetch_notebook_data():
    data = await get_notebook_data()
    return {"data": data}

@router.post("/process-data")
async def handle_data_processing(input_data: dict):
    processed_data = await process_data(input_data)
    return {"processed_data": processed_data}

@router.post("/run-inference")
async def handle_inference(input_data: dict):
    inference_result = await run_inference(input_data)
    return {"inference_result": inference_result}