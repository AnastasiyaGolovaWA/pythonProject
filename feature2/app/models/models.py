from datetime import datetime

import sqlalchemy as db
from sqlalchemy import Integer, String, ForeignKey, DateTime, JSON, Boolean, Date, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

from feature2.app.models import phi_enums

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


class Anonymous(Base):
    __tablename__ = 'anonymous'
    id = db.Column(Integer, primary_key=True)
    create_ts = db.Column(DateTime, nullable=False, default=datetime.utcnow)
    pre_screening = db.Column(JSON)
    anonymous_id = db.Column(UUID, unique=True)
    user_id = db.Column(Integer, ForeignKey('user.id'), unique=True)
    active = db.Column(Boolean)
    email = db.Column(String(1024))
    future_participate_consent = db.Column(Boolean)
    current_subject_flow_step_id = db.Column(Integer, ForeignKey('flow_steps.id'), nullable=True)
    subject_flow_alert_text = db.Column(String(128))
    subject_flow_alert_create_ts = db.Column(DateTime, nullable=True)


class QualityControl(Base):
    __tablename__ = 'quality_control'
    id = db.Column(Integer, primary_key=True)
    study_participant_id = db.Column(Integer, ForeignKey('study_participant.id'))
    date = db.Column(Date, nullable=False)
    stream = db.Column(Enum(phi_enums.DataType), nullable=False)
    type = db.Column(Enum(phi_enums.SourceType), nullable=False)
    series_from = db.Column(DateTime(timezone=True), nullable=True)
    series_to = db.Column(DateTime(timezone=True), nullable=True)
    duration = db.Column(Integer, nullable=True)
    status = db.Column(Enum(phi_enums.QCStatus), nullable=False)
    change_ts = db.Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    ingestion_ts = db.Column(DateTime, nullable=True)
    processing_ts = db.Column(DateTime, nullable=True)