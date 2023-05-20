#include <ESP8266HTTPClient.h>

#include <ArduinoJson.h>

#include <ESP8266WebServer.h>
#include <ESP8266WiFi.h>
#include <Ticker.h>
#include <Wire.h>

// <-------------------- I2C  funkciji zacetek -------------------------->
void I2CWriteRegister(uint8_t I2CDevice, uint8_t RegAdress, uint8_t Value)
{
    // I2CDevice - Naslov I2C naprave
    // RegAddress - Naslov registra
    // Value - Vrednost za vpisati v register

    Wire.beginTransmission(I2CDevice);
    // Napravi sporočimo naslov registra, s katerega želimo brati:
    Wire.write(RegAdress);
    // Posljemo vrednost
    Wire.write(Value);
    Wire.endTransmission();
}

void I2CReadRegister(uint8_t I2CDevice, uint8_t RegAdress, uint8_t NBytes, uint8_t* Value)
{
    Wire.beginTransmission(I2CDevice);
    // Napravi sporočimo naslov registra, s katerega želimo brati:
    Wire.write(RegAdress);
    // Končamo prenos:
    Wire.endTransmission();

    // Napravi sporočimo, da želimo prebrati določeno število 8-bitnih registrov:
    Wire.requestFrom(I2CDevice, NBytes);
    for (int q = 0; q < NBytes; q++) {
        // Preberemo naslednji 8-bitni register oz. naslednji bajt:
        *Value = (uint8_t)Wire.read();
        Value++;
        // uint32_t vrednost = Wire.read();
    }
    // maybe sam to stran?
}

// <-------------------- I2C  Funkcije konec -------------------------->

// Naslov MPU9250 na I2C vodilu
#define MPU_ADD 104
// Naslov registra za pospesek
#define ACC_MEAS_REG 59
// Naslov registra za ziroskop
#define GYRO_MEAS_REG 67

// Stevilo uzorcev za kalibracijo
#define CAL_NO 1000
// Stevilo uzorcev za branje
#define READ_NO 10
// Globalni stevec zanke
uint8_t iter = 0;

// Meritve sa senzorja
uint8_t gyroMeas[] = { 0, 0, 0, 0, 0, 0 };

// Meritve za senzorj pospeškomer
uint8_t accMeas[] = { 0, 0, 0, 0, 0, 0 };

Ticker readSensorGyro;
Ticker readSensorAcc;

// Kalibracione vrednosti
float gyroX_off = 0;
float gyroY_off = 0;
float gyroZ_off = 0;
// Meritve
float gyroX, gyroY, gyroZ;

// Kalibracione vrednosti ACC
float accX_off = 0;
float accY_off = 0;
float accZ_off = 0;
// Meritve ACC
float accX, accY, accZ;
int acc_counter = 0; // Global counter to keep track of readings
int gyro_counter = 0;
const int numReadings = 10; // Number of readings to save
const int SIZE = JSON_ARRAY_SIZE(numReadings * 4);
float accReadings[numReadings][3]; // Array to store the accelerometer readings (X, Y, Z)
float gyroReadings[numReadings][3]; // Array to store the gyroscope readings (X, Y, Z)

// make bool ready
bool readyAccData = false;
bool readyGyroData = false;

enum State {
    IDLE,
    ANALYZE,
    TRACK
};

bool isTracking = false;
bool isDataCollecting = false;

float duration = 0.5;
float read_rate = 0.05;

void MPU9250_init()
{
    // Resetiraj MPU9250 senzora => Register PWR_MGMT_1 (107)
    I2CWriteRegister(MPU_ADD, 107, 128); // 128 = 1000 0000
    // Pocakaj
    delay(500);
    // Preveri ID od senzora => Register WHO_AM_I (117)
    uint8_t ID;
    I2CReadRegister(MPU_ADD, 117, 1, &ID);
    Serial.println("ID:");
    Serial.println(ID, HEX);
    // Gyroscope Conf => Register GYRO_CONFIG (27)
    // 4 in 3 bit dolocata obseg
    I2CWriteRegister(MPU_ADD, 27, 0); //
    delay(100);
    // Accelerator Conf => Register ACCEL_CONFIG (28)
    // 4 in 3 bit dolocata obseg
    // Opciono => Register ACCEL_CONFIG_2 (29)
    I2CWriteRegister(MPU_ADD, 28, 0); //
    delay(100);
}

