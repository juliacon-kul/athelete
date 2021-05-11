import time
from datetime import datetime

def find_athlete(id_, session, User, Athelete):
	# запрашиваем пользователя с заданным id
	query = session.query(User).filter(User.id == id_)
	# создаем список, который содержит рост данного пользователя
	ids = [row.height for row in query]
	if len(ids) > 0:	
		# создаем список, который содержит день рождения данного пользователя
		bths = [row.birthdate for row in query]
		# запрашиваем данные всех атлетов
		query_ath = session.query(Athelete).all()
		# переводим дату рождения атлетов в формат datetime из строки  и создаем словарь с id атлета и ДР атлета
		ath_dict_1 = {ath.id:datetime.strptime(ath.birthdate,"%Y-%m-%d") for ath in query_ath}
		# переводим дату рождения пользователя в формат datetime из формата date
		bths_datetime = datetime.combine(bths[0], datetime.min.time())
		min_b = time.time()
		# ищем атлета с ближайшим к пользователю днем рождения 
		
		for item,value in ath_dict_1.items():
			#обработка исключений
			try:
				if value is not None:

					if bths_datetime.timestamp() - value.timestamp() == 0:
						min_id_b = item
						break 
					elif abs(bths_datetime.timestamp() - value.timestamp()) <=min_b:
						min_b = abs(bths_datetime.timestamp() - value.timestamp())
						min_id_b = item
			except:
				continue
					
		# создаем словарь id атлета - рост атлета
		ath_dict = {ath.id:ath.height for ath in query_ath}
		min_= ids[0]
		# ищем атлета с ближайшим к пользователю росту	
		for item,value in ath_dict.items():
			#обработка исключений
			try:
				if value is not None:
					if abs(ids[0] - value) == 0:
						min_id = item
						break 
					elif (abs(ids[0] - value))< min_:
						min_ = (abs(ids[0] - value))
						min_id = item
			except:
				continue
		# находим атлета с подходящим ДР
		query_min_id_b = session.query(Athelete).filter(Athelete.id == min_id_b)
		ath_name = [row.name for row in query_min_id_b]
		# находим атлета с подходящим ростом
		query_min_id = session.query(Athelete).filter(Athelete.id == min_id)		
		ath_name_1 = [row.name for row in query_min_id]
		return ath_name[0], ath_name_1[0]
	else:
		print("Такого пользователя нет!!!") 