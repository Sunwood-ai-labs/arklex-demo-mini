import os
import logging
import string
import subprocess
import signal
import atexit
from typing import Dict
import json
from http import HTTPStatus
import argparse

from arklex.env.env import Env
import uvicorn

from openai import OpenAI
from fastapi import FastAPI, Response

from arklex.orchestrator.orchestrator import AgentOrg
from create import API_PORT
from arklex.utils.model_config import MODEL

NLUAPI_ADDR = f"http://localhost:{API_PORT}/nlu"
SLOTFILLAPI_ADDR = f"http://localhost:{API_PORT}/slotfill"

logger = logging.getLogger(__name__)
app = FastAPI()

# CONFIG_TASKGRAPH = None

# @app.on_event("startup")
# def load_config():
#     global CONFIG_TASKGRAPH
#     parser = argparse.ArgumentParser(description="Start FastAPI with custom config.")
#     parser.add_argument("--config_taskgraph", type=str, required=True, help="Path to the task graph configuration.")
#     args, _ = parser.parse_known_args()  # Allows FastAPI/uvicorn to pass unknown args
#     CONFIG_TASKGRAPH = args.config_taskgraph
#     if not CONFIG_TASKGRAPH:
#         raise ValueError("CONFIG_TASKGRAPH argument is required.")

process = None  # Global reference for the FastAPI subprocess

def terminate_subprocess():
    """Terminate the FastAPI subprocess."""
    global process
    if process and process.poll() is None:  # Check if process is running
        logger.info(f"Terminating FastAPI process with PID: {process.pid}")
        process.terminate()  # Send SIGTERM
        process.wait()  # Ensure it stops
        logger.info("FastAPI process terminated.")

# Register cleanup function to run on program exit
atexit.register(terminate_subprocess)

# Handle signals (e.g., Ctrl+C)
signal.signal(signal.SIGINT, lambda signum, frame: exit(0))
signal.signal(signal.SIGTERM, lambda signum, frame: exit(0))


def get_api_bot_response(args, history, user_text, parameters, env):
    data = {"text": user_text, 'chat_history': history, 'parameters': parameters}
    orchestrator = AgentOrg(config=os.path.join(args.input_dir, "taskgraph.json"), env=env)
    result = orchestrator.get_response(data)

    return result['answer'], result['parameters']


def start_apis():
    """Start the FastAPI subprocess and update task graph API URLs."""
    global process
    
    command = [
        "uvicorn",
        "arklex.orchestrator.NLU.api:app",  # Replace with proper import path
        "--port", API_PORT,
        "--host", "0.0.0.0",
        "--log-level", "info"
    ]

    # Redirect FastAPI logs to a file
    with open("./logs/model_api.log", "w") as log_file:
        process = subprocess.Popen(
            command,
            stdout=log_file,  # Redirect stdout to a log file
            stderr=subprocess.STDOUT,  # Redirect stderr to the same file
            start_new_session=True  # Run in a separate process group
        )
    logger.info(f"Started FastAPI process with PID: {process.pid}")


@app.post("/eval/chat")
def predict(data: Dict):
    history = data['history']
    params = data['parameters']
    workers = data['workers']
    tools = data['tools']
    user_text = history[-1]['content']

    env = Env(
        tools = tools,
        workers = workers,
        slotsfillapi = SLOTFILLAPI_ADDR
    )
    answer, params = get_api_bot_response(args, history[:-1], user_text, params, env)
    return {"answer": answer, "parameters": params}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start FastAPI with custom config.")
    parser.add_argument('--input-dir', type=str, default="./examples/test")
    parser.add_argument('--model', type=str, default=MODEL["model_type_or_path"])
    parser.add_argument('--port', type=int, default=8000, help="Port to run the FastAPI app")
    
    args = parser.parse_args()
    os.environ["DATA_DIR"] = args.input_dir
    MODEL["model_type_or_path"] = args.model

    start_apis()

    #run server
    uvicorn.run(app, host="0.0.0.0", port=args.port)