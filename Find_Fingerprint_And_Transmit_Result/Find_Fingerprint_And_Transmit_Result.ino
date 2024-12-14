#include <Adafruit_Fingerprint.h>
#include <SoftwareSerial.h>
#include <string.h>

#define BUILT_IN_LED  13U

typedef struct 
{
  uint8_t   id;
  uint16_t  confidence; 
} finger_detected_info_t;

typedef finger_detected_info_t finger_detected_info;

/* Set up alternative serial */
SoftwareSerial input_serial(2, 3);    /* Rx, Tx */
SoftwareSerial output_serial(4, 5);   /* Rx, Tx */

/* Define fingerprint sensor */
Adafruit_Fingerprint finger_sensor = Adafruit_Fingerprint(&input_serial);

void setup()
{
  /* Init all serials and set mode for built-in led */
  Serial.begin(9600);
  while(!Serial);
  delay(100);
  Serial.println("\n\nAdafruit finger detect test");

  output_serial.begin(9600);
  pinMode(BUILT_IN_LED, OUTPUT);

  /* Set the data rate for the sensor serial port */
  finger_sensor.begin(57600);

  /* Verify that the finger print sensor is available or not */
  if (finger_sensor.verifyPassword())
  {
    Serial.println("Found fingerprint sensor!");
  }
  else
  {
    Serial.println("Did not find fingerprint sensor!");
    while (1)
    {
      delay(1);   /* Put the program into an infinite loop */
    }
  }

  /* Get number of fingerprints have been saved */
  finger_sensor.getTemplateCount();
  Serial.print("Sensor contains "); Serial.print(finger_sensor.templateCount); Serial.println(" templates");
  Serial.println("Waiting for valid finger_sensor...");
}

void loop()                  
{
  // getFingerprintIDez();
  // getFingerprintID();
  finger_detected_info finger_info = {0U, 0U};

  getFingerprintIDSimple(&finger_info);

  if (finger_info.confidence > 0)
  {
    Serial.print("Found ID #"); Serial.print(finger_info.id); 
    Serial.print(" with confidence of "); Serial.println(finger_info.confidence);

    String output = String(finger_info.id) + ":" + String(finger_info.confidence);
    // Serial.println(output);
    output_serial.println(output);
  }

  delay(50);            
}

uint8_t getFingerprintID() {
  uint8_t p = finger_sensor.getImage();
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("Image taken");
      break;
    case FINGERPRINT_NOFINGER:
      Serial.println("No finger detected");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      return p;
    case FINGERPRINT_IMAGEFAIL:
      Serial.println("Imaging error");
      return p;
    default:
      Serial.println("Unknown error");
      return p;
  }

  // OK success!

  p = finger_sensor.image2Tz();
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("Image converted");
      break;
    case FINGERPRINT_IMAGEMESS:
      Serial.println("Image too messy");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      return p;
    case FINGERPRINT_FEATUREFAIL:
      Serial.println("Could not find fingerprint features");
      return p;
    case FINGERPRINT_INVALIDIMAGE:
      Serial.println("Could not find fingerprint features");
      return p;
    default:
      Serial.println("Unknown error");
      return p;
  }
  
  // OK converted!
  p = finger_sensor.fingerFastSearch();
  if (p == FINGERPRINT_OK) {
    Serial.println("Found a print match!");
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    Serial.println("Communication error");
    return p;
  } else if (p == FINGERPRINT_NOTFOUND) {
    Serial.println("========================================Did not find a match============================");
    return p;
  } else {
    Serial.println("Unknown error");
    return p;
  }   
  
  // found a match!
  Serial.print("Found ID #"); Serial.print(finger_sensor.fingerID); 
  Serial.print(" with confidence of "); Serial.println(finger_sensor.confidence); 

  return finger_sensor.fingerID;
}

// returns -1 if failed, otherwise returns ID #
int getFingerprintIDez() {
  uint8_t p = finger_sensor.getImage();
  if (p != FINGERPRINT_OK)  return -1;

  p = finger_sensor.image2Tz();
  if (p != FINGERPRINT_OK)  return -1;

  p = finger_sensor.fingerFastSearch();
  if (p != FINGERPRINT_OK)  return -1;
  
  // found a match!
  Serial.print("Found ID #"); Serial.print(finger_sensor.fingerID); 
  Serial.print(" with confidence of "); Serial.println(finger_sensor.confidence);
  return finger_sensor.fingerID; 
}

int16_t getFingerprintIDSimple(finger_detected_info* const info)
{
  uint8_t sensorResponse = 0U;
  
  sensorResponse = finger_sensor.getImage();
  if (sensorResponse != FINGERPRINT_OK)  return -1;

  sensorResponse = finger_sensor.image2Tz();
  if (sensorResponse != FINGERPRINT_OK)  return -1;

  sensorResponse = finger_sensor.fingerFastSearch();
  if (sensorResponse != FINGERPRINT_OK)  return -1;

  info->id = finger_sensor.fingerID;
  info->confidence = finger_sensor.confidence;

  return finger_sensor.fingerID;
}

