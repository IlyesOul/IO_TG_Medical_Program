import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFE
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests as re


# Parses strings with '+'s in between words
def parse_spaces(query):
    return_string = ""

    # Iterate through spaces
    for char in query:
        if char == " ":
            return_string += "+"
        else:
            return_string += char
    return return_string


# Data Collection
data = pd.read_csv("Heart_Disease_Prediction.csv")
# print(data.head())
# print()
# print(f"Features = {data.columns._data}")

# Acquire X/Y data
X = np.array(data.drop(["Heart Disease"], 1))
Y = np.array(data["Heart Disease"])


# Train RFE model
rfe_model = RFE(RandomForestClassifier())
rfe_model.fit_transform(X=X, y=Y)

# Obtain test/train data
x_train = X[:int(len(X)*.75)]
x_test = X[int(len(X)*.75):]

y_train = Y[:int(len(X)*.75)]
y_test = Y[int(len(X)*.75):]

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
forest_ensemble = RandomForestClassifier(n_estimators=30)

# Train & Test Ensemble
forest_ensemble.fit(x_train, y_train)

# Examination of model results
# print(f"Accuracy of forest: {forest_ensemble.score(x_test, y_test)}")
#
# prediction_results = forest_ensemble.predict(x_test)
#
# for i in range(len(prediction_results)):
# 	print(f"Predicted Value: {prediction_results[i]}; Actual value: {y_test[i]}")

# User Prompting

prompt_results = []

# Presence values
# prompt_results = [56, 1, 2, 310, 270, 1, 2, 150, 1, 2, 2, 1, 3]

prompt_results.append(int(input("What is your age? ")))
prompt_results.append(int(input("What is your sex? (0 for male, 1 for female) ")))
prompt_results.append(int(input("What kind of chest pains are you feeling? Enter 1 for typical angina, 2 for atypical angina"
                            ", 3 for non-typical anginal pain, or 4 if you're  asymptomatic: ")))
blood_pressure = (int(input("What is your blood pressure? ")))
# blood_pressure = 310
prompt_results.append(blood_pressure)
cholesterol_level = int(input("What is your cholesterol? "))
# cholesterol_level = 210
prompt_results.append(cholesterol_level)
sugar_above_120 = int(input("Is your fasting blood sugar level over 120 mg/dl? (1 for true and 0 for false): "))
prompt_results.append(sugar_above_120)
# sugar_above_120 = 1
prompt_results.append(int(input("If any, what is the result of your EKG test?  ")))
heart_beat = int(input("When your heart is under stress, what's the highest rate at which it can beat? "))
# heart_beat = 130
prompt_results.append(heart_beat)
prompt_results.append(int(input("Do you experience angina chest pain when you exercise? (1 for yes, 0 for no): ")))
prompt_results.append(int(input("If you experience any levels of S/T Depression, indicate it now: ")))
prompt_results.append(int(input("Please enter the slope of your S/T Depression: (1 for upsloping, 2 for flat, "
                                 "and 3 for downsloping) ")))
prompt_results.append(int(input("How many of your major vessels have been colored by fluoroscopy? (0-3) ")))
prompt_results.append(int(input("Please enter the results of any Thallium testing you may have had:"
                                 "(3 for normal, 6 for fixed defect, 7 for reversable defect) ")))

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

    if blood_pressure >= 130:
        url_prompt += "high blood pressure"

    if cholesterol_level >= 240:
        if len(url_prompt) > 36:
            url_prompt += "%2C high cholesterol"
        else:
            url_prompt += "high cholesterol"

    if sugar_above_120 == 1:
        if len(url_prompt) > 36:
            url_prompt += "%2C high blood sugar"
        else:
            url_prompt += "high blood sugar"

    if heart_beat > 100:
        if len(url_prompt) > 36:
            url_prompt += " and a high heartbeat"
        else:
            url_prompt += "high heart rate"

    url_prompt = parse_spaces(url_prompt)

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
    url = f'https://www.google.com/search?q={parse_spaces(f"What should I do if I have {target_condition}")}&rlz=1C1CHBF_enUS968US968&oq={parse_spaces(f"What should I do if I have {target_condition}")}&gs_lcrp=EgZjaHJvbWUqBwgAEAAYgAQyBwgAEAAYgAQyBwgBEAAYgAQyDQgCEAAYhgMYgAQYigUyDQgDEAAYhgMYgAQYigXSAQg0NjExajBqN6gCALACAA&sourceid=chrome&ie=UTF-8'

    # Make query request
    request = re.get(url, headers=headers).text

    # Web scraping for solution
    soup = BeautifulSoup(request, "html.parser")
    solutions = []

    for n in soup.find_all("li", "TrT0Xe"):
        solutions.append(n.text)

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
    url = f'https://www.google.com/search?q={parse_spaces(f"What should I do to prevent heart disease")}&rlz=1C1CHBF_enUS968US968&oq={parse_spaces(f"What should I do to prevent heart disease")}&gs_lcrp=EgZjaHJvbWUqBwgAEAAYgAQyBwgAEAAYgAQyBwgBEAAYgAQyDQgCEAAYhgMYgAQYigUyDQgDEAAYhgMYgAQYigXSAQg0NjExajBqN6gCALACAA&sourceid=chrome&ie=UTF-8'

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
