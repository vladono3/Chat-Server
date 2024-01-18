from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from storage.models import User, Discussion, Message, Base

engine = create_engine('postgresql://postgres:cristi1971@localhost:5432/chat_app_db', echo=True)

with engine.connect() as connection:
    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(engine)


class DataBase:
    @staticmethod
    def get_users():
        users = session.query(User).all()
        return User.users_dict(users)

    @staticmethod
    def get_discussions():
        discussions = session.query(Discussion).all()
        return Discussion.discussions_dict(discussions)

    @staticmethod
    def get_messages():
        messages = session.query(Message).all()
        return Message.messages_dict(messages)

    @staticmethod
    def create_user(name, password, user_id):
        obj = User(name=name, password=password, id=user_id)
        session.add(obj)
        session.commit()
        return obj

    @staticmethod
    def create_discussion(contacts, discussion_id):
        obj = Discussion(contacts=contacts, id=discussion_id)
        session.add(obj)
        session.commit()
        return obj

    @staticmethod
    def create_message(message_id, discussion_id, user_id, created_at, value, name):
        obj = Message(id=message_id, discussion_id=discussion_id, user_id=user_id, created_at=created_at, value=value,
                      name=name)
        session.add(obj)
        session.commit()
        return obj


db = DataBase()
