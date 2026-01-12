from pathlib import Path
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.file import File
from config import settings


async def save_uploaded_file(
    db: AsyncSession, file: UploadFile, workflow_id: int
) -> dict:
    """
    Save an uploaded file to the user_files folder and store metadata in database.
    workflow_id is required - files are associated with a workflow from upload.
    """
    # Create user_files directory if it doesn't exist
    # Use the anchor from settings so the location never changes
    user_files_dir = settings.PROJECT_BASE_DIR / "user_files"

    # Create it safely
    user_files_dir.mkdir(parents=True, exist_ok=True)

    # Save using that directory
    file_path = user_files_dir / Path(file.filename).name

    # Save the file to disk
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Save metadata to database
        file_record = File(
            workflow_id=workflow_id,
            filename=file.filename,
            filepath=str(file_path),
            size=len(content),
            content_type=file.content_type,
        )
        db.add(file_record)
        await db.commit()
        await db.refresh(file_record)

        return {
            "id": file_record.id,
            "filename": file.filename,
            "filepath": str(file_path),
            "size": len(content),
            "content_type": file.content_type,
            "workflow_id": workflow_id,
            "status": "success",
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def delete_file(db: AsyncSession, file_id: int) -> dict:
    """
    Delete a file from user_files folder and database.
    """
    try:
        # Get file record from database
        result = await db.execute(select(File).filter(File.id == file_id))
        file_record = result.scalars().first()

        if not file_record:
            return {"status": "error", "message": f"File record not found"}

        # Delete from disk
        file_path = Path(file_record.filepath)
        if file_path.exists():
            file_path.unlink()

        # Delete from database
        await db.delete(file_record)
        await db.commit()

        return {"status": "success", "message": f"File deleted successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def get_file_list(db: AsyncSession, workflow_id: int) -> list:
    """
    Get list of files for a specific workflow from database.
    """
    try:
        query = select(File).filter(File.workflow_id == workflow_id)

        result = await db.execute(query)
        files = result.scalars().all()

        return [
            {
                "id": f.id,
                "filename": f.filename,
                "filepath": f.filepath,
                "size": f.size,
                "content_type": f.content_type,
                "workflow_id": f.workflow_id,
                "uploaded_at": f.uploaded_at.isoformat() if fuploaded_at else None,
                "is_ingested": f.is_ingested,
                "ingested_at": f.ingested_at.isoformat() if f.ingested_at else None,
            }
            for f in files
        ]
    except Exception as e:
        return []
