# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os
import json

app = FastAPI(title="MoviePy Runner")

class RunRequest(BaseModel):
    script: str               # name of the .py file in /app/code 
    payload: dict             # any JSON to pass to the script

@app.post("/run")
async def run_script(req: RunRequest):
    script_path = os.path.join("/app/code", req.script)
    if not os.path.isfile(script_path):
        raise HTTPException(status_code=404, detail=f"Script {req.script} not found")
    try:
        # run the script, passing JSON to stdin
        proc = subprocess.run(
            ["python3", script_path],
            input=json.dumps(req.payload),
            capture_output=True,
            text=True,
            check=True
        )
        return {
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr
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
