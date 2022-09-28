import pandas
import sqlalchemy as db

from feature2.app.models.models import FlowSteps, engine, SubjectFlowHistory


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


if __name__ == '__main__':
    converter()
