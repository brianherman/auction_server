import datetime
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

#https://github.com/johnwheeler/flask-ask/issues/4
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
import psycopg2

class Authentication:
    #session.user.userId
    def get_token(self, uid):
        if uid:
            engine = create_engine(
                "postgresql+psycopg2://django:herman69@ebay.cbmefdfxkvkf.us-east-1.rds.amazonaws.com:5432/django"
            )
            Base = automap_base()

            Base.prepare(engine, reflect=True)
            Session = sessionmaker(bind=engine)

            # create a Session
            session = Session()
            try:
                result = session.query(User).filter_by(uid=uid).one()
                return result['token']
            except Exception as e:
                import traceback
                traceback.print_exc()
                return {'error': 'Multiple login tokens.'}
        else:
            return {'error': 'Null Token.'}
    @staticmethod
    def post_token(uid, token):
        engine = create_engine(
            "postgresql+psycopg2://django:herman69@ebay.cbmefdfxkvkf.us-east-1.rds.amazonaws.com:5432/django"
        )
        Base = automap_base()

        Base.prepare(engine, reflect=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        #this is a black box
        #stmt = insert(my_table).values(id=uid, data=)
        #stmt = stmt.on_conflict_do_nothing()
        #conn.execute(stmt)
    


if __name__ == '__main__':
    a = Authentication()
    print(a.get_token(1))