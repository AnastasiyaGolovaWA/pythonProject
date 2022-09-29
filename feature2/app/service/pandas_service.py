import pandas
import sqlalchemy as db

from feature2.app.models.models import FlowSteps, engine, SubjectFlowHistory, Anonymous, QualityControl, Subject, \
    StudyParticipant, Kit, User, Chat


def get_flow_steps():
    flow_steps = pandas.read_sql_query(
        sql=db.select([FlowSteps.id,
                       FlowSteps.subject_status,
                       FlowSteps.detailed_view,
                       FlowSteps.simple_view,
                       FlowSteps.color,
                       FlowSteps.event_name,
                       FlowSteps.code
                       ]),
        con=engine
    )
    return flow_steps


def get_subject_flow_history():
    subject_flow_history = pandas.read_sql_query(
        sql=db.select([SubjectFlowHistory.anonymous_id,
                       SubjectFlowHistory.user_id,
                       SubjectFlowHistory.event_name,
                       SubjectFlowHistory.timestamp
                       ]),
        con=engine
    )
    return subject_flow_history


def get_ids():
    query = db.select(Subject.subject_id, Subject.id.label('subject_integer_id'),
                      StudyParticipant.id.label('study_participant_id'),
                      StudyParticipant.date.label('study_start_date'), User.id.label('user_id'),
                      User.sub.label('user_sub'), Anonymous.anonymous_id, Anonymous.email, Chat.id.label('chat_id'),
                      Kit.name.label('kit_name')).filter(
        Subject.id == StudyParticipant.subject_id).filter(User.id == Subject.user_id).filter(
        Anonymous.user_id == User.id).filter(Chat.user_sub == User.sub).filter(Kit.id == StudyParticipant.kit_id)
    ids = pandas.read_sql_query(
        sql=query,
        con=engine
    )
    return ids


def get_anonymous():
    anonymous = pandas.read_sql_query(
        sql=db.select([Anonymous.id,
                       Anonymous.create_ts,
                       Anonymous.pre_screening,
                       Anonymous.anonymous_id,
                       Anonymous.user_id,
                       Anonymous.active,
                       Anonymous.email,
                       Anonymous.future_participate_consent,
                       Anonymous.current_subject_flow_step_id,
                       Anonymous.subject_flow_alert_text,
                       Anonymous.subject_flow_alert_create_ts
                       ]),
        con=engine
    )
    return anonymous


def get_quality_control():
    quality_control = pandas.read_sql_query(
        sql=db.select([QualityControl.id,
                       QualityControl.study_participant_id,
                       QualityControl.date,
                       QualityControl.stream,
                       QualityControl.type,
                       QualityControl.series_from,
                       QualityControl.series_to,
                       QualityControl.duration,
                       QualityControl.status,
                       QualityControl.change_ts,
                       QualityControl.ingestion_ts,
                       QualityControl.processing_ts
                       ]),
        con=engine
    )
    return quality_control
