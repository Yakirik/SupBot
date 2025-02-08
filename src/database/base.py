from sqlalchemy.ext.asyncio import  async_sessionmaker, create_async_engine, AsyncSession
import os
from dotenv import load_dotenv

def get_db_session():
    load_dotenv()
    engine = create_async_engine(url=os.getenv('SQLALCHEMY_URL'))
    async_session = async_sessionmaker(engine, class_=AsyncSession)
    return async_session


