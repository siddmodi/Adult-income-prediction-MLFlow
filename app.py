from flask import Flask, render_template, request
from flask_cors import cross_origin
import joblib
import numpy as np
import pandas as pd
import os
import joblib
from sklearn import pipeline
from flask import redirect, url_for
os.getcwd()

data_pipeline = joblib.load(open('Pipeline/pipeline.joblib','rb'))

app = Flask(__name__)

@app.route('/')
@cross_origin()
def home():
  return render_template('home.html')


@app.route('/predict', methods=['POST','GET'])
@cross_origin()
def predict():
    
    # # age
    age = int(request.form['age'])
    # age = request.form.get("age")

    # education
    education = request.form["education"]
    # education = 0


    # hours_per_week
    hours_per_week = request.form["hours_per_week"]
    # hours_per_week = 0

    # marital_status
    marital_status_single = request.form["marital_status"]
    # marital_status_single = 0

    # workclass
    workclass = request.form["workclass"]
    # workclass = 'Self emp not inc'
    
    if workclass == 'Self emp not inc':
        local_gov = 0
        private = 0
        self_emp_inc = 0
        self_emp_not_inc = 1
        state_gov = 0
        without_pay = 0
    
    elif workclass == 'Private':
        local_gov = 0
        private = 1
        self_emp_inc = 0
        self_emp_not_inc = 0
        state_gov = 0
        without_pay = 0

    elif workclass == 'State gov':
        local_gov = 0
        private = 0
        self_emp_inc = 0
        self_emp_not_inc = 0
        state_gov = 1
        without_pay = 0

    elif workclass == 'Local gov':
        local_gov = 1
        private = 0
        self_emp_inc = 0
        self_emp_not_inc = 0
        state_gov = 0
        without_pay = 0

    elif workclass == 'Self emp inc':
        local_gov = 0
        private = 0
        self_emp_inc = 1
        self_emp_not_inc = 0
        state_gov = 0
        without_pay = 0
    
    elif workclass == 'Without pay':
        local_gov = 0
        private = 0
        self_emp_inc = 0
        self_emp_not_inc = 0
        state_gov = 0
        without_pay = 1

    else:
        local_gov = 0
        private = 0
        self_emp_inc = 0
        self_emp_not_inc = 0
        state_gov = 0
        without_pay = 0

    # occupation
    occupation = request.form["occupation"]
    # occupation == 'Craft repair'

    if occupation == 'Craft repair':
        craft_repair = 1
        exec_managerial = 0  
        farming_fishing = 0
        handlers_cleaners = 0
        machine_op_inspct = 0
        other = 0
        prof_specialty = 0 
        protective_serv = 0
        sales = 0
        tech_support = 0 
        transport_moving = 0
        others = 0
    
    elif occupation == 'Exec managerial':
        craft_repair = 0
        exec_managerial = 1  
        farming_fishing = 0
        handlers_cleaners = 0
        machine_op_inspct = 0
        other = 0
        prof_specialty = 0 
        protective_serv = 0
        sales = 0
        tech_support = 0 
        transport_moving = 0
        others = 0

    elif occupation == 'Farming fishing':
        craft_repair = 0
        exec_managerial = 0  
        farming_fishing = 1
        handlers_cleaners = 0
        machine_op_inspct = 0
        other = 0
        prof_specialty = 0 
        protective_serv = 0
        sales = 0
        tech_support = 0 
        transport_moving = 0
        others = 0
    
    elif occupation == 'Handlers cleaners':
        craft_repair = 0
        exec_managerial = 0  
        farming_fishing = 0
        handlers_cleaners = 1
        machine_op_inspct = 0
        other = 0
        prof_specialty = 0 
        protective_serv = 0
        sales = 0
        tech_support = 0 
        transport_moving = 0
        others = 0

    elif occupation == 'Machine op inspct':
        craft_repair = 0
        exec_managerial = 0  
        farming_fishing = 0
        handlers_cleaners = 0
        machine_op_inspct = 1
        other = 0
        prof_specialty = 0 
        protective_serv = 0
        sales = 0
        tech_support = 0 
        transport_moving = 0
        others = 0

    elif occupation == 'Prof specialty':
        craft_repair = 0
        exec_managerial = 0  
        farming_fishing = 0
        handlers_cleaners = 0
        machine_op_inspct = 0
        other = 0
        prof_specialty = 1
        protective_serv = 0
        sales = 0
        tech_support = 0 
        transport_moving = 0
        others = 0

    elif occupation == 'Protective serv':
        craft_repair = 0
        exec_managerial = 0  
        farming_fishing = 0
        handlers_cleaners = 0
        machine_op_inspct = 0
        other = 0
        prof_specialty = 0 
        protective_serv = 1
        sales = 0
        tech_support = 0 
        transport_moving = 0
        others = 0

    elif occupation == 'Sales':
        craft_repair = 0
        exec_managerial = 0  
        farming_fishing = 0
        handlers_cleaners = 0
        machine_op_inspct = 0
        other = 0
        prof_specialty = 0 
        protective_serv = 0
        sales = 1
        tech_support = 0 
        transport_moving = 0
        others = 0

    elif occupation == 'Tech support':
        craft_repair = 0
        exec_managerial = 0  
        farming_fishing = 0
        handlers_cleaners = 0
        machine_op_inspct = 0
        other = 0
        prof_specialty = 0 
        protective_serv = 0
        sales = 0
        tech_support = 1
        transport_moving = 0
        others = 0

    elif occupation == 'Transport moving':
        craft_repair = 0
        exec_managerial = 0  
        farming_fishing = 0
        handlers_cleaners = 0
        machine_op_inspct = 0
        other = 0
        prof_specialty = 0 
        protective_serv = 0
        sales = 0
        tech_support = 0 
        transport_moving = 1
        others = 0

    elif occupation == 'others':
        craft_repair = 0
        exec_managerial = 0  
        farming_fishing = 0
        handlers_cleaners = 0
        machine_op_inspct = 0
        other = 0
        prof_specialty = 0 
        protective_serv = 0
        sales = 0
        tech_support = 0 
        transport_moving = 0
        others = 1


    # sex
    male = request.form["sex"]

    # country
    country = request.form["country"]
    if country == 'El Salvador':
        el_salvador = 1
        germany = 0 
        india = 0
        mexico = 0
        philippines = 0
        puerto_rico = 0
        united_states = 0
        country_others = 0
    
    if country == 'Germany':
        el_salvador = 0
        germany = 1
        india = 0
        mexico = 0
        philippines = 0
        puerto_rico = 0
        united_states = 0
        country_others = 0

    if country == 'India':
        el_salvador = 0
        germany = 0 
        india = 1
        mexico = 0
        philippines = 0
        puerto_rico = 0
        united_states = 0
        country_others = 0

    if country == 'Mexico':
        el_salvador = 0
        germany = 0 
        india = 0
        mexico = 1
        philippines = 0
        puerto_rico = 0
        united_states = 0
        country_others = 0

    if country == 'Philippines':
        el_salvador = 0
        germany = 0 
        india = 0
        mexico = 0
        philippines = 1
        puerto_rico = 0
        united_states = 0
        country_others = 0

    if country == 'Puerto Rico':
        el_salvador = 0
        germany = 0 
        india = 0
        mexico = 0
        philippines = 0
        puerto_rico = 1
        united_states = 0
        country_others = 0

    if country == 'United States':
        el_salvador = 0
        germany = 0 
        india = 0
        mexico = 0
        philippines = 0
        puerto_rico = 0
        united_states = 1
        country_others = 0

    if country == 'others':
        el_salvador = 0
        germany = 0 
        india = 0
        mexico = 0
        philippines = 0
        puerto_rico = 0
        united_states = 0
        country_others = 1


    # capital_gain_or_loss
    capital_gain_or_loss = request.form["capital_gain_or_loss"]

    inp={
        'age':[age] ,
        'education':[education] ,
        'hours_per_week':[hours_per_week] ,
        'marital_status_single':[marital_status_single] ,
        'local_gov':[local_gov],
        'private':[private] , 
        'self_emp_inc':[self_emp_inc] , 
        'self_emp_not_inc':[self_emp_not_inc] ,
        'state_gov':[state_gov] ,
        'without_pay':[without_pay] ,  
        'craft_repair':[craft_repair] ,
        'exec_managerial':[exec_managerial] , 
        'farming_fishing':[farming_fishing] ,   
        'handlers_cleaners':[handlers_cleaners] , 
        'machine_op_inspct':[machine_op_inspct] , 
        'other':[other] , 
        'prof_specialty':[prof_specialty] ,
        'protective_serv':[protective_serv] ,
        'sales':[sales] ,
        'tech_support':[tech_support] , 
        'transport_moving':[transport_moving] ,
        'others':[others] ,
        'male':[male] ,
        'el_salvador':[el_salvador] ,
        'germany':[germany] , 
        'india':[india] ,
        'mexico':[mexico] ,
        'philippines':[philippines] ,
        'puerto_rico':[puerto_rico] , 
        'united_states':[united_states] ,
        'country_others':[country_others] ,
        'capital_gain_or_loss':[capital_gain_or_loss]
    }
    ini=pd.DataFrame(inp)
    prediction = data_pipeline.predict(ini)

    if prediction == 0:
        output = "Greater then 50K"
    elif prediction == 1:
        output = "Less then 50K"

    return render_template('home.html',prediction_text=f"Your Salary is {output}")


if __name__ == "__main__":
    app.run(debug=True)




