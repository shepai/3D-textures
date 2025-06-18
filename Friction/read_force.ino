#include "HX711.h"

// Pin definitions
#define DT  3  // HX711 data pin
#define SCK 2  // HX711 clock pin

HX711 scale;

void setup() {
  Serial.begin(9600);
  scale.begin(DT, SCK);

  Serial.println("Initializing scale...");

  // Tare (zero the scale)
  scale.set_scale();  // No calibration yet
  scale.tare();       // Reset scale to 0

  Serial.println("Tare complete. Place a known weight for calibration.");
}

void loop() {
  // Read raw value from HX711
  Serial.print("Raw reading: ");
  Serial.println(scale.get_units(10)); // average of 10 readings

  delay(1000);
}
