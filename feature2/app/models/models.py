import sqlalchemy as db
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
engine = db.create_engine("postgresql://postgres:root@localhost:5432/BackEnd")


class FlowSteps(Base):
    __tablename__ = 'flow_steps'
    id = db.Column(Integer, primary_key=True)
    subject_status = db.Column(String(64))
    detailed_view = db.Column(String(256))
    simple_view = db.Column(String(64))
    color = db.Column(String(8))
    event_name = db.Column(String(64), index=True, unique=True)
    code = db.Column(String(4), nullable=True)


class SubjectFlowHistory(Base):
    __tablename__ = 'subject_flow_history'
    anonymous_id = db.Column(String(128), primary_key=True)
    user_id = db.Column(Integer, ForeignKey('user.id'), nullable=True)
    event_name = db.Column(String(64), ForeignKey('flow_steps.event_name'), primary_key=True)
    timestamp = db.Column(DateTime(timezone=True), nullable=False)