void calibrateGyro()
{

    uint32_t ITER = 1000; // Stevilo uzorcev za glajenje
    int32_t tmp;
    Serial.println("Kalibracija ziroskopa");
    for (int i = 0; i < CAL_NO; i++) {
        I2CReadRegister(MPU_ADD, GYRO_MEAS_REG, 6, gyroMeas);
        // GYRO_XOUT = Gyro_Sensitivity * X_angular_rate
        tmp = (((int8_t)gyroMeas[0] << 8) + (uint8_t)gyroMeas[1]);
        gyroX_off += tmp * 1.0 / 131.0;
        // GYRO_YOUT = Gyro_Sensitivity * Y_angular_rate
        tmp = (((int8_t)gyroMeas[2] << 8) + (uint8_t)gyroMeas[3]);
        gyroY_off += tmp * 1.0 / 131.0;
        // GYRO_ZOUT = Gyro_Sensitivity * Z_angular_rate
        tmp = (((int8_t)gyroMeas[4] << 8) + (uint8_t)gyroMeas[5]);
        gyroZ_off += tmp * 1.0 / 131.0;
        Serial.print(".");
    }
    Serial.println("Konec kalibracije");

    gyroX_off /= CAL_NO;
    gyroY_off /= CAL_NO;
    gyroZ_off /= CAL_NO;

    Serial.println("Ziroskop X osa");
    Serial.println(gyroX_off);
    Serial.println("Ziroskop Y osa");
    Serial.println(gyroY_off);
    Serial.println("Ziroskop Z osa");
    Serial.println(gyroZ_off);
}

void readGyro()
{
    int32_t tmp;
    I2CReadRegister(MPU_ADD, GYRO_MEAS_REG, 6, gyroMeas); // preberi vse podatke gyrota
    // GYRO_XOUT = Gyro_Sensitivity * X_angular_rate
    tmp = (((int8_t)gyroMeas[0] << 8) + (uint8_t)gyroMeas[1]); // spravi high in low, ki je v enem bytu v eno 16 bitno spremenljivko (konkateniraš jih ubistvu)
    gyroX = tmp * 1.0 / 131.0;
    // GYRO_YOUT = Gyro_Sensitivity * Y_angular_rate
    tmp = (((int8_t)gyroMeas[2] << 8) + (uint8_t)gyroMeas[3]);
    gyroY = tmp * 1.0 / 131.0;
    // GYRO_ZOUT = Gyro_Sensitivity * Z_angular_rate
    tmp = (((int8_t)gyroMeas[4] << 8) + (uint8_t)gyroMeas[5]);
    gyroZ = tmp * 1.0 / 131.0;
    /* Serial.print("Gyro X: ");
    Serial.print(gyroX);
    Serial.print(" Y: ");
    Serial.print(gyroY);
    Serial.print(" Z: ");
    Serial.println(gyroZ); */

    gyroReadings[gyro_counter % numReadings][0] = gyroX;
    gyroReadings[gyro_counter % numReadings][1] = gyroY;
    gyroReadings[gyro_counter % numReadings][2] = gyroZ;

    gyro_counter++;
    if (gyro_counter % numReadings == 0) {
        readyGyroData = true;
    }
}

