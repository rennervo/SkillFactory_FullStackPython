import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from B4.sql import connect_db

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True)
    first_name = sa.Column(sa.TEXT)
    last_name = sa.Column(sa.TEXT)
    gender = sa.Column(sa.TEXT)
    email = sa.Column(sa.TEXT)
    birthdate = sa.Column(sa.TEXT)
    height = sa.Column(sa.REAL)


def get_gender():
    text = input("Укажите пол. 'М' - мужской, 'Ж' - женский: ")
    if text.lower() == "м":
        return str("Male")
    elif text.lower() == "ж":
        return str("Male")
    else:
        print("Вы ввели неверное значение. Введите или 'М' или 'Ж'")
        get_gender()


def get_email():
    email = input("Введите email: ")
    if email.count("@") == 1:
        if "." in email.split("@")[1]:
            return str(email)
        else:
            print("Введенный email некорректный. Убедитесь что в доменной части есть точка")
            get_email()
    else:
        print("Введенный email некорректный. Убедитесь что в адресе одна @")
        get_email()


def request_data():
    print("Здравствуйте, введите данные нового пользователя")
    first_name = input("Введите имя: ")
    last_name = input("Введите фамилию: ")
    gender = get_gender()
    email = get_email()
    birthdate = input("Введите дату рождения (формат YYYY-MM-DD): ")
    height = input("Введите рост (формат Х.ХХ): ")
    user = User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height
    )
    return user


def get_id_last_user(session):
    last_user = session.query(User).all().last()
    return last_user.id

def main():
    session = connect_db()
    user = request_data()
    session.add(user)
    session.commit()
    print("Пользователь успешно добавлен в БД. ID нового пользователя {}".format(user.id))


if __name__ == "__main__":
    main()
