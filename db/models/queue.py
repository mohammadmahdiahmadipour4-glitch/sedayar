from sqlalchemy import Column  , Integer , String , DateTime , Boolean 
from datetime import datetime
from db.base import Base


class UpdateQueue(Base): 
    __tablename__ = "update_queue"
    
    id = Column(Integer, primary_key=True)
    update_json = Column(String,  nullable=False)
    is_processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)