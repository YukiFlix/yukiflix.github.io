_A='utf-8'
from flask import*
import os,json,pickle,base64
def decrypt(encoded_text):encoded_bytes=encoded_text.encode(_A);decoded_bytes=base64.b64decode(encoded_bytes);return decoded_bytes.decode(_A)
def create_folder(name):
	if not os.path.exists(name):os.makedirs(name)
def create_root(root):
	folders=root.split('/');orig_dir=os.getcwd()
	for x in range(len(folders)):
		try:create_folder(folders[x]);os.chdir(folders[x])
		except:pass
	os.chdir(orig_dir)
def write_json(data,file_path):
	with open(file_path,'w',encoding=_A)as file:json.dump(data,file,ensure_ascii=True,indent=4)
def read_json(file):
	with open(file,'r',encoding=_A)as file:data=json.load(file)
	return data
def get_input(_input):return request.form[_input]
def read_pickle(file):
	try:
		with open(file,'rb')as visits_file:return pickle.load(visits_file)
	except:return 0
def write_pickle(file,variable):
	with open(file,'wb')as visits_file:pickle.dump(variable,visits_file)
def count():A='visits.pkl';visits=read_pickle(A)+1;write_pickle(A,visits)
def search_movie_and_series_with_letter(lettre):
	B='series';A='movies';data=read_json('data.json')
	if lettre=='all':return data
	def format(liste):return dict(item for sublist in liste for item in sublist.items())
	movies=data[A];series=data[B];movies2=[{key:value}for(key,value)in movies.items()if list(key)[0].lower()==lettre];movies=format(movies2);series2=[{key:value}for(key,value)in series.items()if list(key)[0].lower()==lettre];series=format(series2);dictio={A:movies,B:series};return dictio