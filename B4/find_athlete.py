from datetime import datetime

from B4.sql import connect_db, Athelete
from B4.users import User


def find_user(id, session):
    user = session.query(User).filter(User.id == id).first()
    if user is not None:
        print("Пользователь с ID {} найден".format(user.id))
    else:
        print("Пользователя с указанным ID нет в базе данных")
    return user


def find_closest_value(user, athletes):
    birthdate_athlete = None
    height_athlete = None
    current_value = 0
    for athlete in athletes:
        if birthdate_athlete is None:
            birthdate_athlete = athlete
            current_value = get_timestamp(athlete.birthdate)
        elif abs(get_timestamp(user.birthdate) - get_timestamp(athlete.birthdate)) < abs(
                get_timestamp(user.birthdate) - current_value):
            birthdate_athlete = athlete
            current_value = get_timestamp(athlete.birthdate)
    current_value = 0
    for athlete in athletes:
        if athlete.height is not None:
            if height_athlete is None:
                height_athlete = athlete
                current_value = athlete.height
            elif abs(user.height - athlete.height) < abs(user.height - current_value):
                height_athlete = athlete
                current_value = athlete.height
    return birthdate_athlete, height_athlete


def get_timestamp(value):
    time = datetime.strptime(value, "%Y-%m-%d")
    return time


def main():
    session = connect_db()
    id = input("Введите id пользователя: ")
    user = find_user(id, session)
    if user is not None:
        athletes = session.query(Athelete).all()
        bd_athlete, height_athlete = find_closest_value(user, athletes)
        print(
            "Пользователь с идентификатором {} родился {} и имеет рост {}".format(user.id, user.birthdate, user.height))
        print("Ближайший атлет по дате рождения имеет ID {}. Атлет родился {}".format(bd_athlete.id,
                                                                                      bd_athlete.birthdate))
        print("Ближайший атлет по росту имеет ID {}. Рост атлета {}".format(height_athlete.id, height_athlete.height))


if __name__ == "__main__":
    main()
