from fastapi import BackgroundTasks
from typing import Any, Dict

def process_data(data: Dict[str, Any]) -> None:
    # Function to process data
    pass

def run_inference(data: Dict[str, Any]) -> Any:
    # Function to run inference on the processed data
    pass

def schedule_background_task(background_tasks: BackgroundTasks, data: Dict[str, Any]) -> None:
    background_tasks.add_task(process_data, data)
    background_tasks.add_task(run_inference, data)