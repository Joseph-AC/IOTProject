#include <SPI.h>
#include <MFRC522.h>

// Define pins for RFID module
#define SS_PIN 5  // SDA Pin on RC522
#define RST_PIN 4 // RST Pin on RC522

// Define pin for light intensity sensor
#define LIGHT_SENSOR_PIN 33  // Example: Light sensor connected to A0

// Create an MFRC522 instance
MFRC522 mfrc522(SS_PIN, RST_PIN);

// Function to read light intensity (using analog sensor)
int readLightIntensity() {
  int lightValue = analogRead(LIGHT_SENSOR_PIN);
  return lightValue;  // Return the light intensity (0-1023)
}

void setup() {
  Serial.begin(115200);  // Start serial communication at 115200 baud rate

  // Initialize RFID
  SPI.begin();
  mfrc522.PCD_Init();

  // Initialize light sensor (analog pin A0)
  pinMode(LIGHT_SENSOR_PIN, INPUT);
  
  Serial.println("RFID and Light Intensity Reader Ready!");
}

void loop() {
  // Look for new RFID cards
  if (mfrc522.PICC_IsNewCardPresent()) {
    if (mfrc522.PICC_ReadCardSerial()) {
      String rfid_tag = "";
      for (byte i = 0; i < mfrc522.uid.size; i++) {
        rfid_tag += String(mfrc522.uid.uidByte[i], HEX);  // Get UID in hex format
      }

      // Read light intensity
      int light_intensity = readLightIntensity();

      // Send RFID and light intensity to Python via serial
      Serial.print(rfid_tag);  // Send RFID tag
      Serial.print(",");       // Separator between RFID and light intensity
      Serial.println(light_intensity);  // Send light intensity
    }
  }
}