void calibrateAcc()
{
    // TODO kle bi mogu še upoštevat da je skos pospešek g pri z osi

    uint32_t ITER = 1000; // Stevilo uzorcev za glajenje
    int32_t tmp;
    Serial.println("Kalibracija pospekomera");
    for (int i = 0; i < CAL_NO; i++) {
        I2CReadRegister(MPU_ADD, ACC_MEAS_REG, 6, accMeas);
        // GYRO_XOUT = Gyro_Sensitivity * X_angular_rate
        tmp = (((int8_t)accMeas[0] << 8) + (uint8_t)accMeas[1]);
        accX_off += tmp; // kle mors delit?
                         // GYRO_YOUT = Gyro_Sensitivity * Y_angular_rate
        tmp = (((int8_t)accMeas[2] << 8) + (uint8_t)accMeas[3]);
        accY_off += tmp;
        // GYRO_ZOUT = Gyro_Sensitivity * Z_angular_rate
        tmp = (((int8_t)accMeas[4] << 8) + (uint8_t)accMeas[5]);
        accZ_off += tmp;
    }
    Serial.println("Konec kalibracije");

    accX_off /= CAL_NO;
    accY_off /= CAL_NO;
    accZ_off /= CAL_NO;

    /* Serial.println("Pospeskomer X os");
    Serial.println(accX_off);
    Serial.println("Pospeskomer Y os");
    Serial.println(accY_off);
    Serial.println("Pospeskomer Z os");
    Serial.println(accZ_off); */
}

void readAcc()
{
    int32_t tmp;
    I2CReadRegister(MPU_ADD, ACC_MEAS_REG, 6, accMeas); // preberi vse podatke iz pospeškomera
    float pretvornik = 10.0 / 16384.0;
    // X_angular_rate
    tmp = (((int8_t)accMeas[0] << 8) + (uint8_t)accMeas[1]); // spravi high in low, ki je v enem bytu v eno 16 bitno spremenljivko (konkateniraš jih ubistvu)
    accX = tmp - accX_off;
    accX = accX * pretvornik;

    // Y_angular_rate
    tmp = (((int8_t)accMeas[2] << 8) + (uint8_t)accMeas[3]);
    accY = tmp - accY_off;
    accY = accY * pretvornik;

    // Z_angular_rate
    tmp = (((int8_t)accMeas[4] << 8) + (uint8_t)accMeas[5]);
    accZ = tmp - accZ_off;
    accZ = accZ * pretvornik;
    // Serial.print("a");

    accReadings[acc_counter % numReadings][0] = accX;
    accReadings[acc_counter % numReadings][1] = accY;
    accReadings[acc_counter % numReadings][2] = accZ;

    acc_counter++;
    if (acc_counter % numReadings == 0) {
        readyAccData = true;
    }

    // izpisi meritve na serijsko
    /* Serial.print("Acc X: ");
    Serial.print(accX);
    Serial.print(" Y: ");
    Serial.print(accY);
    Serial.print(" Z: ");
    Serial.println(accZ); */
}

// wifi setup
// Ime dostopne točke:
const char AP_NameChar[] = "dostopna_tocka";
// Geslo dostopne točke:
const char AP_WiFiAPPSK[] = "geslo123";

// "kreiramo" server na portu 80:
// WiFiServer server(80);
ESP8266WebServer server(80);

// Initialize the HTTPClient object
HTTPClient http;
WiFiClient client;

void setupWiFiAP()
{
    WiFi.mode(WIFI_AP);
    WiFi.softAP(AP_NameChar, AP_WiFiAPPSK);
    delay(500);
    Serial.println("Dostopna tocka postavljena.");
    Serial.println("------------------------");
    Serial.print("AP name: ");
    Serial.println(AP_NameChar);
    Serial.print("AP password: ");
    Serial.println(AP_WiFiAPPSK);
    Serial.print("IP naslov: ");
    // IPAddress myIP = WiFi.softAPIP();
    Serial.println(WiFi.softAPIP());
    Serial.print("Gateway: ");
    Serial.println(WiFi.gatewayIP());
    Serial.println("------------------------");
}

// Track label variable
String trackLabel;

// char* serverUrl = "http://192.168.4.2:8080"; // Replace with your server URL
const String serverUrl = "http://192.168.4.2:8080";

// Create a flag to indicate if the track label is received

