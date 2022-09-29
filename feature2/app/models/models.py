from datetime import datetime

import sqlalchemy as db
from sqlalchemy import Integer, String, ForeignKey, DateTime, JSON, Boolean, Date, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from feature2.app.models import phi_enums

Base = declarative_base()
engine = db.create_engine("postgresql://postgres:root@localhost:5432/phy_demo")


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
    user = relationship('User', back_populates='subject_flow_history', uselist=False)
    flow_step = relationship('FlowSteps', uselist=False)


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
    user = relationship("User", back_populates='anonymous', uselist=False)


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


class Subject(Base):
    __tablename__ = 'subject'
    id = db.Column(Integer, primary_key=True)
    subject_id = db.Column(String(10), unique=True)
    user_id = db.Column(Integer, ForeignKey('user.id'), unique=True)
    create_ts = db.Column(DateTime, nullable=False, default=datetime.utcnow)
    change_ts = db.Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    fitbit_is_personal = db.Column(Boolean)
    withings_is_personal = db.Column(Boolean)
    start_date_ideal = db.Column(Date)
    start_date_backup = db.Column(Date)
    dominant_hand = db.Column(Enum(phi_enums.Hand))
    fitbit_hand = db.Column(Enum(phi_enums.Hand))
    bed_shared_with = db.Column(Enum(phi_enums.BedSharedWith))
    age = db.Column(Integer)
    sex = db.Column(Enum(phi_enums.Sex))
    race = db.Column(JSON)
    identity_verified = db.Column(Boolean)
    approved = db.Column(Boolean)
    approved_by = db.Column(UUID, nullable=True)
    progress = db.Column(String(32), nullable=False, index=True)
    fitbit_auth = db.Column(JSON)
    withings_auth = db.Column(JSON)
    is_photo_identify = db.Column(Boolean)
    future_participate = db.Column(Boolean)
    future_participate_step = db.Column(String(32))
    screening_start_ts = db.Column(DateTime)
    start_date_ideal_init = db.Column(Date)
    start_date_backup_init = db.Column(Date)
    shipper_overview_alert_text = db.Column(String(128))
    shipper_overview_alert_create_ts = db.Column(DateTime)
    admin_overview_alert_text = db.Column(String(128))
    admin_overview_alert_create_ts = db.Column(DateTime)
    user = relationship("User", back_populates="subject", uselist=False)
    study_participant = relationship("StudyParticipant", back_populates="subject", uselist=False)


class StudyParticipant(Base):
    __tablename__ = 'study_participant'
    id = db.Column(Integer, primary_key=True)
    create_ts = db.Column(DateTime, nullable=False, default=datetime.utcnow)
    change_ts = db.Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    study_id = db.Column(Integer, ForeignKey('study.id'))
    subject_id = db.Column(Integer, ForeignKey('subject.id'), unique=True)
    kit_id = db.Column(Integer, ForeignKey('kit.id'), unique=True)
    kit = relationship("Kit", back_populates="study_participant", uselist=False)
    date = db.Column(Date, nullable=False)
    date_send = db.Column(Date)
    expected_delivery = db.Column(Date)
    kit_confirm_received = db.Column(Boolean)
    kit_date_received = db.Column(DateTime)
    box_is_good_received = db.Column(Boolean)
    fitbit_sense_received = db.Column(Boolean)
    withings_mat_received = db.Column(Boolean)
    manual_received = db.Column(Boolean)
    return_shipping_slip_received = db.Column(Boolean)
    withings_is_setup = db.Column(Boolean)
    fitbit_is_setup = db.Column(Boolean)
    kit_tracking_number_received = db.Column(String(64))
    kit_tracking_number_returned = db.Column(String(64))
    kit_return_shipper = db.Column(Boolean)
    date_return_shipper = db.Column(Date)
    date_received_shipper = db.Column(Date)
    withings_is_setup_basic = db.Column(Boolean)
    fitbit_is_setup_basic = db.Column(Boolean)
    date_init = db.Column(Date, nullable=True)
    subject = relationship("Subject", back_populates="study_participant", uselist=False)


class User(Base):
    __tablename__ = 'user'
    id = db.Column(Integer, primary_key=True)
    sub = db.Column(UUID, unique=True)
    create_ts = db.Column(DateTime, nullable=False, default=datetime.utcnow)
    change_ts = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_activity = db.Column(DateTime)
    timezone = db.Column(Enum(phi_enums.TypeTimeZone), default=phi_enums.TypeTimeZone.EASTERN_TZ)
    subject = relationship("Subject", back_populates='user', foreign_keys="[Subject.user_id]", uselist=False)
    subject_flow_history = relationship("SubjectFlowHistory", back_populates='user', uselist=True)
    anonymous = relationship("Anonymous", back_populates='user', uselist=False)


class Chat(Base):
    __tablename__ = 'chat'
    id = db.Column(Integer, primary_key=True)
    create_ts = db.Column(DateTime, nullable=False, default=datetime.utcnow)
    user_sub = db.Column(UUID, unique=True)
    user_email = db.Column(String(256))
    chat_satisfied = db.Column(Boolean)
    chat_satisfied_ts = db.Column(DateTime)
    chat_read_by_concierge = db.Column(Boolean)
    chat_read_by_subject = db.Column(Boolean)
    unread_messages_to_user_count = db.Column(Integer, default=0)


class Kit(Base):
    __tablename__ = 'kit'
    id = db.Column(Integer, primary_key=True)
    batch_id = db.Column(Integer, ForeignKey('batch.id'), nullable=True)
    change_ts = db.Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    create_ts = db.Column(DateTime, nullable=False, default=datetime.utcnow)
    email = db.Column(String, unique=True)
    name = db.Column(String, nullable=False, unique=True)
    email_password = db.Column(String)
    status = db.Column(Enum(phi_enums.KitStatus, create_constraint=True, validate_strings=True))
    status_change_ts = db.Column(DateTime, nullable=False)
    study_participant = relationship('StudyParticipant', back_populates='kit', uselist=False)
    fitbit_device_asset_tag = db.Column(String)
    withings_device_asset_tag = db.Column(String)
    fitbit_device_password = db.Column(String)
    withings_device_password = db.Column(String)
    mail_uncofirmed_receipt_kit = db.Column(Boolean, default=False)
    mail_uncofirmed_receipt_kit_ts = db.Column(DateTime, nullable=True)
    mail_notify_kit_arrival = db.Column(Boolean, default=False)
    mail_notify_kit_arrival_ts = db.Column(DateTime, nullable=True)
