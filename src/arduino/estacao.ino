#include "DHT.h"

#define DHTPIN 2
#define DHTTYPE DHT11
#define PIN_RED 9
#define PIN_GREEN 10
#define PIN_BLUE 11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(PIN_RED, OUTPUT);
  pinMode(PIN_GREEN, OUTPUT);
  pinMode(PIN_BLUE, OUTPUT);
  setLED(10, 10, 10); // Led começa branco
}

void loop() {
  if (Serial.available() > 0) {
    char comando = Serial.read();

    if (comando == 'L') { // comando que autoriza a leitura do sensor
      float umid = dht.readHumidity();
      float temp = dht.readTemperature();

      if (!isnan(umid) && !isnan(temp)) {
        float sensacao = dht.computeHeatIndex(temp, umid, false);

        // envia os dados para o monitor serial
        Serial.print("{");
        Serial.print("\"temperatura\":"); Serial.print(temp);
        Serial.print(",\"umidade\":"); Serial.print(umid);
        Serial.print(",\"sensacao\":"); Serial.print(sensacao);
        Serial.println("}");

        // cor dos leds baseada na temperatira
        if (temp < 20.0) setLED(0, 0, 255); // azul
        else if (temp <= 27.0) setLED(0, 255, 0); // verde
        else setLED(255, 0, 0); // vermelho
      }
    }
  }
}

void setLED(int r, int g, int b) {
  analogWrite(PIN_RED, r);
  analogWrite(PIN_GREEN, g);
  analogWrite(PIN_BLUE, b);
}