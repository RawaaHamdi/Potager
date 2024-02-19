#include <WiFi.h>  
#include <PubSubClient.h>
#include <DHTesp.h>
#include <ESP32Servo.h>
const int NTC_PIN = 34; 
const int SERVO_PIN = 18;
const int DHT_PIN = 15;  
const int LDR_PIN = 35; 
char clientId[50];
DHTesp dht; 
const char* ssid = "Wokwi-GUEST"; ///  wifi ssid 
const char* password = "";
const char* mqtt_server = "broker.hivemq.com";// mosquitto server url

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
float temp = 0;
float hum = 0;


void setup_wifi() { 
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA); 
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) { 
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}
void callback(char* topic, byte* payload, unsigned int length) { 
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) { 
    Serial.print((char)payload[i]);
  }}
void mqttReconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    long r = random(1000);
    sprintf(clientId, "clientId-%ld", r);
    if (client.connect(clientId)) {
      Serial.print(clientId);
      Serial.println(" connected");
      client.subscribe("AA");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

Servo servo;
float convertToTemperature(int adcValue) {
  // Convert ADC value to resistance
  float resistance = (float)(4095 - adcValue) * 10000 / adcValue;
  // Steinhart-Hart equation to calculate temperature in Celsius
  float temperature = 1 / (log(resistance / 10000) / 3950 + 1 / 298.15) - 273.15;
  return temperature;
}
void setup() {
  pinMode(34, INPUT); // Set NTC pin as input
  pinMode(18, OUTPUT);
  
  Serial.begin(115200);
  setup_wifi(); 
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback); 
  dht.setup(DHT_PIN, DHTesp::DHT22);
    servo.attach(18, 500, 2400);
 
}
int pos = 0;

void loop() {
  if (!client.connected()) {
     mqttReconnect();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastMsg > 2000) { //perintah publish data
    lastMsg = now;
    TempAndHumidity  data = dht.getTempAndHumidity();

    String temp = String(data.temperature, 2);
    client.publish("/Thinkitive/temp", temp.c_str()); // publish temp topic /ThinkIOT/temp
    String hum = String(data.humidity, 1); 
    client.publish("/Thinkitive/hum", hum.c_str());   // publish hum topic /ThinkIOT/hum
    int ldrValue = analogRead(LDR_PIN);
    String ldrStr = String(ldrValue);
    client.publish("/Thinkitive/ldr", ldrStr.c_str());
      // Read NTC sensor value
    int ntcValue = analogRead(NTC_PIN);
    // Convert analog reading to temperature in Celsius
    float temperature = convertToTemperature(ntcValue);
    // Convert temperature to String
    String ntcStr = String(temperature, 2);
    // Publish temperature to MQTT topic
    client.publish("/Thinkitive/ntc", ntcStr.c_str());


    Serial.print("Temperature: ");
    Serial.println(temp);
    Serial.print("Humidity: ");
    Serial.println(hum);
     Serial.print("LDR Value: ");
    Serial.println(ldrStr);
    Serial.print("NTC Temperature: ");
    Serial.println(ntcStr);
     for (pos = 0; pos <= 180; pos += 1) {
    servo.write(pos);
    delay(15);
  }
  for (pos = 180; pos >= 0; pos -= 1) {
    servo.write(pos);
    delay(15);
  }
  
    
  
   
  }
}