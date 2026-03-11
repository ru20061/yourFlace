import aioboto3
import aiofiles
import os
from typing import Optional, BinaryIO
import mimetypes
from app.config import settings

# 로컬 저장소 경로 (S3/MinIO 미사용 시 fallback)
LOCAL_UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "static", "uploads")

class CloudflareR2Storage:
    def __init__(self):
        self.session = aioboto3.Session(
            aws_access_key_id=settings.CLOUDFLARE_R2_ACCESS_KEY,
            aws_secret_access_key=settings.CLOUDFLARE_R2_SECRET_KEY,
        )
        self.bucket = settings.CLOUDFLARE_R2_BUCKET
        self.endpoint = settings.CLOUDFLARE_R2_ENDPOINT
        self.public_url = settings.CLOUDFLARE_R2_PUBLIC_URL

    async def _save_local(self, file_obj: BinaryIO, object_name: str) -> str:
        """로컬 디스크에 파일 저장 (S3 연결 불가 시 fallback)"""
        filename = object_name.replace("/", "_")
        save_path = os.path.join(LOCAL_UPLOAD_DIR, filename)
        os.makedirs(LOCAL_UPLOAD_DIR, exist_ok=True)
        data = file_obj.read()
        async with aiofiles.open(save_path, "wb") as f:
            await f.write(data)
        return f"http://localhost:8000/static/uploads/{filename}"

    async def upload_file(
        self,
        file_obj: BinaryIO,
        object_name: str,
        content_type: Optional[str] = None,
        metadata: Optional[dict] = None
    ) -> str:
        """파일 업로드 및 Public URL 반환 (S3 실패 시 로컬 저장 fallback)"""
        if not content_type:
            content_type = mimetypes.guess_type(object_name)[0] or 'application/octet-stream'

        extra_args = {'ContentType': content_type}
        if metadata:
            extra_args['Metadata'] = metadata

        try:
            async with self.session.client(
                's3',
                endpoint_url=self.endpoint,
            ) as s3_client:
                await s3_client.upload_fileobj(
                    file_obj,
                    self.bucket,
                    object_name,
                    ExtraArgs=extra_args
                )
            return f"{self.public_url}/{object_name}"
        except Exception:
            # S3/MinIO 미실행 시 로컬 저장소로 fallback
            file_obj.seek(0)
            return await self._save_local(file_obj, object_name)
    
    async def download_file(self, object_name: str) -> bytes:
        """파일 다운로드"""
        async with self.session.client(
            's3',
            endpoint_url=self.endpoint,
        ) as s3_client:
            response = await s3_client.get_object(
                Bucket=self.bucket,
                Key=object_name
            )
            return await response['Body'].read()
    
    async def delete_file(self, object_name: str) -> bool:
        """파일 삭제"""
        async with self.session.client(
            's3',
            endpoint_url=self.endpoint,
        ) as s3_client:
            await s3_client.delete_object(
                Bucket=self.bucket,
                Key=object_name
            )
        return True
    
    async def list_files(self, prefix: str = "") -> list:
        """파일 목록 조회"""
        async with self.session.client(
            's3',
            endpoint_url=self.endpoint,
        ) as s3_client:
            response = await s3_client.list_objects_v2(
                Bucket=self.bucket,
                Prefix=prefix
            )
            return response.get('Contents', [])
    
    async def file_exists(self, object_name: str) -> bool:
        """파일 존재 여부 확인"""
        try:
            async with self.session.client(
                's3',
                endpoint_url=self.endpoint,
            ) as s3_client:
                await s3_client.head_object(
                    Bucket=self.bucket,
                    Key=object_name
                )
            return True
        except:
            return False

storage = CloudflareR2Storage()

async def init_storage():
    """스토리지 초기화"""
    pass
