from cryptography.fernet import Fernet
import getpass
import json
from os import path

class BookerConfig:
	filename = 'booker.json'
	user_list = []
	pwd_list = []

	@staticmethod
	def load_file():
		if(path.isfile(BookerConfig.filename)):
			with open(BookerConfig.filename) as conf_file:
				conf_map = json.load(conf_file)
			key = list(conf_map.keys())[0]
			if(conf_map[key] != ''):
				user_map = conf_map[key]
				f = Fernet(bytes(key,encoding='utf-8'))
				for user in list(user_map.keys()):
					BookerConfig.user_list.append(f.decrypt(bytes(user,encoding='utf-8')).decode('utf-8'))
					BookerConfig.pwd_list.append(f.decrypt(bytes(user_map[user],encoding='utf-8')).decode('utf-8'))

	@staticmethod
	def getUsers():
		return BookerConfig.user_list

	@staticmethod
	def getPwds():
		return BookerConfig.pwd_list	


if __name__ == "__main__":
    #foo = BookerConfig()
    BookerConfig.load_file()
    print(BookerConfig.getUsers())
    print(BookerConfig.getPwds())		
	