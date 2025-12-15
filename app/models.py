from datetime import datetime
from sqlalchemy import Integer, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base

class Nursery(Base):
    __tablename__ = "nurseries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # DB用
    source_id: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=False)  # スプシのid

    name: Mapped[str] = mapped_column(String(200), nullable=False)  # 保育園名
    postal_code: Mapped[str | None] = mapped_column(String(8))      # 194-0211
    address: Mapped[str | None] = mapped_column(Text)               # 相原町3338-1
    phone: Mapped[str | None] = mapped_column(String(30))           # 042-...
    other_services: Mapped[str | None] = mapped_column(Text)        # その他の事業内容（複数行のまま保存OK）
    homepage_url: Mapped[str | None] = mapped_column(Text)
    guidebook_url: Mapped[str | None] = mapped_column(Text)

    imported_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
