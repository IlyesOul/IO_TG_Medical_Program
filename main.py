import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFE
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests as re
from tkinter import *
from PIL import ImageTk, Image

button_width=5
button_height=2
# Parses strings with '+'s in between words
def parse_query(query):
    return_string = ""

    # Iterate through spaces
    for char in query:
        if char == " ":
            return_string += "+"
        else:
            return_string += char
    return return_string


def setdata1():
    prompt_results.append(int(agescale.get()))
    prompt_results.append(int(z.get()))
    prompt_results.append(int(y.get()))
    prompt_results.append(int(pressurebox.get()))
    prompt_results.append(int(cholbox.get()))
    prompt_results.append(int(ekgbox.get()))
    prompt_results.append(int(beatscale.get()))

def submit():
    setdata2()
    data = pd.read_csv("Heart_Disease_Prediction.csv")
    # print(data.head())
    # print()
    # print(f"Features = {data.columns._data}")

    # Acquire X/Y data
    X = np.array(data.drop(["Heart Disease"], axis=1))
    Y = np.array(data["Heart Disease"])

    # Train RFE model
    rfe_model = RFE(RandomForestClassifier())
    rfe_model.fit_transform(X=X, y=Y)

    # Obtain test/train data
    x_train = X[:int(len(X) * .75)]
    x_test = X[int(len(X) * .75):]

    y_train = Y[:int(len(X) * .75)]
    y_test = Y[int(len(X) * .75):]
    forest_ensemble = RandomForestClassifier(n_estimators=30)
    forest_ensemble.fit(x_train, y_train)
    prediction_result = forest_ensemble.predict([prompt_results])

    print(f"Based on your current conditions, we've predicted that you ", end='')

    if prediction_result[0] == "Presence":
        print("may have disease present in your body ")
    else:
        print("are disease free! ")

    if prediction_result[0] == "Presence":
        # Beginning of web-scrapping
        soup = BeautifulSoup()

        # Generating prompt DEFAULT LENGTH: 36 characters
        url_prompt = "What heart disease do I have with a "

        if prompt_results[3] >= 130:
            url_prompt += "high blood pressure"

        if prompt_results[4] >= 240:
            if len(url_prompt) > 36:
                url_prompt += "%2C high cholesterol"
            else:
                url_prompt += "high cholesterol"

        if prompt_results[12] == 1:
            if len(url_prompt) > 36:
                url_prompt += "%2C high blood sugar"
            else:
                url_prompt += "high blood sugar"

        if prompt_results[6]> 100:
            if len(url_prompt) > 36:
                url_prompt += " and a high heartbeat"
            else:
                url_prompt += "high heart rate"

        url_prompt = parse_query(url_prompt)

        # Make request and collect results
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
        }

        url = f"https://www.google.com/search?q={url_prompt}&rlz=1C1CHBF_enUS968US968&oq={url_prompt}&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCTEzNzU0ajBqN6gCALACAA&sourceid=chrome&ie=UTF-8"

        # Make query request
        request = re.get(url, headers=headers).text

        # Web scraping
        soup = BeautifulSoup(request, "html.parser")
        conditions = []

        for n in soup.find_all("b"):
            conditions.append(n.text)

        # Iterate through suggestion results and identify conditions
        target_condition = ""

        for item in conditions:
            if "cancer" in item or "diabetes" in item or "disease" in item:
                # General condition identified
                target_condition = item.title()

        # Prepare second request to determine solution
        url = f'https://www.google.com/search?q={parse_query(f"What should I do if I have {target_condition}")}&rlz=1C1CHBF_enUS968US968&oq={parse_query(f"What should I do if I have {target_condition}")}&gs_lcrp=EgZjaHJvbWUqBwgAEAAYgAQyBwgAEAAYgAQyBwgBEAAYgAQyDQgCEAAYhgMYgAQYigUyDQgDEAAYhgMYgAQYigXSAQg0NjExajBqN6gCALACAA&sourceid=chrome&ie=UTF-8'

        # Make query request
        request = re.get(url, headers=headers).text

        # Web scraping for solution
        soup = BeautifulSoup(request, "html.parser")
        solutions = []

        for n in soup.find_all("li", "TrT0Xe"):
            solutions.append(n.text)
            print(n)


        # Iterate through results and locate solution
        target_solutions = []

        for item in solutions:
            target_solutions.append(item)

        # Display predicted disease and solutions

        print(f"Based on your current conditions, we predict that you may have: {target_condition}")
        print("We suggest that you do the following in order to quell your condition:")

        for solution in target_solutions:
            print(solution)
    else:

        # Prevention suggestions
        url = f'https://www.google.com/search?q={parse_query(f"What should I do to prevent heart disease")}&rlz=1C1CHBF_enUS968US968&oq={parse_query(f"What should I do to prevent heart disease")}&gs_lcrp=EgZjaHJvbWUqBwgAEAAYgAQyBwgAEAAYgAQyBwgBEAAYgAQyDQgCEAAYhgMYgAQYigUyDQgDEAAYhgMYgAQYigXSAQg0NjExajBqN6gCALACAA&sourceid=chrome&ie=UTF-8'

        # Make query request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
        }
        request = re.get(url, headers=headers).text

        # Web scraping for suggestions
        soup = BeautifulSoup(request, "html.parser")
        solutions = []

        for n in soup.find_all("li", "TrT0Xe"):
            solutions.append(n.text)

        # Iterate through results and locate solution
        target_solutions = []

        for item in solutions:
            target_solutions.append(item)

        # Display predicted disease and solutions

        print("Here are some steps to take to prevent heart disease")

        for solution in target_solutions:
            print(solution)

