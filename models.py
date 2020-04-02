from database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import backref, relationship


class Ship(Base):
    __tablename__ = 'ship'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    date_added =  Column(DateTime, default=func.now())

class Rank(Base):
    __tablename__ = 'rank'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    date_added = Column(DateTime, default=func.now())


class Race(Base):
    __tablename__ = 'race'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    date_added = Column(DateTime, default=func.now())


class Crew(Base):
    __tablename__ = 'crew'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    ship_id = Column(Integer, ForeignKey('ship.id'))
    race_id = Column(Integer, ForeignKey('race.id'))
    rank_id = Column(Integer, ForeignKey('rank.id'))
    date_added = Column(DateTime, default=func.now())
    ship = relationship(
        Ship,
        backref=backref('ships',
                        uselist=True,
                        cascade='delete, all'))
    race = relationship(
        Race,
        backref=backref('races',
                        uselist=True,
                        cascade='delete, all'))
    rank = relationship(
        Rank,
        backref=backref('ranks',
                        uselist=True,
                        cascade='delete, all'))
