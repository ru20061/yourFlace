import aioboto3
from typing import Optional, BinaryIO
import mimetypes
from app.config import settings

class CloudflareR2Storage:
    def __init__(self):
        self.session = aioboto3.Session(
            aws_access_key_id=settings.CLOUDFLARE_R2_ACCESS_KEY,
            aws_secret_access_key=settings.CLOUDFLARE_R2_SECRET_KEY,
        )
        self.bucket = settings.CLOUDFLARE_R2_BUCKET
        self.endpoint = settings.CLOUDFLARE_R2_ENDPOINT
        self.public_url = settings.CLOUDFLARE_R2_PUBLIC_URL
    
    async def upload_file(
        self,
        file_obj: BinaryIO,
        object_name: str,
        content_type: Optional[str] = None,
        metadata: Optional[dict] = None
    ) -> str:
        """파일 업로드 및 Public URL 반환"""
        if not content_type:
            content_type = mimetypes.guess_type(object_name)[0] or 'application/octet-stream'
        
        extra_args = {
            'ContentType': content_type,
        }
        
        if metadata:
            extra_args['Metadata'] = metadata
        
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
