from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, LargeBinary, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class State(Base):
    __tablename__ = 'state'

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    title = Column(String)
    screenshot = Column(LargeBinary)
    date = Column(DateTime)
    console = Column(String)
    has_bug = Column(Boolean)
    http_requests = Column(String)
    state_hash = Column(String)
    request_count = Column(Integer)

    def __init__(self, url, title, screenshot, console, has_bug, http_requests, state_hash, req_count, id=None):
        self.id = id
        self.state_hash = state_hash
        self.url = url
        self.title = title
        self.screenshot = screenshot
        self.console = console
        self.has_bug = has_bug
        self.http_requests = http_requests
        self.http_requests = req_count

    def as_dict(self):
        return {c.name: getattr(self, c.name) if type(getattr(self, c.name)) != bytes else\
               getattr(self, c.name).decode('utf-8') for c in self.__table__.columns}

class Element(Base):
    __tablename__ = 'element'

    id = Column(Integer, primary_key=True)
    state_id = Column(Integer, ForeignKey('state.id'))
    state = relationship(State)
    text = Column(String)
    width = Column(Integer)
    height = Column(Integer)
    location_x = Column(Integer)
    location_y = Column(Integer)
    screenshot = Column(LargeBinary)
    innerHTML = Column(String)


class Transition(Base):
    __tablename__ = 'transition'

    id = Column(Integer, primary_key=True)
    state_from_id = Column(Integer, ForeignKey('state.id'))
    state_to_id = Column(Integer, ForeignKey('state.id'))
    element_id = Column(Integer, ForeignKey('element.id'))
    state_from = relationship(State, foreign_keys=[state_from_id])
    state_to = relationship(State, foreign_keys=[state_to_id])
    element = relationship(Element)
    action = Column(String)

    def __init__(self, state_from_id, state_to_id, action):
        self.state_from_id = state_from_id
        self.state_to_id = state_to_id
        self.action = action

    def as_dict(self):
        return {c.name: getattr(self, c.name) if type(getattr(self, c.name)) != bytes else\
               getattr(self, c.name).decode('utf-8') for c in self.__table__.columns}

class Bot(Base):
    __tablename__ = 'bot'

    id = Column(Integer, primary_key=True)
    state_id = Column(Integer)
    start_time = Column(Integer)
    states_count = Column(Integer)
    bugs_count = Column(Integer)

    def __init__(self, start_time, states_count, bugs_count, id=None, state_id=None):
        self.id = id;
        self.state_id = state_id;
        self.start_time = start_time;
        self.states_count = states_count;
        self.bugs_count = bugs_count;

if __name__ == '__main__':
    engine = create_engine('sqlite:///network.db')
    Base.metadata.create_all(engine)
