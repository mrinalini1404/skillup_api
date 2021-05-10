import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from flask import Flask, render_template,request, redirect, url_for, session,Response
from flask import Flask, jsonify, request, redirect
from flask_pymongo import PyMongo
import pandas as pd 
import numpy as np      
import pickle
from pymongo import MongoClient
app = Flask(__name__)
app.secret_key = 'Mrinalini'

client = MongoClient("mongodb://localhost:27017")
db = client.test


@app.route('/',methods=['GET'])
def home():
	return jsonify({'result' : 'k'})
    
@app.route('/position',methods=['GET'])
def position():
	#data=request.get_json()
    #id_no = data['id']
	#print(id_no)
	id_no=150
	star = db.students
	s = star.find_one({'ID' : id_no})
	# if s:
	# 	output = {'GradeID' : s['GradeID']}
	# else:
	# 	output = "No such name"


	gender_map = {'M':1, 
              'F':2}

	StageID_map = {'HighSchool':1, 
				'lowerlevel':2, 
				'MiddleSchool':3}

	GradeID_map =   {'G-01':1,
					'G-02':2,
					'G-03':3,
					'G-04':4,
					'G-05':5,
					'G-06':6,
					'G-07':7,
					'G-08':8,
					'G-09':9,
					'G-10':10,
					'G-11':11,
					'G-12':12}



	Topic_map  =    {'Biology' : 1,
					'Geology' : 2,
					'Quran' : 3,
					'Science' : 4,
					'Spanish' : 5,
					'IT' : 6,
					'French' : 7,
					'English' :8,
					'Arabic' :9,
					'Chemistry' :10,
					'Math' :11,
					'History' : 12}



	StudentAbsenceDays_map = {'Under-7':0,
							'Above-7':1}

	Class_map = {'H':10,
				'M':5,
				'L':2}



	gender=s['gender']
	StageID=s['StageID']
	GradeID=s['GradeID']
	Topic=s['Topic']
	raisedHands=s['raisedHands']
	VisitedResources=s['VisitedResources']
	AnnouncementsView=s['AnnouncementsView']
	Discussion=s['Discussion']
	StudentAbsenceDays=s['StudentAbsenceDays']

	gender                 = gender_map[gender]
	StageID                = StageID_map[StageID]
	GradeID                = GradeID_map[GradeID]
	Topic                  = Topic_map[Topic]
	StudentAbsenceDays     = StudentAbsenceDays_map[StudentAbsenceDays]

	print(gender)
	filename = 'finalized_model.sav'
	loaded_model = pickle.load(open(filename, 'rb'))

	test_x = np.array([gender, StageID, GradeID, Topic, raisedHands, VisitedResources, AnnouncementsView, Discussion, StudentAbsenceDays]).reshape(1, -1)
	result = loaded_model.predict(test_x)

	return jsonify({'result' : str(result[0])})

if __name__ == '__main__':
   app.run(host='localhost',debug=True)
