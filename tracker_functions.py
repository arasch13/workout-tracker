import requests
from datetime import datetime
import os


WORKOUT_SHEET_API_ENDPOINT = os.environ["WORKOUT_SHEET_API_ENDPOINT"]
NUTRITIONIX_API_ENDPOINT = os.environ["NUTRITIONIX_API_ENDPOINT"]
GENDER = "male"
WEIGHT_KG = 81
HEIGHT_CM = 1.77
AGE = 31


def write_to_sheet(result):
    api_endpoint = WORKOUT_SHEET_API_ENDPOINT
    for excercise in result['exercises']:
        sheet_input = {
            "workout": {
                'date': datetime.today().strftime("%d/%m/%Y"),
                'time': datetime.now().strftime("%H:%M:%S"),
                'exercise': excercise['name'].title(),
                'duration': excercise['duration_min'],
                'calories': excercise['nf_calories']
            }
        }
        response = requests.post(
            url=api_endpoint,
            json=sheet_input,
            auth=(os.environ["WORKOUT_SHEET_USER"], os.environ["WORKOUT_SHEET_PASSWORD"]))
        response.raise_for_status()


def add_new_workout():
    user_message = input("Tell me which excercises you did: ")
    api_endpoint = f"{NUTRITIONIX_API_ENDPOINT}/natural/exercise"
    headers = {
        "x-app-id": os.environ["NUTRITIONIX_APP_ID"],
        "x-app-key": os.environ["NUTRITIONIX_APP_KEY"],
        "Content-Type": "application/json"
    }
    parameters = {
        "query": user_message,
        "gender": GENDER,
        "weight_kg": WEIGHT_KG,
        "height_cm": HEIGHT_CM,
        "age": AGE
    }

    response = requests.post(
        url=api_endpoint, json=parameters, headers=headers)
    response.raise_for_status()
    result = response.json()
    write_to_sheet(result)