def setdata2():
    prompt_results.append(int(x.get()))
    prompt_results.append(int(depbox.get()))
    prompt_results.append(int(s.get()))
    prompt_results.append(int(vesselbox.get()))
    prompt_results.append(int(t.get()))
    prompt_results.append(int(sg.get()))

def nextpage():
    setdata1()
    for i,x1,y1 in geometry:
        i.place_forget()
    for i,x1,y1 in geometry2:
        i.place(x=x1,y=y1)

    #iterate through each first column of each row and destroy the widgets from the canvases
    #use place_forget to remove all widgets from both canvases
    #use a for loop to iterate through the 2D arrays and replace the widgets in the proper x and y values
    #repeat steps in prevpage method

def prevpage():
    prompt_results=[]
    for i, x1, y1 in geometry2:
        i.place_forget()
    for i, x1, y1 in geometry:
        i.place(x=x1, y=y1)

window=Tk()

window.geometry("6000x6000")
window.update()

geometry=[]
#make a 2D array with x rows (based on number of widgets in canvas) and 3 columns that store the widget and the x and y values
canvas=Canvas(window,width=window.winfo_screenwidth(),height=window.winfo_screenheight())
canvas.pack()

agelabel=Label(canvas,text="Age?",font=(10))
agelabel.place(x=canvas.winfo_screenwidth()/2,y=0)

geometry.append([agelabel,canvas.winfo_screenwidth()/2,0])

agescale=Scale(canvas,from_=100,to=0,tickinterval=10,font=(20),length=1000,resolution=1,orient=HORIZONTAL)
agescale.place(x=150,y=40)

geometry.append([agescale,150,40])

genderlabel=Label(canvas,text="Gender?",font=(15))
genderlabel.place(x=canvas.winfo_screenwidth()/2-15,y=130)

geometry.append([genderlabel,canvas.winfo_screenwidth()/2-15,130])

z=IntVar()

y=IntVar()

malebutton = Radiobutton(canvas,width=button_width,variable=z,value=0,height=button_height,text="Male",font=("Arial",12))
malebutton.place(x=canvas.winfo_screenwidth()/2-60,y=button_height+160)


geometry.append([malebutton,canvas.winfo_screenwidth()/2-60,button_height+160])

femalebutton = Radiobutton(canvas,width=button_width,variable=z,value=1,height=button_height,text="Female",font=("Arial",12))
femalebutton.place(x=canvas.winfo_screenwidth()/2+40,y=button_height+160)

geometry.append([femalebutton,canvas.winfo_screenwidth()/2+40,button_height+160])

chestlabel=Label(canvas,text="What kind of chest pains are you feeling?",font=(10))
chestlabel.place(x=canvas.winfo_screenwidth()/2-150,y=200)

