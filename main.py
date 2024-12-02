import os
import shutil

import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from mapping import extract_text

app = FastAPI()

try:
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    temp_dir = os.path.join(current_directory, "temp")
    os.makedirs(temp_dir, exist_ok=True)
except OSError:
    pass


@app.post("/ocr")
async def ocr_api(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        temp_file_path = os.path.join(temp_dir, f"temp_{file.filename}")

        with open(temp_file_path, "wb") as temp_file:
            shutil.copyfileobj(file.file, temp_file)

        try:
            extracted_data = extract_text(temp_file_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error during OCR processing: {e}")
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

        return JSONResponse(content=extracted_data)

    except Exception as e:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        raise HTTPException(status_code=500, detail=f"File processing failed: {e}")


if __name__ == "__main__":
    port_number = int(os.getenv('PORT_NUMBER'))
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=port_number,
        proxy_headers=True
    )
