


#include "HX711.h"

// Pin definitions
#define DT  3  // HX711 data pin
#define SCK 2  // HX711 clock pin
#define dirPin 4
#define stepPin 0

HX711 scale;

void setup() {
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  
  Serial.begin(9600);
  scale.begin(DT, SCK);

  Serial.println("Initializing scale...");

  // Tare (zero the scale)
  //scale.set_scale();  // No calibration yet
  scale.tare();       // Reset scale to 0
  scale.set_scale(-8898.37/50); //the reading devided by the grams
  Serial.println("Tare complete. Place a known weight for calibration.");
  for(int i=0;i<10;i++){
    stepMotor(true);
  }
  
}
void stepMotor(bool dir) {
  digitalWrite(dirPin, dir);
  for (int i = 0; i < 100; i++) {  // Adjust steps per command
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(500);       // Speed
    digitalWrite(stepPin, LOW);
    delayMicroseconds(500);
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
    }
  delay(5);
}

}

//Serial.print("Raw reading: ");
  //Serial.println(scale.get_units(10)); // average of 10 readings
  //delay(1000);