void handleDataCollection()
{
    // Handle the "/track" endpoint
    String dataCollectionPage = "<html><body>";
    dataCollectionPage += "<h1>Data Collection</h1>";
    dataCollectionPage += "<form method='post' action='/start-collecting'>";
    dataCollectionPage += "<label for='label'>Select Track Label:</label>";
    dataCollectionPage += "<select id='label' name='label'>";
    dataCollectionPage += "<option value='Walking'>Walking</option>";
    dataCollectionPage += "<option value='Running'>Running</option>";
    dataCollectionPage += "<option value='Cycling'>Cycling</option>";
    dataCollectionPage += "</select>";
    dataCollectionPage += "</form>";
    dataCollectionPage += "<button type='submit' id='startBtn' onclick='startCollecting();'>Start collecting data</button>";
    dataCollectionPage += "<button id='stopBtn' onclick='stopCollecting();' disabled>Stop collecting data</button>";
    dataCollectionPage += "<script>";
    dataCollectionPage += "function startCollecting() {";
    dataCollectionPage += "document.getElementById('startBtn').disabled = true;";
    dataCollectionPage += "document.getElementById('stopBtn').disabled = false;";
    dataCollectionPage += "var label = document.getElementById('label').value;";
    dataCollectionPage += "var xhr = new XMLHttpRequest();";
    dataCollectionPage += "xhr.open('POST', '/start-collecting', true);";
    dataCollectionPage += "xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');";
    dataCollectionPage += "xhr.send('label=' + encodeURIComponent(label));";
    dataCollectionPage += "}";
    dataCollectionPage += "function stopCollecting() {";
    dataCollectionPage += "document.getElementById('startBtn').disabled = false;";
    dataCollectionPage += "document.getElementById('stopBtn').disabled = true;";
    dataCollectionPage += "var xhr = new XMLHttpRequest();";
    dataCollectionPage += "xhr.open('GET', '/stop-collecting', true);";
    dataCollectionPage += "xhr.send();";
    dataCollectionPage += "}";
    dataCollectionPage += "</script>";
    dataCollectionPage += "</body></html>";

    server.send(200, "text/html", dataCollectionPage);
}
const unsigned long interval = 1000; // Interval between requests in milliseconds

void handleTrack()
{
    String htmlPage = "<html><head><title>Activity Tracking</title>";
    htmlPage += "<script>";
    htmlPage += "function startTracking() {";
    htmlPage += "var xhr = new XMLHttpRequest();";
    htmlPage += "xhr.open('GET', '/start-tracking', true);";
    htmlPage += "xhr.send();";
    htmlPage += "document.getElementById('startBtn').disabled = true;";
    htmlPage += "document.getElementById('stopBtn').disabled = false;";
    htmlPage += "intervalId = setInterval(fetchActivity, 1000);";
    htmlPage += "}";
    htmlPage += "function stopTracking() {";
    htmlPage += "clearInterval(intervalId);";
    htmlPage += "var xhr = new XMLHttpRequest();";
    htmlPage += "xhr.open('GET', '/stop-tracking', true);";
    htmlPage += "xhr.send();";
    htmlPage += "document.getElementById('startBtn').disabled = false;";
    htmlPage += "document.getElementById('stopBtn').disabled = true;";
    htmlPage += "}";
    htmlPage += "function fetchActivity() {";
    htmlPage += "var xhr = new XMLHttpRequest();";
    htmlPage += "xhr.open('GET', '/last-activity', true);";
    htmlPage += "xhr.onreadystatechange = function() {";
    htmlPage += "if (xhr.readyState === 4 && xhr.status === 200) {";
    htmlPage += "var response = JSON.parse(xhr.responseText);";
    htmlPage += "document.getElementById('result').value = response.activity_type;";
    htmlPage += "}";
    htmlPage += "};";
    htmlPage += "xhr.send();";
    htmlPage += "}";
    htmlPage += "</script>";
    htmlPage += "</head><body>";
    htmlPage += "<h1>Activity Tracking</h1>";
    htmlPage += "<input type='text' id='result' readonly />";
    htmlPage += "<br><br>";
    htmlPage += "<button id='startBtn' onclick='startTracking();'>Start Tracking</button>";
    htmlPage += "<button id='stopBtn' onclick='stopTracking();' disabled>Stop Tracking</button>";
    htmlPage += "</body></html>";

    server.send(200, "text/html", htmlPage);
}

