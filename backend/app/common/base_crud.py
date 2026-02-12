from typing import TypeVar, Generic, Type, Optional, List, Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_
from sqlalchemy.orm import DeclarativeMeta
from pydantic import BaseModel
from datetime import datetime

ModelType = TypeVar("ModelType", bound=DeclarativeMeta)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    async def create(
        self, 
        db: AsyncSession, 
        obj_in: CreateSchemaType
    ) -> ModelType:
        """생성"""
        obj_data = obj_in.model_dump(exclude_unset=True)
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj
    
    async def get(
        self, 
        db: AsyncSession, 
        id: int
    ) -> Optional[ModelType]:
        """단건 조회"""
        # status 컬럼이 있는 경우만 필터링
        if hasattr(self.model, 'status'):
            stmt = select(self.model).where(
                and_(
                    self.model.id == id,
                    self.model.status != 'D'
                )
            )
        else:
            stmt = select(self.model).where(self.model.id == id)
        
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_multi(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ModelType]:
        """다건 조회"""
        if hasattr(self.model, 'status'):
            stmt = select(self.model).where(self.model.status != 'D')
        else:
            stmt = select(self.model)
        
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key):
                    stmt = stmt.where(getattr(self.model, key) == value)
        
        stmt = stmt.offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()
    
    async def update(
        self,
        db: AsyncSession,
        id: int,
        obj_in: UpdateSchemaType
    ) -> Optional[ModelType]:
        """업데이트"""
        db_obj = await self.get(db, id)
        if not db_obj:
            return None
        
        update_data = obj_in.model_dump(exclude_unset=True)
        if hasattr(self.model, 'updated_at'):
            update_data['updated_at'] = datetime.utcnow()
        
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**update_data)
        )
        await db.execute(stmt)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj
    
    async def delete(
        self,
        db: AsyncSession,
        id: int
    ) -> bool:
        """삭제 (status='D')"""
        if not hasattr(self.model, 'status'):
            return False
        
        update_data = {'status': 'D'}
        if hasattr(self.model, 'updated_at'):
            update_data['updated_at'] = datetime.utcnow()
        
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**update_data)
        )
        result = await db.execute(stmt)
        return result.rowcount > 0
    
    async def count(
        self,
        db: AsyncSession,
        filters: Optional[Dict[str, Any]] = None
    ) -> int:
        """카운트"""
        from sqlalchemy import func
        
        if hasattr(self.model, 'status'):
            stmt = select(func.count()).select_from(self.model).where(
                self.model.status != 'D'
            )
        else:
            stmt = select(func.count()).select_from(self.model)
        
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key):
                    stmt = stmt.where(getattr(self.model, key) == value)
        
        result = await db.execute(stmt)
        return result.scalar()
