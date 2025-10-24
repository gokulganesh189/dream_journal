# app/services/image_service.py (optional AI generation stub)
from pathlib import Path
from fastapi import UploadFile
from app.core.config import settings


class ImageService:
    """Handles saving uploads and (optionally) calling AI providers.
    - SRP: Media responsibilities only.
    - OCP: You can subclass to integrate OpenAI/Stability without changing callers.
    """
    def save_upload(self, file: UploadFile) -> str:
        dest = Path(settings.media_dir) / file.filename
        with dest.open("wb") as f:
            f.write(file.file.read())
        return str(dest)


    def generate_ai_image(self, prompt: str) -> str:
        """Stub: integrate real provider and return a URL/path."""
        # In a real impl, call external API and save result.
        return ""