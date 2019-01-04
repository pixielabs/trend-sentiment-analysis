from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Entity(Base):
    __tablename__ = 'entities'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    type = Column(Integer)
    wikipedia_url = Column(String(255))
    mid = Column(String(255))
    salience = Column(Float)
    sentiment_score = Column(Float)
    sentiment_magnitude = Column(Float)
    posted_at = Column(Integer)
    remote_post_id = Column(String(255))


class Mention(Base):
    __tablename__ = 'mentions'

    id = Column(Integer, primary_key=True)
    entity_id = Column(Integer, ForeignKey('entities.id'))
    content = Column(String(255))
    begin_offset = Column(Integer)
    type = Column(Integer)
    sentiment_score = Column(Float)
    sentiment_magnitude = Column(Float)

    entity = relationship("Entity", back_populates="mentions")

Entity.mentions = relationship(
    "Mention", order_by=Mention.id, back_populates="entity")
