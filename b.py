from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, sessionmaker
from pydantic import BaseModel, ConfigDict

# ==========================================
# 1. データベース設定 (SQLAlchemy)
# ==========================================
DATABASE_URL = "sqlite:///./sql_app.db"

# connect_argsはSQLite固有の設定（マルチスレッド対策）
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)

# セッションを作る工場（リクエストのたびにここからセッションを作る）
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# ==========================================
# 2. データベースのモデル (SQLAlchemy)
#    -> DBテーブルの設計図
# ==========================================
class UserDB(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)

# データベースとテーブルを作成
Base.metadata.create_all(bind=engine)

# ==========================================
# 3. APIのデータ形式 (Pydantic)
#    -> 入出力のチェック用
# ==========================================

# ユーザーを作成するときに受け取るデータ
class UserCreate(BaseModel):
    name: str
    email: str

# ユーザー情報を返すときのデータ形式
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    
    # 【超重要】ORM(SQLAlchemy)のオブジェクトをPydanticモデルに変換する設定
    # これがないとエラーになります (Pydantic v2の書き方)
    model_config = ConfigDict(from_attributes=True)