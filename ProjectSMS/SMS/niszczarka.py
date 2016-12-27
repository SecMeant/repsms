import os
import pytz
import sqlite3
from datetime import  datetime
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def destroyAfterExpire():
	print(os.path.join(BASE_DIR,'SMS\\TemporaryUser.db'))
	conn = sqlite3.connect(os.path.join(BASE_DIR,'SMS\\TemporaryUser.db'))
	c = conn.cursor()
	c.execute('SELECT * from tempUsers')
	try:
		users = c.fetchall()
		if(len(users) == 0):
			sqlite3.Error += "Brak uzytkowniko"
			raise sqlite3.Error

		for user in users:
			if(datetime.strptime(user[7],"%Y-%m-%d %H:%M:%S.%f").replace(tzinfo=pytz.utc) < datetime.utcnow().replace(tzinfo=pytz.utc)):
				
				c.execute('DELETE FROM tempUsers WHERE activCode=(?) ' , [user[6]])

	except sqlite3.Error as error:
		print ("error" + error[0])
	conn.commit()
	conn.close()

if __name__ == "__main__":
	destroyAfterExpire()