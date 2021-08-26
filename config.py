import os


class Config:
	APP_NAME = os.getenv('APP_NAME', 'IPBDAM5_herkansing')
	DATABASE_URI = os.getenv('DATABASE_URI', 'mysql+pymysql://root@127.0.0.1:3306/test')
	BASE_PATH = os.getenv('BASE_PATH', os.path.abspath(os.path.dirname(__file__)))
	# os.path.dirname(os.path.abspath(__file__))


__all__ = ['Config']
