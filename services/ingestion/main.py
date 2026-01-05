import sys
import os
import shutil
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel

# Fix the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from agents_core.orchestrator import DefenseOrchestrator

app = FastAPI(title="VeriShield AI Defense Node")
brain = DefenseOrchestrator()

@app.post("/verify")
async def verify_transaction(
    user_id: str = Form(...),
    amount: float = Form(...),
    image_file: UploadFile = File(...)  # <--- NEW: Accepts a File!
):
    print(f"📨 API RECEIVED: Request for {user_id} with Image Analysis")
    
    # 1. Save the uploaded image temporarily so the AI can read it
    temp_filename = f"temp_{image_file.filename}"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(image_file.file, buffer)

    try:
        # 2. Call the AI Brain with the image path
        decision = await brain.analyze_transaction(user_id, amount, image_path=temp_filename)
        
        # 3. Cleanup: Delete the temp file after analysis
        os.remove(temp_filename)

        if "BLOCKED" in decision:
            raise HTTPException(status_code=403, detail=decision)
        
        return {"status": "APPROVED", "message": decision}

    except Exception as e:
        # Cleanup even if error
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        raise HTTPException(status_code=500, detail=str(e))