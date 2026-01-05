#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "MumurRed";
const char* password = "mumurs04005";
String serverUrl = "http://10.26.19.81:5000/verificar";

const int LED_VERDE = 2; 
const int LED_ROJO = 4;

void setup() {
  Serial.begin(115200);
  pinMode(LED_VERDE, OUTPUT);
  pinMode(LED_ROJO, OUTPUT);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    digitalWrite(LED_ROJO, HIGH); delay(100); digitalWrite(LED_ROJO, LOW);
  }
  for(int i=0; i<5; i++) { digitalWrite(LED_VERDE, HIGH); delay(50); digitalWrite(LED_VERDE, LOW); delay(50); }
}

void loop() {
  if (Serial.available() > 0) {
    String placa = Serial.readStringUntil('\n');
    placa.trim();
    if (placa.length() > 0) {
      consultarLaptop(placa);
    }
  }
}

void consultarLaptop(String placa) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");

    String postData = "placa=" + placa;
    int httpCode = http.POST(postData);

    if (httpCode > 0) {
      String payload = http.getString();
      
      Serial.println(payload); 

      if (payload.indexOf("autorizado") > 0) {
        digitalWrite(LED_VERDE, HIGH);
        delay(4000);
        digitalWrite(LED_VERDE, LOW);
      } else if (payload.indexOf("espera") > 0) {
        // Parpadeo corto amarillo (o ambos leds) indicando espera
        digitalWrite(LED_ROJO, HIGH); digitalWrite(LED_VERDE, HIGH);
        delay(1000);
        digitalWrite(LED_ROJO, LOW); digitalWrite(LED_VERDE, LOW);
      } else {
        digitalWrite(LED_ROJO, HIGH);
        delay(2000);
        digitalWrite(LED_ROJO, LOW);
      }
    } else {
      Serial.println("{\"status\":\"error\", \"msg\":\"Error WiFi ESP32\"}");
    }
    http.end();
  } else {
    Serial.println("{\"status\":\"error\", \"msg\":\"No WiFi\"}");
    WiFi.reconnect();
  }
}