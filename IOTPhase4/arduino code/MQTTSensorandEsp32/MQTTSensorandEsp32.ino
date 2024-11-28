#include <SPI.h>
#include <MFRC522.h>
#include <WiFi.h>
#include <PubSubClient.h>

// WiFi and MQTT setup
const char* ssid = "WIFINAME";
const char* password = "WIFIPASS";
const char* mqtt_server = "IPHERE";

WiFiClient espClient;
PubSubClient client(espClient);

long lastMsg = 0;
char msg[50];
int value = 0;

// RFID setup
#define SS_PIN 5  // SDA Pin on RC522
#define RST_PIN 4 // RST Pin on RC522
MFRC522 rfid(SS_PIN, RST_PIN); // Create MFRC522 instance

String data = "";  // String to store the UID data
String lastUID = ""; // String to store the last UID for comparison

// // Light sensor setup
 #define LIGHT_SENSOR_PIN  35  // ESP32 pin GPIO36 (ADC0) connected to light sensor
 #define ANALOG_THRESHOLD  2000

void setup() {
  Serial.begin(115200);
  
  // Setup WiFi
  setup_wifi();
  
  // Setup MQTT
  client.setServer(mqtt_server, 1883);

  // Setup RFID
  SPI.begin();
  rfid.PCD_Init();
  Serial.println("Place your RFID card near the reader...");

  // Setup Light Sensor
  analogSetAttenuation(ADC_11db);
  // //pinMode(LED_PIN, OUTPUT);
}

void setup_wifi() {
  delay(10);
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  // while (WiFi.status() != WL_CONNECTED) {
  //   delay(500);
  //   Serial.print(".");
  // }
  Serial.println();
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("vanieriot")) {
      Serial.println("connected to MQTT");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }

   client.loop(); // Keep the MQTT connection alive

  // Read the light sensor value
   int analogValue = analogRead(LIGHT_SENSOR_PIN);
   Serial.println(analogValue);

  // // Convert the analog value to a string and publish it to MQTT
   char message[10];
   itoa(analogValue, message, 10);
   client.publish("IoTProject/INTENSITY", message);

delay(500);
  // // // Check light sensor value and publish corresponding message
  // if (analogValue < ANALOG_THRESHOLD) {
  //   Serial.println("Message published: It is DARK");
  //    client.publish("IoTlab/SENSOR", "Light:ON");
  //   // digitalWrite(LED_PIN, HIGH); // Turn on LED
  // } else {
  //    Serial.println("Message published: Not dark");
  //    client.publish("IoTlab/SENSOR", "Light:OFF");
  //   // digitalWrite(LED_PIN, LOW);  // Turn off LED
  //  }

  // RFID card detection
  if (!rfid.PICC_IsNewCardPresent()) {
    return;
  }
  
  if (!rfid.PICC_ReadCardSerial()) {
    return;
  }

  // Initialize the current UID as a string
  String currentUID = "";

  // Store the current UID into the currentUID string
  for (byte i = 0; i < rfid.uid.size; i++) {
    if (rfid.uid.uidByte[i] < 0x10) {
      currentUID += "0"; // Add leading zero if necessary
    }
    currentUID += String(rfid.uid.uidByte[i], HEX); // Append byte as hex
  }

  // Check if the current UID is different from the last one
  if (currentUID != lastUID) {
    // UID is different, reset 'data' string
    data = "";  // Clear the data string
    Serial.println("New card detected, resetting data.");
    data = currentUID; // Store new UID in data string

    // Publish the new UID to MQTT topic IoTProject/ID
    Serial.print("New Card UID: ");
    Serial.println(data);
    client.publish("IoTProject/ID", data.c_str()); // Publish UID to MQTT
  }

  // Update the 'lastUID' with the current UID
  lastUID = currentUID;



  // Halt PICC (Card)
  rfid.PICC_HaltA();
  //only works for the card reading
  delay(2000); // Delay for a short period to avoid flooding the serial and MQTT server

}
