from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    company = Column(String)
    manager_id = Column(Integer, ForeignKey('users.id'))
    
    def __repr__(self):
        return f"<User(id={self.id}, name={self.first_name} {self.last_name}, company={self.company})>"

class AccessEvent(Base):
    __tablename__ = 'access'
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('users.id'))
    gate_id = Column(Integer)
    direction = Column(String)
    timestamp = Column(DateTime)
    
    person = relationship("User", back_populates="access_events")
    
User.access_events = relationship("AccessEvent", order_by=AccessEvent.id, back_populates="person")

def init_db():
    engine = create_engine('sqlite:///access_monitoring.db')
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)

Session = init_db()