import datetime
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import Column, Integer, String

#https://github.com/johnwheeler/flask-ask/issues/4
#from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
import psycopg2

DeclarativeBase = declarative_base()

class Authentication:
    #session.user.userId
    @staticmethod
    def get_token(self, uid):
        if uid:
            engine = create_engine(
                "postgresql+psycopg2://root:Idolikeevian@auction.cbmefdfxkvkf.us-east-1.rds.amazonaws.com:5432/django"
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
    #    auth.post_token(d['name'], d['email'], d['user_id'])
    def post_token(name, email, uid):
        engine = create_engine(
            "postgresql+psycopg2://root:Idolikeevian@auction.cbmefdfxkvkf.us-east-1.rds.amazonaws.com:5432/auction"
        )#this will timeout if you have the wrong database name in login
        #needs aws execution role for postgres
        DeclarativeBase.metadata.create_all(engine)


        #Base.prepare(engine, reflect=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        #this is a black box

        stmt = insert(my_table).values(name=name, email=email, uid=uid)
        stmt = stmt.on_conflict_do_nothing()
        

        session.execute(stmt)
        session.close()
     


if __name__ == '__main__':
    a = Authentication()
    #print(a.get_token(1))
    engine = create_engine(
        "postgresql+psycopg2://root:Idolikeevian@auction.cbmefdfxkvkf.us-east-1.rds.amazonaws.com:5432/auction"
    )
    DeclarativeBase.metadata.create_all(engine)



class User(DeclarativeBase):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    uid = Column(String)

    def __repr__(self):
        return "<User(name='%s', email='%s', uid='%s')>" % (
                                self.name, self.email, self.uid)