void handleHistory()
{

    /* DynamicJsonDocument doc(1024);

    // Add data for each day and sport
    doc["mon"]["running"]["minutes"] = 100;
    doc["mon"]["running"]["calories"] = 500;
    doc["mon"]["running"]["distance"] = 1000;

    doc["mon"]["cycling"]["minutes"] = 100;
    doc["mon"]["cycling"]["calories"] = 500;
    doc["mon"]["cycling"]["distance"] = 1000;

    doc["mon"]["walking"]["minutes"] = 100;
    doc["mon"]["walking"]["calories"] = 500;
    doc["mon"]["walking"]["distance"] = 1000;

    doc["tue"]["running"]["minutes"] = 100;
    doc["tue"]["running"]["calories"] = 500;
    doc["tue"]["running"]["distance"] = 1000;

    doc["tue"]["cycling"]["minutes"] = 100;
    doc["tue"]["cycling"]["calories"] = 500;
    doc["tue"]["cycling"]["distance"] = 1000;

    doc["tue"]["walking"]["minutes"] = 100;
    doc["tue"]["walking"]["calories"] = 500;
    doc["tue"]["walking"]["distance"] = 1000;

    String json;
    serializeJson(doc, json); */

    // Make a GET request
    http.begin(client, serverUrl + "/weekly-data");
    int httpResponseCode = http.GET();

    if (httpResponseCode == 200) {
        String jsonResponse = http.getString();
        Serial.println(jsonResponse);
        String htmlPage = "<!DOCTYPE html> <html> <script src='https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.5.0/Chart.min.js'></script> <body> <div style='display: flex; justify-content: space-between; max-width: 1200px; margin-bottom: 20px;'> <canvas id='minutesChart' style='width: 400px;'></canvas> <canvas id='caloriesChart' style='width: 400px;'></canvas> <canvas id='distanceChart' style='width: 400px;'></canvas> </div> <script> var data = " + jsonResponse + "; var days = Object.keys(data); var sports = Object.keys(data[days[0]]); var barColors = ['red', 'green', 'blue']; var minutesData = sports.map(function(sport) { return days.map(function(day) { return data[day][sport].minutes; }); }); var caloriesData = sports.map(function(sport) { return days.map(function(day) { return data[day][sport].calories; }); }); var distanceData = sports.map(function(sport) { return days.map(function(day) { return data[day][sport].distance; }); }); new Chart('minutesChart', { type: 'bar', data: { labels: days, datasets: sports.map(function(sport, index) { return { label: sport, backgroundColor: barColors[index], data: minutesData[index] }; }) }, options: { title: { display: true, text: 'Activity Minutes by Sport' }, scales: { yAxes: [{ ticks: { beginAtZero: true } }] } } }); new Chart('caloriesChart', { type: 'bar', data: { labels: days, datasets: sports.map(function(sport, index) { return { label: sport, backgroundColor: barColors[index], data: caloriesData[index] }; }) }, options: { title: { display: true, text: 'Calories Burned by Sport' }, scales: { yAxes: [{ ticks: { beginAtZero: true } }] } } }); new Chart('distanceChart', { type: 'bar', data: { labels: days, datasets: sports.map(function(sport, index) { return { label: sport, backgroundColor: barColors[index], data: distanceData[index] }; }) }, options: { title: { display: true, text: 'Distance Covered by Sport' }, scales: { yAxes: [{ ticks: { beginAtZero: true } }] } } }); </script> </body> </html>";
        // String htmlPage = "<!DOCTYPE html> <html> <script src='https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.5.0/Chart.min.js'></script> <body> <div style='max-width: 1200px; margin-bottom: 20px;'> <canvas id='minutesChart' style='width: 100%;'></canvas> </div> <div style='max-width: 1200px; margin-bottom: 20px;'> <canvas id='caloriesChart' style='width: 100%;'></canvas> </div> <div style='max-width: 1200px; margin-bottom: 20px;'> <canvas id='distanceChart' style='width: 100%;'></canvas> </div> <script> var data = " + jsonResponse + "; var days = Object.keys(data); var sports = Object.keys(data[days[0]]); var barColors = ['red', 'green', 'blue']; // Prepare data for each sport var minutesData = sports.map(function(sport) { return days.map(function(day) { return data[day][sport].minutes; }); }); var caloriesData = sports.map(function(sport) { return days.map(function(day) { return data[day][sport].calories; }); }); var distanceData = sports.map(function(sport) { return days.map(function(day) { return data[day][sport].distance; }); }); new Chart('minutesChart', { type: 'bar', data: { labels: days, datasets: sports.map(function(sport, index) { return { label: sport, backgroundColor: barColors[index], data: minutesData[index] }; }) }, options: { title: { display: true, text: 'Activity Minutes by Sport' }, scales: { yAxes: [{ ticks: { beginAtZero: true } }] } } }); new Chart('caloriesChart', { type: 'bar', data: { labels: days, datasets: sports.map(function(sport, index) { return { label: sport, backgroundColor: barColors[index], data: caloriesData[index] }; }) }, options: { title: { display: true, text: 'Calories Burned by Sport' }, scales: { yAxes: [{ ticks: { beginAtZero: true } }] } } }); // Create distance chart new Chart('distanceChart', { type: 'bar', data: { labels: days, datasets: sports.map(function(sport, index) { return { label: sport, backgroundColor: barColors[index], data: distanceData[index] }; }) }, options: { title: { display: true, text: 'Distance Covered by Sport' }, scales: { yAxes: [{ ticks: { beginAtZero: true } }] } } }); </script> </body> </html>";
        server.send(200, "text/html", htmlPage);
    } else {
        server.send(500, "text/plain", "Error retrieving last activity");
    }

    // End the HTTP connection
    http.end();
}

