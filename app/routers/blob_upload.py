import os
import requests
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import Dict

router = APIRouter()

@router.post("/upload-csv-blob")
async def upload_csv_to_blob(file: UploadFile = File(...)) -> Dict[str, str]:
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be CSV format")
    
    # Get Vercel Blob token from environment
    blob_token = os.getenv("BLOB_READ_WRITE_TOKEN")
    if not blob_token:
        raise HTTPException(status_code=500, detail="Blob token not configured")
    
    try:
        # Read file content
        file_content = await file.read()
        
        # Vercel Blob API endpoint
        blob_api_url = f"https://blob.vercel-storage.com/{file.filename}"
        
        headers = {
            'Authorization': f'Bearer {blob_token}',
            'Content-Type': 'text/csv',
            'x-content-type': 'text/csv'
        }
        
        # Upload to Vercel Blob
        response = requests.put(
            blob_api_url,
            headers=headers,
            data=file_content
        )
        
        if response.status_code not in [200, 201]:
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to upload to blob: {response.text}"
            )
        
        blob_data = response.json()
        
        return {
            "message": "File uploaded to Vercel Blob successfully",
            "blob_url": blob_data.get('url', blob_api_url),
            "filename": file.filename,
            "size": len(file_content)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")