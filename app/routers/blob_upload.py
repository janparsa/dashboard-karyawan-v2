import os
import requests
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict

router = APIRouter()

@router.post("/upload-csv-blob")
async def upload_csv_to_blob(file: UploadFile = File(...)) -> Dict[str, str]:
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be CSV format")
    
    # Get Vercel Blob token from environment
    blob_token = os.getenv("dashboardkaryawanV2_READ_WRITE_TOKEN")
    if not blob_token:
        raise HTTPException(status_code=500, detail="Blob token not configured")
    
    try:
        # Prepare headers for Vercel Blob API
        headers = {
            "Authorization": f"Bearer {blob_token}",
            "Content-Type": "text/csv"
        }
        
        # Stream file directly to Vercel Blob
        blob_url = f"https://blob.vercel-storage.com/{file.filename}"
        
        # Read file content as stream and upload
        file_content = await file.read()
        
        response = requests.put(
            blob_url,
            headers=headers,
            data=file_content
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to upload to blob: {response.text}"
            )
        
        blob_data = response.json()
        
        return {
            "message": "File uploaded successfully",
            "blob_url": blob_data.get("url", blob_url),
            "filename": file.filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")