from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from app.db.models import Base

from app.db.models import Receipt, Team, User


class DatabaseManager:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_async_engine(
            self.database_url, echo=True,
            future=True
        )
        self.AsyncSession = sessionmaker(
            self.engine, expire_on_commit=False,
            class_=AsyncSession
        )

    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def close(self):
        await self.engine.dispose()

    async def get_session(self) -> AsyncSession:
        async with self.AsyncSession() as session:
            return session

    async def execute_raw_query(self, query: str):
        async with self.engine.connect() as connection:
            try:
                result = await connection.execute(text(query))
                return result.fetchall()
            finally:
                await connection.close()


    async def create_receipt(
        self,
        session: AsyncSession,
        team_id: int,
        user_id: int,
        date: datetime,
        amount: Decimal,
        operation_number: str,
        sender: str,
        receiver: str,
        status: str,
        file_path: str,
        notes: Optional[str] = None,
        organization: Optional[str] = None,
        fee: Optional[Decimal] = None
    ) -> Receipt:
        """Create a new receipt record."""
        receipt = Receipt(
            team_id=team_id,
            uploaded_by=user_id,
            date=date,
            amount=amount,
            operation_number=operation_number,
            sender=sender,
            receiver=receiver,
            status=status,
            file_path=file_path,
            notes=notes,
            organization=organization,
            fee=fee
        )
        try:
            session.add(receipt)
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        await session.refresh(receipt)
        return receipt

    async def get_team_receipts(
            self,
            session: AsyncSession,
            team_id: int,
            start_date: datetime,
            end_date: datetime
    ) -> List[Receipt]:
        """Get team receipts within date range."""
        query = select(Receipt).where(
            Receipt.team_id == team_id,
            Receipt.date >= start_date,
            Receipt.date <= end_date
        )
        result = await session.execute(query)
        return result.scalars().all()

    async def update_receipt(
            self,
            session: AsyncSession,
            receipt_id: int,
            **kwargs
    ) -> Optional[Receipt]:
        """Update receipt details."""
        query = select(Receipt).where(Receipt.id == receipt_id)
        result = await session.execute(query)
        receipt = result.scalar_one_or_none()

        if receipt:
            for key, value in kwargs.items():
                if hasattr(receipt, key):
                    setattr(receipt, key, value)
            await session.commit()
            await session.refresh(receipt)

        return receipt

    async def get_receipt(
            self,
            session: AsyncSession,
            receipt_id: int
    ) -> Optional[Receipt]:
        """Get receipt by ID."""
        query = select(Receipt).where(Receipt.id == receipt_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def delete_receipt(
            self,
            session: AsyncSession,
            receipt_id: int
    ) -> bool:
        """Delete a receipt."""
        query = select(Receipt).where(Receipt.id == receipt_id)
        result = await session.execute(query)
        receipt = result.scalar_one_or_none()

        if receipt:
            await session.delete(receipt)
            try:
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            return True
        return False

    async def get_team_receipts_summary(
            self,
            session: AsyncSession,
            team_id: int,
            start_date: datetime,
            end_date: datetime
    ) -> dict:
        """Get summary of team receipts."""
        receipts = await self.get_team_receipts(session, team_id, start_date,
                                                end_date)

        total_amount = sum(float(r.amount) for r in receipts)
        total_fee = sum(float(r.fee or 0) for r in receipts)

        return {
            "total_receipts": len(receipts),
            "total_amount": total_amount,
            "total_fee": total_fee,
            "date_range": {
                "start": start_date,
                "end": end_date
            }
        }
