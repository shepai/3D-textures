


#include "HX711.h"

// Pin definitions
#define DT  3  // HX711 data pin
#define SCK 2  // HX711 clock pin
#define dirPin 4
#define stepPin 5
#define enable 8

HX711 scale;

void setup() {
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(enable, OUTPUT);
  digitalWrite(enable,0);
  
  Serial.begin(921600);
  Serial.println("Testing...");
  scale.begin(DT, SCK);

  //Serial.println("Initializing scale...");

  // Tare (zero the scale)
  //scale.set_scale();  // No calibration yet
  scale.tare();       // Reset scale to 0
  scale.set_scale(-64991.41/50); //the reading devided by the grams
  //Serial.println("Tare complete. Place a known weight for calibration.");
  
}
void stepMotor(bool dir) {
  digitalWrite(dirPin, dir);
  for (int i = 0; i < 100; i++) {
    digitalWrite(stepPin, HIGH);
    delay(5);  // 5 ms high
    digitalWrite(stepPin, LOW);
    delay(5);  // 5 ms low
  }
}
void loop() {
 
  // Read raw value from HX711
  if (Serial.available()) {
    char c = Serial.read();
    if (c == 'w') {
      stepMotor(true);
    } else if (c == 's') {
      stepMotor(false);
      
    }else if (c == 'r') {
      Serial.println(scale.get_units(10));
    }
  }
  


}

//Serial.print("Raw reading: ");
  //Serial.println(scale.get_units(10)); // average of 10 readings
  //delay(1000);
