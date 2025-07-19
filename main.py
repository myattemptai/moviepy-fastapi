# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os

app = FastAPI(title="MoviePy Runner")

class RunRequest(BaseModel):
    script: str  # name of the Python file to execute

@app.post("/run")
async def run_script(req: RunRequest):
    script_path = os.path.join("/app/code", req.script)
    if not os.path.isfile(script_path):
        raise HTTPException(status_code=404, detail=f"Script {req.script} not found")
    try:
        result = subprocess.run(
            ["python3", script_path],
            capture_output=True,
            text=True,
            check=True
        )
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except subprocess.CalledProcessError as e:
        raise HTTPException(
            status_code=500,
            detail={
                "returncode": e.returncode,
                "stdout": e.stdout,
                "stderr": e.stderr
            }
        )