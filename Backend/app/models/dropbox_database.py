"""
Dropbox model for database additions
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DropboxAccount(Base):
    __tablename__ = 'dropbox_accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dropbox_user_id = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=False)

    # Foreign key constraint to the users table
    local_user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))

    def __repr__(self):
        return f"<DropboxAccount(id={self.id}, dropbox_user_id={self.dropbox_user_id}, name={self.name}, refresh_token={self.refresh_token})>"
