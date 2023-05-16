#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClient.h>
#include <PubSubClient.h>
#include "config.h"

#include "tensorflow/lite/micro/all_ops_resolver.h"
#include "tensorflow/lite/micro/micro_error_reporter.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/schema/schema_generated.h"

#include "yolo.h"

WiFiClient wifiClient;
PubSubClient client(wifiClient);

namespace {
  tflite::ErrorReporter* error_reporter = nullptr;
  const tflite::Model* model = nullptr;
  tflite::MicroInterpreter* interpreter = nullptr;
  TfLiteTensor* input = nullptr;
  TfLiteTensor* output = nullptr;

  constexpr int kTensorArenaSize = 10 * 1024;
  uint8_t tensor_arena[kTensorArenaSize];

}

void callback(char* topic, byte* payload, unsigned int length){
	Serial.println("Message arrived");

	for(int i=0; i<length ; i++)
		Serial.print((char)payload[i]);
	Serial.println();
}

void setup() {
	
	Serial.begin(9600);
	Serial.println("ESP started");
	
	model = tflite::GetModel(yolo_tflite);
	WiFi.begin(SSID, WIFI_PASSWORD);

	Serial.println("Connecting to WiFi...");
	while(WiFi.status() != WL_CONNECTED){
		delay(100);	
	}
	
	Serial.println("Connected!");

	client.setServer(BROKER_IP, 1883);
	client.setCallback(callback);

	client.connect("ESP32s3");
	client.subscribe("images");
}

void loop() {
	client.loop();
}