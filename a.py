from sqlalchemy import create_engine,String
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,Session
from sqlalchemy import select

engine=create_engine('sqlite:///test.db',echo=True)

class Base(DeclarativeBase):
    pass
class User(Base):
    __tablename__='users'

    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(30))
    email:Mapped[str]=mapped_column()
    
Base.metadata.create_all(engine)
print('データーベースを作成しました')

with Session(engine) as session:
    
    new_user=User(name='Sato',email='test@test.com')
    session.add(new_user)
    session.commit()

with Session(engine) as session:
    stmt=select(User).where(User.name=='Sato')
    
    user=session.scalars(stmt).first()
    if user:
        print(f'発見　{user.id},{user.name},{user.email}')

with Session(engine) as session:
    # データを取得
    stmt = select(User).where(User.name == "Sato")
    user = session.scalars(stmt).first()
    
    if user:
        # Pythonのオブジェクトの属性を変更するだけ
        user.email = "new_sato@example.com"
        
        # 変更を検知して自動で UPDATE 文が発行される
        session.commit()
with Session(engine) as session:
    stmt = select(User).where(User.name == "Sato")
    user = session.scalars(stmt).first()
    
    if user:
        # 削除リストに追加
        session.delete(user)
        
        # 確定
        session.commit()