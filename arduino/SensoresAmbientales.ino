#include <DHT.h>

// Pines
const int dhtPin = 2;        // DHT11 en pin digital 2
const int mq135Pin = A0;     // MQ135 en pin analógico A0

// Tipo de sensor DHT
#define DHTTYPE DHT11
DHT dht(dhtPin, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  // Leer temperatura y humedad
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  // Leer calidad de aire (valor analógico)
  int mq135Value = analogRead(mq135Pin);

  // Validar lecturas del DHT11
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("ERROR");
  } else {
    // Enviar como JSON en una sola línea (fácil de leer en Python)
    Serial.print("{\"temperature\":");
    Serial.print(temperature, 1);
    Serial.print(",\"humidity\":");
    Serial.print(humidity, 1);
    Serial.print(",\"air_quality\":");
    Serial.print(mq135Value);  // valor entre 0 y 1023
    Serial.println("}");
  }

  delay(1000); // 1 segundo entre lecturas
}