geometry.append([chestlabel,canvas.winfo_screenwidth()/2-150,200])

typicalbutton = Radiobutton(canvas,width=button_width+5,variable=y,value=1,height=button_height,text="typical angina",font=("Arial",10))
typicalbutton.place(x=100,y=250)

geometry.append([typicalbutton,100,250])

atypicalbutton = Radiobutton(canvas,width=button_width+5,variable=y,value=2,height=button_height,text="atypical angina",font=("Arial",10))
atypicalbutton.place(x=400,y=250)

geometry.append([atypicalbutton,400,250])

nontypicalbutton = Radiobutton(canvas,width=button_width+8,variable=y,value=3,height=button_height,text="non-typical angina",font=("Arial",10))
nontypicalbutton.place(x=700,y=250)

geometry.append([nontypicalbutton,700,250])

asymptomaticbutton = Radiobutton(canvas,width=button_width+10,variable=y,value=4,height=button_height,text="asymptomatic angina",font=("Arial",10))
asymptomaticbutton.place(x=1000,y=250)

geometry.append([asymptomaticbutton,1000,250])


pressurelabel=Label(canvas,text="What is your blood pressure?",font=(15))
pressurelabel.place(x=canvas.winfo_screenwidth()/2-110,y=290)

geometry.append([pressurelabel,canvas.winfo_screenwidth()/2-110,290])

pressurebox=Entry(canvas,width=20,borderwidth=3.0,font=(15))
pressurebox.place(x=canvas.winfo_screenwidth()/2-90,y=320)

geometry.append([pressurebox,canvas.winfo_screenwidth()/2-90,320])

chollabel=Label(canvas,text="What is your cholesterol?",font=(15))
chollabel.place(x=canvas.winfo_screenwidth()/2-90,y=360)

geometry.append([chollabel,canvas.winfo_screenwidth()/2-90,360])

cholbox=Entry(canvas,width=20,borderwidth=3.0,font=(15))
cholbox.place(x=canvas.winfo_screenwidth()/2-90,y=390)

geometry.append([cholbox,canvas.winfo_screenwidth()/2-90,390])

ekglabel=Label(canvas,text="If any, what is the result of your EKG test?",font=(15))
ekglabel.place(x=canvas.winfo_screenwidth()/2-150,y=420)

geometry.append([ekglabel,canvas.winfo_screenwidth()/2-150,420])

ekgbox=Entry(canvas,width=20,borderwidth=3.0,font=(15))
ekgbox.place(x=canvas.winfo_screenwidth()/2-90,y=450)

geometry.append([ekgbox,canvas.winfo_screenwidth()/2-90,450])

beatlabel=Label(canvas,text="When your heart is under stress, what's the highest rate at which it can beat?",font=(15))
beatlabel.place(x=canvas.winfo_screenwidth()/2-300,y=480)

geometry.append([beatlabel,canvas.winfo_screenwidth()/2-300,480])

beatscale=Scale(canvas,from_=100,to=30,tickinterval=10,font=(20),length=1000,resolution=1,orient=HORIZONTAL)
beatscale.place(x=200,y=510)

geometry.append([beatscale,200,510])

Nextbutton=Button(canvas,text="Next Page",width=button_width+5,height=button_height,borderwidth=2,font=("Arial",12,"underline"),command=nextpage)
Nextbutton.place(x=canvas.winfo_screenwidth()-120,y=0)

geometry.append([Nextbutton,canvas.winfo_screenwidth()-120,0])

#make all canvas widgets here

#make a 2D array with x rows (based on number of widgets in canvas) and 3 columns that store the widget and the x and y values

geometry2=[]

exlabel=Label(canvas,text="Do you experience angina chest pain when you exercise?",font=(15))

x=IntVar()

geometry2.append([exlabel,canvas.winfo_screenwidth()/2-220,30])

yesbutton = Radiobutton(canvas,width=button_width,variable=x,value=1,height=button_height,text="Yes",font=("Arial",12))

geometry2.append([yesbutton,canvas.winfo_screenwidth()/2-60,60])

nobutton = Radiobutton(canvas,width=button_width,variable=x,value=0,height=button_height,text="No",font=("Arial",12))

