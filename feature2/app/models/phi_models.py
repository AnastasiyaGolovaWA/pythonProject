from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (JSON, Boolean, Column, Date, DateTime, Enum, Integer,
                        String)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql.schema import ForeignKey

from . import phi_enums

Base = declarative_base()
db = SQLAlchemy()


class Anonymous(db.Model):
    id = Column(Integer, primary_key=True)
    create_ts = Column(DateTime, nullable=False, default=datetime.utcnow)
    pre_screening = Column(JSON)  # future participate can get from pre screening
    anonymous_id = Column(UUID, unique=True)  # uuid from RudderStack
    user_id = Column(Integer, ForeignKey('user.id'), unique=True)  # add after linking
    active = Column(Boolean)  # for subject flow inactivate button (also no notifications for inactivated users)
    email = Column(String(1024))  # if ask question not login user or subscribe news
    future_participate_consent = Column(Boolean)  # future participate from inform consent

    current_subject_flow_step_id = Column(Integer, ForeignKey('flow_steps.id'), nullable=True)
    subject_flow_alert_text = Column(String(128))
    subject_flow_alert_create_ts = Column(DateTime, nullable=True)

    user = relationship("User", back_populates='anonymous', uselist=False)


class SubjectFlowHistory(db.Model):
    anonymous_id = Column(String(128), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    event_name = Column(String(64), ForeignKey('flow_steps.event_name'), primary_key=True)
    timestamp = Column(DateTime(timezone=True), nullable=False)

    user = relationship('User', back_populates='subject_flow_history', uselist=False)
    flow_step = relationship('FlowSteps', uselist=False)


class FlowSteps(db.Model):
    id = Column(Integer, primary_key=True)
    subject_status = Column(String(64))
    detailed_view = Column(String(256))
    simple_view = Column(String(64))
    color = Column(String(8))
    event_name = Column(String(64), index=True, unique=True)
    code = Column(String(4), nullable=True)


class QualityControl(db.Model):
    id = Column(Integer, primary_key=True)
    study_participant_id = Column(Integer, ForeignKey('study_participant.id'))
    date = Column(Date, nullable=False)  # date series_to.date()
    stream = Column(Enum(phi_enums.DataType), nullable=False)
    type = Column(Enum(phi_enums.SourceType), nullable=False)
    series_from = Column(DateTime(timezone=True), nullable=True)
    series_to = Column(DateTime(timezone=True), nullable=True)
    duration = Column(Integer, nullable=True)
    status = Column(Enum(phi_enums.QCStatus), nullable=False)
    change_ts = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    ingestion_ts = Column(DateTime, nullable=True)
    processing_ts = Column(DateTime, nullable=True)
