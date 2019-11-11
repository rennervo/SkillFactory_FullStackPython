import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()


class Athelete(Base):
    __tablename__ = "athelete"
    id = sa.Column(sa.INTEGER, primary_key=True)
    age = sa.Column(sa.INTEGER)
    birthdate = sa.Column(sa.TEXT)
    gender = sa.Column(sa.TEXT)
    height = sa.Column(sa.REAL)
    weight = sa.Column(sa.INTEGER)
    gold_medals = sa.Column(sa.INTEGER)
    silver_medals = sa.Column(sa.INTEGER)
    bronze_medals = sa.Column(sa.INTEGER)
    total_medals = sa.Column(sa.INTEGER)
    sport = sa.Column(sa.TEXT)
    country = sa.Column(sa.TEXT)


def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


current_session = connect_db()
athletes = current_session.query(Athelete).all()

if __name__ == "__main__":
    # Найдем количество атлетов женского пола
    women = current_session.query(Athelete).filter(Athelete.gender == "Female")
    print("В базе данных найходится {} атлетов женщин".format(women.count()))

    # Найдем количество атлетов старше 30 лет
    moreThen30Years = current_session.query(Athelete).filter(Athelete.age > 30)
    print("В базе данных найходится {} атлетов старше 30 лет".format(moreThen30Years.count()))

    # Найдем количество мужчин старше 30 лет которые получили более 1 золотой медали
    menChampions = current_session.query(Athelete).filter(Athelete.age > 25, Athelete.gender == "Male",
                                                          Athelete.gold_medals > 1)
    print("В базе данных найходится {} мужчин старше 25 лет имеющих 2 и более золотых медалей".format(
        menChampions.count()))