geometry2.append([nobutton,canvas.winfo_screenwidth()/2+40,60])

deplabel=Label(canvas,text="If you experience any levels of S/T Depression, indicate it now: (mm)",font=(15))


geometry2.append([deplabel,canvas.winfo_screenwidth()/2-270,110])

depbox=Entry(canvas,width=20,borderwidth=3.0,font=(15))


geometry2.append([depbox,canvas.winfo_screenwidth()/2-90,140])

slopelabel=Label(canvas,text="Please enter the slope of your S/T Depression:",font=(15))


s=IntVar()

geometry2.append([slopelabel,canvas.winfo_screenwidth()/2-180,180])

upslopingbutton = Radiobutton(canvas,width=button_width+5,variable=s,value=1,height=button_height,text="Upsloping",font=("Arial",12))


geometry2.append([upslopingbutton,canvas.winfo_screenwidth()/2-150,210])

flatbutton = Radiobutton(canvas,width=button_width,variable=s,value=2,height=button_height,text="Flat",font=("Arial",12))


geometry2.append([flatbutton,canvas.winfo_screenwidth()/2-5,210])

downslopingbutton = Radiobutton(canvas,width=button_width+5,variable=s,value=3,height=button_height,text="Downsloping",font=("Arial",12))


geometry2.append([downslopingbutton,canvas.winfo_screenwidth()/2+90,210])

vessellabel=Label(canvas,text="How many of your major vessels have been colored by fluoroscopy? (0-3)",font=(15))


geometry2.append([vessellabel,canvas.winfo_screenwidth()/2-260,240])

vesselbox=Entry(canvas,width=20,borderwidth=3.0,font=(15))


geometry2.append([vesselbox,canvas.winfo_screenwidth()/2-90,290])

thallabel=Label(canvas,text="Please enter the results of any Thallium testing you may have had:",font=(15))


t=IntVar()

geometry2.append([thallabel,canvas.winfo_screenwidth()/2-240,320])

normalbutton = Radiobutton(canvas,width=button_width,variable=t,value=3,height=button_height,text="Normal",font=("Arial",12))


geometry2.append([normalbutton,canvas.winfo_screenwidth()/2-200,350])

fixedbutton = Radiobutton(canvas,width=button_width+10,variable=t,value=6,height=button_height,text="Fixed Defect",font=("Arial",12))


geometry2.append([fixedbutton,canvas.winfo_screenwidth()/2-80,350])

reversablebutton = Radiobutton(canvas,width=button_width+10,variable=t,value=7,height=button_height,text="Reversable Defect",font=("Arial",12))


geometry2.append([reversablebutton,canvas.winfo_screenwidth()/2+120,350])

submitbutton=Button(canvas,width=button_width+5,height=button_height,borderwidth=2,text="Submit",font=(12),command=submit)


geometry2.append([submitbutton,canvas.winfo_screenwidth()/2-20,480])

prevbutton=Button(canvas,width=button_width+8,height=button_height,text="Previous Page",font=("Arial",12,"underline"),command=prevpage)


geometry2.append([prevbutton,2,0])

sugarlabel=Label(canvas,text="Is your fasting blood sugar level over 120 mg/dl? (1 for true and 0 for false): ",font=(15))


geometry2.append([sugarlabel,canvas.winfo_screenwidth()/2-270,canvas.winfo_screenheight()-340])

sg=IntVar()

tsg=Radiobutton(canvas,text="True",variable=sg,value=1,font=(12))


geometry2.append([tsg,canvas.winfo_screenwidth()/2-50,canvas.winfo_screenheight()-300])

fsg=Radiobutton(canvas,text="False",variable=sg,value=0,font=(12))


geometry2.append([fsg,canvas.winfo_screenwidth()/2+70,canvas.winfo_screenheight()-300])


window.update()
# Data Collection
data = pd.read_csv("Heart_Disease_Prediction.csv")
# print(data.head())
# print()
# print(f"Features = {data.columns._data}")

# Acquire X/Y data
X = np.array(data.drop(["Heart Disease"], axis=1))
Y = np.array(data["Heart Disease"])


