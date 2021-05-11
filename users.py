import time
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from find_athlete import find_athlete 

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

class User(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'user'

    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True, autoincrement = True)
    # имя пользователя
    first_name = sa.Column(sa.Text)
    # фамилия пользователя
    last_name = sa.Column(sa.Text)
    #пол
    gender = sa.Column(sa.Text)
    # адрес электронной почты пользователя
    email = sa.Column(sa.Text)
    #рост
    height = sa.Column(sa.Float)
    #дата рождения
    birthdate = sa.Column(sa.Date)

class Athelete(Base):
    """
    Описывает структуру таблицы Athelete для хранения данных об атлетах
    """
    # задаем название таблицы
    __tablename__ = 'athelete'
     # идентификатор спортсмена, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True, autoincrement = True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa. Column(sa.Float)
    name = sa.Column(sa.Text)
    weight = sa.Column(sa.Integer)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()

def request_data():
    """
    Запрашивает у пользователя данные и добавляет их в список users
    """
    # выводим приветствие
    print("Привет! Я запишу твои данные!")
    # запрашиваем у пользователя данные
    first_name = input("Введи своё имя: ")
    last_name = input("А теперь фамилию: ")
    gender = input("Твой пол: Female или Male ")
    email = input("Мне еще понадобится адрес твоей электронной почты: ")
    height = input("И рост (например 1.77):")
    birthdate = input("Дату рождения в формате yyyy-mm-dd:")
    
    # создаем нового пользователя
    user = User(
        first_name=first_name,
        last_name=last_name,
        gender= gender,
        email=email,
        height= height,
        birthdate =datetime.strptime(birthdate, "%Y-%m-%d")
    )
    # возвращаем созданного пользователя
    return user
		
def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    # просим пользователя выбрать режим
    mode = input("Выбери режим.\n1 - найти атлета\n2 - ввести данные нового пользователя\n")
    # проверяем режим
    if mode == "1":
        # выбран режим поиска, запускаем его
        id_ = input("Введи id пользователя для поиска: ")
        # вызываем печать результатов работы функции поиска по дате рождения и росту
       	if find_athlete(id_, session, User, Athelete)  is not None:
       		print("Имена атлетов с подходящим ДР и ростом", find_athlete(id_, session, User, Athelete))
       	
    elif mode == "2":
        # запрашиваем данные пользователя
        user = request_data()
        # добавляем нового пользователя в сессию
        session.add(user)
        # сохраняем все изменения, накопленные в сессии
        session.commit()
        print("Спасибо, данные сохранены!")
    else:
        print("Некорректный режим:(")


if __name__ == "__main__":
    main()        