void handleStartTracking()
{
    Serial.println("Start tracking");
    // Branje gyro senzorja
    readSensorGyro.attach(read_rate, readGyro);
    // Branje acc senzorja
    readSensorAcc.attach(read_rate, readAcc);
}

void handleStopTracking()
{
    Serial.println("Stop tracking");
    readSensorGyro.detach();
    readSensorAcc.detach();
}

void handleLastActivity()
{
    // DynamicJsonDocument doc(128);
    // doc["activity_type"] = "running";
    // String json;
    // serializeJson(doc, json);

    // server.send(200, "application/json", json);

    // Make a GET request
    http.begin(client, serverUrl + "/predict");
    int httpResponseCode = http.GET();

    if (httpResponseCode == 200) {
        String jsonResponse = http.getString();
        server.sendHeader("Content-Type", "application/json");
        server.send(200, "application/json", jsonResponse);
    } else {
        server.send(500, "text/plain", "Error retrieving last activity");
    }

    // End the HTTP connection
    http.end();
}

void handleStartCollecting()
{
    // Handle the "/start-collecting" endpoint
    if (server.hasArg("label")) {
        trackLabel = server.arg("label");
        Serial.println("Start collecting data for " + trackLabel);
        // Branje gyro senzorja
        readSensorGyro.attach(read_rate, readGyro);
        // Branje acc senzorja
        readSensorAcc.attach(read_rate, readAcc);
        isDataCollecting = true;
    }
}

