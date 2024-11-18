#include <WiFi.h>
#include <PubSubClient.h>
// Replace the next variables with your SSID/Password combination
const char* ssid = "PUT_WIFI_NAME";
const char* password = "PUT_WIFI_PASSWORD";
// Add your MQTT Broker IP address, example:
const char* mqtt_server = "PUT_IP_HERE";
WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;
// LED Pin

#define LIGHT_SENSOR_PIN  35 // ESP32 pin GPIO36 (ADC0) connected to light sensor
#define LED_PIN           26  // ESP32 pin GPIO22 connected to LED
#define ANALOG_THRESHOLD  2000
void setup() {
 Serial.begin(115200);
 setup_wifi();
//Install this library
 client.setServer(mqtt_server, 1883);
analogSetAttenuation(ADC_11db);
  pinMode(LED_PIN, OUTPUT);
}
void setup_wifi() {
 delay(10);
 // We start by connecting to a WiFi network
 Serial.println();
 Serial.print("Connecting to ");
 Serial.println(ssid);
 WiFi.begin(ssid, password);
 while (WiFi.status() != WL_CONNECTED) {
 delay(500);
 Serial.print(".");
 }
 Serial.println("");
 Serial.println("WiFi connected");
 Serial.println("IP address: ");
 Serial.println(WiFi.localIP());
}
/*
void callback(char* topic, byte* message, unsigned int length) {    
 Serial.print("Message arrived on topic: ");
 Serial.print(topic);
 Serial.print(". Message: ");
 String messagein;

 for (int i = 0; i < length; i++) {
 Serial.print((char)message[i]);
 messagein += (char)message[i];
 }
 if(topic=="room/light"){
 if (messagein == "ON")
 Serial.println("Light is ON");
 }else{
 Serial.println("Light is OFF");
 }
 
}*/
void reconnect() {
 while (!client.connected()) {
 Serial.print("Attempting MQTT connection...");
 if (client.connect("vanieriot")) {
 Serial.println("connected vanieriot");
 client.subscribe("room/light",0);
 
 } else {
 Serial.print("failed, rc=");
 Serial.print(client.state());
 Serial.println(" try again in 5 seconds");
 // Wait 5 seconds before retrying
 delay(5000);
 }
 }
}
void loop() {
 if (!client.connected()) {
 reconnect();
 }

 if(!client.loop())
 client.connect("vanieriot");

 //client.subscribe("room/light",0); 

int analogValue = analogRead(LIGHT_SENSOR_PIN); // read the value on analog pin
    Serial.println(analogValue);
    //to convert
    char message[10];
    itoa(analogValue, message, 10);
    client.publish("IoTlab/INTENSITY",message);

  if (analogValue < ANALOG_THRESHOLD){
     Serial.println("Message published: It is DARK");
    client.publish("IoTlab/SENSOR","Light:ON");
   // digitalWrite(LED_PIN, HIGH); // turn on LED
  //  Serial.print("HIGH");
  }
  else{
     Serial.println("Message published: Not dark");
    client.publish("IoTlab/SENSOR","Light:OFF");
   // digitalWrite(LED_PIN, LOW);  // turn off LED
    //Serial.print("LOW");
  }
 delay(1000);
 }
