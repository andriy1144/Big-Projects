import mysql.connector
# Own dispatcher for controlling the database

class UseDatabase():
	def __init__(self,config) -> object:
		self.configuratoin = config
	def __enter__(self):
		self.conn = mysql.connector.connect(**self.configuratoin)
		self.cursor = self.conn.cursor()
		return self.cursor
	def __exit__(self, exc_type, exc_val, exc_tb):
		self.conn.commit()
		self.conn.close()
		self.cursor.close()