void handleStopCollecting()
{
    // Handle the "/stop-collecting" endpoint
    Serial.println("Stop collecting data");
    readSensorGyro.detach();
    readSensorAcc.detach();
    isDataCollecting = false;
    // change the server url to /save-csv endpoint

    // Make a PUT request
    http.begin(client, serverUrl + "/save-csv");
    // Set the Content-Type header to indicate JSON data
    http.addHeader("Content-Type", "text/plain");

    // Send the PUT request without any JSON data
    int httpResponseCode = http.PUT("");

    if (httpResponseCode == HTTP_CODE_OK) {
        // Request successful
        String response = http.getString();
        Serial.println("Response: " + response);
    } else {
        // Request failed
        Serial.println("Error: " + http.errorToString(httpResponseCode));
    }

    // End the request
    http.end();
}

void setupWebServer()
{
    // Setup server
    server.on("/", []() {
        server.send(200, "text/plain", "Hello World!");
    });

    server.on("/data-collection", handleDataCollection);
    server.on("/tracking", handleTrack);
    server.on("/last-activity", handleLastActivity);
    server.on("/start-tracking", handleStartTracking);
    server.on("/stop-tracking", handleStopTracking);
    server.on("/start-collecting", handleStartCollecting);
    server.on("/stop-collecting", handleStopCollecting);
    server.on("/history", handleHistory);

    // Start the server
    server.begin();
}

// compute the required size
const size_t CAPACITY = JSON_ARRAY_SIZE(numReadings) + numReadings * JSON_OBJECT_SIZE(3) + 1024; // add buffer for the JSON document
void sendData(char* type)
{
    // Serial.println("Sending data to server...");
    //  Clear the JSON object

    // create an empty array
    // Create a JSON object
    StaticJsonDocument<CAPACITY> doc;
    JsonObject root = doc.to<JsonObject>();
    JsonArray array = root.createNestedArray(type);

    if (strcmp(type, "gyro") == 0) {
        for (int i = 0; i < numReadings; i++) {
            JsonObject obj1 = array.createNestedObject();
            obj1["x"] = accReadings[i][0];
            obj1["y"] = accReadings[i][1];
            obj1["z"] = accReadings[i][2];
            obj1["duration"] = read_rate * numReadings;
            if (isDataCollecting) {
                obj1["label"] = trackLabel;
            }
        }
    }

    if (strcmp(type, "acc") == 0) {
        for (int i = 0; i < numReadings; i++) {
            JsonObject obj1 = array.createNestedObject();
            obj1["x"] = gyroReadings[i][0];
            obj1["y"] = gyroReadings[i][1];
            obj1["z"] = gyroReadings[i][2];
            obj1["duration"] = read_rate * numReadings;
            if (isDataCollecting) {
                obj1["label"] = trackLabel;
            }
        }
    }

    String json;
    serializeJson(doc, json);
    Serial.print("serialized json: " + json);

    // Make a GET request
    if (isDataCollecting) {
        http.begin(client, serverUrl + "/data");
    } else {
        http.begin(client, serverUrl + "/tracking");
    }
    // Set the Content-Type header to indicate JSON data
    http.addHeader("Content-Type", "application/json");

    // Send the POST request with the JSON data
    int httpResponseCode = http.POST(json);

    // Check the response code
    if (httpResponseCode == 200) {
        Serial.println("Data sent successfully.");
    } else {
        Serial.print("Error sending data. Response code: ");
        Serial.println(httpResponseCode);
    }

    // End the HTTP connection
    http.end();
}

void setup()
{
    // Serijska komunikacija
    Serial.begin(115200);
    // I2C
    Wire.begin(12, 14);
    Wire.setClock(100000);

    // Podesavanje senzorja
    // https://github.com/bolderflight/mpu9250/blob/main/src/mpu9250.cpp
    MPU9250_init();

    // Kalibracija gyro
    calibrateGyro();

    // Kalibracija acc
    calibrateAcc();

    // Setup WiFi AP
    setupWiFiAP();
    setupWebServer();
}

void loop()
{
    // put your main code here, to run repeatedly:
    server.handleClient();

    if (readyAccData) {
        // Serial.println("Sending acc data");
        sendData("acc");
        readyAccData = false;
    }

    if (readyGyroData) {
        // Serial.println("Sending gyro data");
        sendData("gyro");
        readyGyroData = false;
    }
}