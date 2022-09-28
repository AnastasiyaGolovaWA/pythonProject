import pandas
import sqlalchemy as db

from feature2.app.models.models import FlowSteps, engine, SubjectFlowHistory, Anonymous, QualityControl


def converter():
    quality_control = pandas.read_sql_query(
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

    print("QUALITY CONTROL")
    print()
    print(quality_control)

    subject_flow_history = pandas.read_sql_query(
        sql=db.select([SubjectFlowHistory.anonymous_id,
                       SubjectFlowHistory.user_id,
                       SubjectFlowHistory.event_name,
                       SubjectFlowHistory.timestamp
                       ]),
        con=engine
    )

    print("SUBJECT FLOW HISTORY")
    print()
    print(subject_flow_history)

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

    print("ANONYMOUS")
    print()
    print(anonymous)

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

    print("QUALITY CONTROL")
    print()
    print(quality_control)


if __name__ == '__main__':
    converter()