# Train RFE model
rfe_model = RFE(RandomForestClassifier())
rfe_model.fit_transform(X=X, y=Y)

# Obtain test/train data
x_train = X[:int(len(X)*.75)]
x_test = X[int(len(X)*.75):]

y_train = Y[:int(len(X)*.75)]
y_test = Y[int(len(X)*.75):]
forest_ensemble = RandomForestClassifier(n_estimators=30)
forest_ensemble.fit(x_train, y_train)
# Optimization of n_estimators
# list_of_dicts = []
#
# estimator_to_score = {}
#
# # Trial 1
# for i in range(10, 120, 10):
# 	random_forest = RandomForestClassifier(n_estimators=i)
# 	random_forest.fit(x_train, y_train)
# 	estimator_to_score[i] = random_forest.score(x_test, y_test)
#
# list_of_dicts.append(estimator_to_score)
# estimator_to_score = {}
#
# # Trial 2
# for i in range(10, 120, 10):
# 	random_forest = RandomForestClassifier(n_estimators=i)
# 	random_forest.fit(x_train, y_train)
# 	estimator_to_score[i] = random_forest.score(x_test, y_test)
#
# list_of_dicts.append(estimator_to_score)
# estimator_to_score = {}
#
# # Trial 3
# for i in range(10, 120, 10):
# 	random_forest = RandomForestClassifier(n_estimators=i)
# 	random_forest.fit(x_train, y_train)
# 	estimator_to_score[i] = random_forest.score(x_test, y_test)
#
# list_of_dicts.append(estimator_to_score)
# estimator_to_score = {}
#
# # Print out results from each trial
# for i in range(len(list_of_dicts)):
# 	print(list_of_dicts[i])

# plt.xlabel("N_estimators")
# plt.ylabel("Testing Accuracy")
# plt.plot(range(10, 120, 10), scores, c='red')
# plt.show()

# Create optimized Forest Ensemble

# Train & Test Ensemble


# Examination of model results
# print(f"Accuracy of forest: {forest_ensemble.score(x_test, y_test)}")
#
# prediction_results = forest_ensemble.predict(x_test)
#
# for i in range(len(prediction_results)):
# 	print(f"Predicted Value: {prediction_results[i]}; Actual value: {y_test[i]}")

# User Prompting

prompt_results = []
#
# # Presence values
# #prompt_results = [56, 1, 2, 310, 270, 1, 2, 150, 1, 2, 2, 1, 3]
#
# #prompt_results.append(int(input("What is your age? ")))
# prompt_results.append(int(input("What is your sex? (0 for male, 1 for female) ")))
# prompt_results.append(int(input("What kind of chest pains are you feeling? Enter 1 for typical angina, 2 for atypical angina"
#                             ", 3 for non-typical anginal pain, or 4 if you're  asymptomatic: ")))
# blood_pressure = (int(input("What is your blood pressure? ")))
# #blood_pressure = 310
# prompt_results.append(blood_pressure)
# cholesterol_level = int(input("What is your cholesterol? "))
# #cholesterol_level = 210
# prompt_results.append(cholesterol_level)
# sugar_above_120 = int(input("Is your fasting blood sugar level over 120 mg/dl? (1 for true and 0 for false): "))
# prompt_results.append(sugar_above_120)
# #sugar_above_120 = 1
# prompt_results.append(int(input("If any, what is the result of your EKG test?  ")))
# heart_beat = int(input("When your heart is under stress, what's the highest rate at which it can beat? "))
# #heart_beat = 130
# prompt_results.append(heart_beat)
# prompt_results.append(int(input("Do you experience angina chest pain when you exercise? (1 for yes, 0 for no): ")))
# prompt_results.append(int(input("If you experience any levels of S/T Depression, indicate it now: ")))
# prompt_results.append(int(input("Please enter the slope of your S/T Depression: (1 for upsloping, 2 for flat, "
#                                "and 3 for downsloping) ")))
# prompt_results.append(int(input("How many of your major vessels have been colored by fluoroscopy? (0-3) ")))
# prompt_results.append(int(input("Please enter the results of any Thallium testing you may have had:"
#                                  "(3 for normal, 6 for fixed defect, 7 for reversable defect) ")))
#
#


window.mainloop()
