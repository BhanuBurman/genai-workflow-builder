from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel
from typing import List

from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.file_service import (
    save_uploaded_file,
    delete_file,
    get_file_list,
)

router = APIRouter()


# --- Schemas ---
class FileUploadResponse(BaseModel):
    id: int
    filename: str
    filepath: str
    size: int
    content_type: str
    workflow_id: int = None
    status: str


class FileDeleteResponse(BaseModel):
    status: str
    message: str


class FileListResponse(BaseModel):
    files: List[dict]


# --- Upload File Endpoint ---
@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    workflow_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """
    Upload a file to the user_files folder and save metadata to database.
    workflow_id is required - files are associated with a workflow from upload.
    """
    try:
        result = await save_uploaded_file(db, file, workflow_id)
        if result["status"] == "success":
            return result
        else:
            raise HTTPException(status_code=500, detail=result["message"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")


# --- Delete File Endpoint ---
@router.delete("/delete", response_model=FileDeleteResponse)
async def delete_uploaded_file(
    file_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a file from user_files folder and database.
    """
    try:
        result = await delete_file(db, file_id)
        if result["status"] == "success":
            return result
        else:
            raise HTTPException(status_code=404, detail=result["message"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File deletion failed: {str(e)}")


# --- List Files Endpoint ---
@router.get("/list", response_model=FileListResponse)
async def list_files(
    workflow_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Get list of files for a specific workflow.
    """
    try:
        files = await get_file_list(db, workflow_id)
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list files: {str(e)}")
