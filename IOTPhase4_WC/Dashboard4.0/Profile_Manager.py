import os
from time import sleep
import json

import Email_Manager

#Info for intensity + MQTT message
profile_database = {
    "": {
        "username": "Jonkler",
        "profile_image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT9AmqnRC5e6nGOwkLsHbuRcIHgxSh2AAMCJw&s",
        "temperature_threshold": 20,
        "intensity_threshold": 2000
    },

    "2317caf7": {
        "username": "Joseph",
        "profile_image": "https://i.imgflip.com/7pmzha.jpg",
        "temperature_threshold": 20,
        "intensity_threshold": 2000
    },

    "3339cbf7": {
        "username": "Willit",
        "profile_image": "https://i.imgflip.com/7pmzha.jpg",
        "temperature_threshold": 20,
        "intensity_threshold": 2000
    },

    "23c3ccf7": {
        "username": "Arjun",
        "profile_image": "lnk",
        "temperature_threshold": 20,
        "intensity_threshold": 2000
    },

    "c34ad524": {
        "username": "JOnkler",
        "profile_image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT9AmqnRC5e6nGOwkLsHbuRcIHgxSh2AAMCJw&s",
        "temperature_threshold": 22,
        "intensity_threshold": 2200
    }
}

userID = ""
userTempThreshold = 35 #base value
userLightThreshold = 2000 #base value
    
def profileData():

    payload = {
        "userID": userID,
        "tempThreshold": userTempThreshold,
        "lightThreshold": userLightThreshold
    }

    if (profile_database[userID]): 
        return { "userID": userID, "data": profile_database[userID]}
    else:
        return payload

def set_Profile():
    if (profile_database[userID]): 
        userProfile = profile_database[userID]
        global userTempThreshold
        userTempThreshold = userProfile['temperature_threshold']
        global userLightThreshold
        userLightThreshold = userProfile['intensity_threshold']
        Email_Manager.send_email_profile()
    else:
        print("Please add the user.")

def set_UserID(mqtt_message):
    global userID
    userID = mqtt_message
    set_Profile()
    