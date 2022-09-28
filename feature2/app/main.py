from sqlalchemy import Integer, String


def converter():
    import pandas
    import sqlalchemy as db
    from sqlalchemy.ext.declarative import declarative_base

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

    df = pandas.read_sql_query(
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

    print("Type:", type(df))
    print()
    print(df)


if __name__ == '__main__':
    converter()
