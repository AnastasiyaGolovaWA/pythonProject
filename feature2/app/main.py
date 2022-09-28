import pandas
import sqlalchemy as db

from feature2.app.models.models import FlowSteps, engine


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


if __name__ == '__main__':
    converter()
