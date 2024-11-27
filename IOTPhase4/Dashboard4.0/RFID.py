

#Info for intensity + MQTT message
userID = ""
userTempThreshold = 35 #base value
userLightThreshold = 2000 #base value
    
def profileData():
    userData = {
        "userID": userID,
        "tempThreshold": userTempThreshold,
        "lightThreshold": userLightThreshold
    }
    return userData

def set_UserID(mqtt_message):
    global userID
    userID = mqtt_message
