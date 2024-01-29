import datetime
import uuid

from sqlalchemy import Column, String, ARRAY, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()
ENGINE = create_engine('postgresql://postgres:cristi1971@localhost:5432/chat_app_db', echo=True)


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)

    @staticmethod
    def users_dict(users):
        users_dict = {}
        for user in users:
            users_dict[str(user.id)] = {
                "id": str(user.id),
                "name": str(user.name),
                "password": str(user.password)
            }
        return users_dict


class Discussion(Base):
    __tablename__ = "discussions"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    contacts = Column(ARRAY(UUID(as_uuid=True)), nullable=False)
    name = Column(String)  # Add a new column for the name

    @staticmethod
    def discussions_dict(discussions):
        discussions_dict = {}
        for discussion in discussions:
            serialized_contacts = [str(contact) for contact in discussion.contacts]
            discussions_dict[str(discussion.id)] = {
                "id": str(discussion.id),
                "contacts": serialized_contacts,
                "name": discussion.name  # Include the name in the serialized dictionary
            }
        return discussions_dict


class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    discussion_id = Column(UUID(as_uuid=True), ForeignKey("discussions.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    value = Column(String, nullable=False)
    name = Column(String, nullable=False)

    @staticmethod
    def messages_dict(messages):
        messages_dict = {}
        for message in messages:
            messages_dict[str(message.id)] = {
                "id": str(message.id),
                "created_at": str(message.created_at),
                "discussion_id": str(message.discussion_id),
                "user_id": str(message.user_id),
                "value": str(message.value),
                "name": str(message.name)
            }
        return messages_dict
