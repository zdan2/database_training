from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# ① Engine（SQLiteファイルを作る）
engine = create_engine("sqlite:///app.db", echo=False)

# ② Base（ORMモデルの土台）
class Base(DeclarativeBase):
    pass

# ③ Session（作業机）
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
