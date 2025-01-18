#include "Arduino.h"
#include <ESP32AnalogRead.h>
#include <ArduinoBLE.h>

ESP32AnalogRead adc;
//Déclaration des pins de contrôle, du delai de lecture et du tableau de voltages
int s0 = 23;
int s1 = 22;
int s2 = 21;
int s3 = 19;
int delai = 0;
int voltages[16];

 
BLEService Transmission("ed8aa916-7657-4faf-9b83-eda02ccee33c");
BLECharacteristic mesures("97918cb5-8f6d-4247-9296-6cead3928adf", BLERead | BLENotify | BLEBroadcast,64,true);
void setup(){
  pinMode(s0, OUTPUT); 
  pinMode(s1, OUTPUT); 
  pinMode(s2, OUTPUT); 
  pinMode(s3, OUTPUT); 
  digitalWrite(s0, LOW);
  digitalWrite(s1, LOW);
  digitalWrite(s2, LOW);
  digitalWrite(s3, LOW);
  adc.attach(35);
  Serial.begin(115200);
  delay(100);
  if (!BLE.begin()) {
    Serial.println("échec de l'initiation du module Bluetooth BLE");
    while (1);
  }
  BLE.setLocalName("Espied32");
  Transmission.addCharacteristic(mesures);
  BLE.addService(Transmission);
  BLE.setAdvertisedService(Transmission);
  BLE.advertise();
}
void loop() {
  BLEDevice central = BLE.central(); //Connexion BLE
  
   while (central.connected()) {// Lit et envoi seulement lorsque connecté 
    for (int i = 0; i < 16; i++) {
      int s0_state = (i & 0x01) ? HIGH : LOW;
      int s1_state = (i & 0x02) ? HIGH : LOW;
      int s2_state = (i & 0x04) ? HIGH : LOW;
      int s3_state = (i & 0x08) ? HIGH : LOW;

      digitalWrite(s0, s0_state);
      digitalWrite(s1, s1_state);
      digitalWrite(s2, s2_state);
      digitalWrite(s3, s3_state);

      delay(delai);
      voltages[i] = adc.readMiliVolts();
      Serial.print("Voltage" + String(i + 1) + " = " + String(voltages[i]) + " ");
    }
    
    Serial.println();
    mesures.writeValue(voltages, 64);
  }
}



