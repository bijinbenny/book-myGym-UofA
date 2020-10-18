from cryptography.fernet import Fernet
import getpass
import json
from os import path


filename = 'booker.json'
user_map = {}
user = input("Enter user email id: ")
pass1 = getpass.getpass(prompt='Enter password: ')
pass2 = getpass.getpass(prompt='Confirm password: ')
if(pass1 != pass2):
	print("Passwords do not match!")
	exit()
if(not path.isfile(filename)):
	key = Fernet.generate_key()
	with open(filename,'w') as conf_file:
		key_map = {key.decode('utf-8') : ''}
		json.dump(key_map,conf_file)
with open(filename) as conf_file:
  	conf_map = json.load(conf_file)		
key = list(conf_map.keys())[0]
if(conf_map[key] != ''):
	user_map = conf_map[key]
f = Fernet(bytes(key,encoding='utf-8'))
user_map[f.encrypt(bytes(user,encoding='utf-8')).decode('utf-8')] = f.encrypt(bytes(pass1,encoding='utf-8')).decode('utf-8')
conf_map[key] = user_map
with open(filename,'w') as conf_file:
	json.dump(conf_map,conf_file)
