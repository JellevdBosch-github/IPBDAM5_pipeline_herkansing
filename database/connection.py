# class for connecting and retrieving connection to mysql database
from sqlalchemy import create_engine


class Connection:

	def __init__(self):
		"""
		Initializes the database connection using the SQLAlchemy Engine
		# :param host: The host where the database is hosted, usually 127.0.0.1 (localhost)
		# :param port: The port used to locate the database, usually 3306
		# :param database: The name of the database
		# :param user: The username which is used to access the database, usually root
		# :param password: The password which is used to access the database, usually empty
		"""
		self.engine = create_engine('mysql+pymysql://root@127.0.0.1:3306/test')
		self.conn = self.connect()

	def connect(self):
		"""
		Establishes connection to the database
		:return: SQLAlchemy Engine Connection
		"""
		try:
			return self.engine.connect()
		except ConnectionError as ce:
			print(ce)

	def get_connection(self):
		"""
		:return: SQLAlchemy Engine Connection object
		"""
		return self.conn

	def get_engine(self):
		"""
		:return: SQLAlchemy Engine object
		"""
		return self.engine

	def disconnect(self):
		"""
		Disconnect the SQLAlchemy Engine from the database
		:return: Boolean
		"""
		return self.conn.close()
