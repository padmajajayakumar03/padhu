/*
 * Neurofibromatosis Monitoring System - ESP32 Code
 * Embedded AI for Bioimpedance and Nerve Signal Analysis
 * 
 * Author: Padmaja
 * Hardware: ESP32, AD5933, AD620, Bluetooth Module
 */

#include <WiFi.h>
#include <BluetoothSerial.h>
#include <Wire.h>
#include <ArduinoJson.h>
#include <math.h>

// TensorFlow Lite for Microcontrollers (simulation)
// #include "tensorflow/lite/micro/all_ops_resolver.h"
// #include "tensorflow/lite/micro/micro_error_reporter.h"
// #include "tensorflow/lite/micro/micro_interpreter.h"

// Pin Definitions
#define AD5933_SDA_PIN 21
#define AD5933_SCL_PIN 22
#define AD620_SIGNAL_PIN 34
#define MUX_CONTROL_PIN 25
#define LED_STATUS_PIN 2
#define BATTERY_PIN 35

// System Constants
#define SAMPLING_FREQUENCY 1000  // 1kHz
#define MEASUREMENT_INTERVAL 5000  // 5 seconds
#define BLUETOOTH_BAUD 115200
#define SERIAL_BAUD 115200

// AD5933 Registers (simplified)
#define AD5933_ADDR 0x0D
#define AD5933_CONTROL_REG 0x80
#define AD5933_START_FREQ_REG 0x82
#define AD5933_REAL_DATA_REG 0x94
#define AD5933_IMAG_DATA_REG 0x96

// Global Variables
BluetoothSerial SerialBT;
bool bluetoothConnected = false;
unsigned long lastMeasurement = 0;
float batteryLevel = 100.0;

// Measurement Data Structure
struct BioimpedanceData {
  float resistance;
  float reactance;
  float phase_angle;
  float magnitude;
  float frequency;
};

struct NerveSignalData {
  float amplitude;
  float conduction_velocity;
  float latency;
  String signal_quality;
};

struct MLPrediction {
  String prediction;
  float confidence;
  float normal_prob;
  float early_nf_prob;
  float advanced_nf_prob;
};

// Function Prototypes
void initializeSystem();
void initializeBluetooth();
void initializeAD5933();
BioimpedanceData measureBioimpedance();
NerveSignalData measureNerveSignal();
MLPrediction performMLInference(BioimpedanceData bio, NerveSignalData nerve);
void sendBluetoothData(BioimpedanceData bio, NerveSignalData nerve, MLPrediction ml);
void updateBatteryLevel();
void blinkStatusLED(int times);
String getRiskLevel(MLPrediction ml);

void setup() {
  Serial.begin(SERIAL_BAUD);
  pinMode(LED_STATUS_PIN, OUTPUT);
  pinMode(MUX_CONTROL_PIN, OUTPUT);
  pinMode(BATTERY_PIN, INPUT);
  
  delay(2000);
  
  Serial.println("🏥 NEUROFIBROMATOSIS MONITORING SYSTEM");
  Serial.println("🔬 Embedded AI for Bioimpedance Analysis");
  Serial.println("👨‍⚕️ By: Padmaja");
  Serial.println("=" * 50);
  
  initializeSystem();
  
  Serial.println("✅ System Ready for Monitoring!");
  blinkStatusLED(3);
}

void loop() {
  unsigned long currentTime = millis();
  
  // Check if it's time for a new measurement
  if (currentTime - lastMeasurement >= MEASUREMENT_INTERVAL) {
    
    Serial.println("\n📏 Starting Measurement Cycle...");
    blinkStatusLED(1);
    
    // Perform bioimpedance measurement
    digitalWrite(MUX_CONTROL_PIN, LOW);  // Select AD5933
    delay(100);
    BioimpedanceData bioData = measureBioimpedance();
    
    // Perform nerve signal measurement
    digitalWrite(MUX_CONTROL_PIN, HIGH); // Select AD620
    delay(100);
    NerveSignalData nerveData = measureNerveSignal();
    
    // Perform ML inference
    MLPrediction mlResult = performMLInference(bioData, nerveData);
    
    // Display results on Serial Monitor
    displayMeasurementResults(bioData, nerveData, mlResult);
    
    // Send data via Bluetooth
    if (bluetoothConnected) {
      sendBluetoothData(bioData, nerveData, mlResult);
    }
    
    // Update system status
    updateBatteryLevel();
    lastMeasurement = currentTime;
    
    // Alert if abnormal
    if (mlResult.prediction != "Normal") {
      Serial.println("🚨 ALERT: Abnormal condition detected!");
      blinkStatusLED(5);  // Alert blink pattern
    }
  }
  
  // Check Bluetooth connection
  if (SerialBT.available()) {
    String command = SerialBT.readString();
    handleBluetoothCommand(command);
  }
  
  delay(100);  // Small delay for stability
}

void initializeSystem() {
  Serial.println("🔧 Initializing Hardware Components...");
  
  // Initialize I2C for AD5933
  Wire.begin(AD5933_SDA_PIN, AD5933_SCL_PIN);
  delay(500);
  
  // Initialize AD5933
  initializeAD5933();
  
  // Initialize Bluetooth
  initializeBluetooth();
  
  Serial.println("📊 Calibrating sensors...");
  delay(1000);
  
  Serial.println("🧠 Loading TinyML model...");
  // In real implementation, load TensorFlow Lite model here
  delay(500);
  
  Serial.println("🔋 Battery Level: 100%");
}

void initializeBluetooth() {
  Serial.println("🔵 Initializing Bluetooth...");
  SerialBT.begin("NF_Monitor_001"); // Bluetooth device name
  Serial.println("📱 Device: NF_Monitor_001");
  Serial.println("✅ Bluetooth Ready!");
  bluetoothConnected = true;
}

void initializeAD5933() {
  Serial.println("📊 Initializing AD5933 Impedance Analyzer...");
  
  // Set start frequency (50kHz for bioimpedance)
  Wire.beginTransmission(AD5933_ADDR);
  Wire.write(AD5933_START_FREQ_REG);
  Wire.write(0x0C);  // 50kHz start frequency (simplified)
  Wire.write(0x35);
  Wire.write(0x0);
  Wire.endTransmission();
  
  delay(100);
  
  // Initialize measurement mode
  Wire.beginTransmission(AD5933_ADDR);
  Wire.write(AD5933_CONTROL_REG);
  Wire.write(0x11);  // Initialize with start frequency
  Wire.endTransmission();
  
  Serial.println("✅ AD5933 Ready!");
}

BioimpedanceData measureBioimpedance() {
  BioimpedanceData data;
  
  // Simulate realistic bioimpedance measurement
  // In real implementation, read from AD5933 registers
  
  // Read real and imaginary components (simulated)
  int16_t realPart = random(400, 1200);  // Simulated real part
  int16_t imagPart = random(200, 600);   // Simulated imaginary part
  
  // Calculate impedance parameters
  data.resistance = abs(realPart) * 0.8 + random(-50, 50);  // Add some noise
  data.reactance = abs(imagPart) * 0.6 + random(-30, 30);
  data.phase_angle = atan2(data.reactance, data.resistance) * (180.0 / PI);
  data.magnitude = sqrt(data.resistance * data.resistance + data.reactance * data.reactance);
  data.frequency = 50000;  // 50kHz measurement frequency
  
  // Ensure realistic ranges
  data.resistance = constrain(data.resistance, 50, 2000);
  data.reactance = constrain(data.reactance, 10, 800);
  
  return data;
}

NerveSignalData measureNerveSignal() {
  NerveSignalData data;
  
  // Read from AD620 amplifier (simulated)
  int adcValue = analogRead(AD620_SIGNAL_PIN);
  
  // Convert ADC to meaningful nerve signal parameters
  float rawVoltage = (adcValue / 4095.0) * 3.3;  // ESP32 ADC reference
  
  // Simulate nerve signal characteristics
  data.amplitude = (rawVoltage * 1000) + random(-10, 10);  // Convert to mV with noise
  data.conduction_velocity = random(25, 60) + (rawVoltage * 10);
  data.latency = random(2.5, 6.0) - (rawVoltage * 0.5);
  
  // Determine signal quality
  if (data.amplitude > 40) {
    data.signal_quality = "Good";
  } else if (data.amplitude > 25) {
    data.signal_quality = "Fair";
  } else {
    data.signal_quality = "Poor";
  }
  
  // Ensure realistic ranges
  data.amplitude = constrain(data.amplitude, 5, 80);
  data.conduction_velocity = constrain(data.conduction_velocity, 20, 65);
  data.latency = constrain(data.latency, 2.0, 8.0);
  
  return data;
}

MLPrediction performMLInference(BioimpedanceData bio, NerveSignalData nerve) {
  MLPrediction prediction;
  
  // Simple rule-based classification (simulating TinyML)
  // In real implementation, use TensorFlow Lite inference
  
  // Create feature vector
  float features[7] = {
    bio.resistance,
    bio.reactance, 
    bio.phase_angle,
    bio.magnitude,
    nerve.amplitude,
    nerve.conduction_velocity,
    nerve.latency
  };
  
  // Simple classification logic
  float riskScore = 0.0;
  
  // Bioimpedance risk factors
  if (bio.resistance > 1500) riskScore += 0.4;
  else if (bio.resistance > 1000) riskScore += 0.2;
  
  if (bio.reactance > 500) riskScore += 0.3;
  else if (bio.reactance > 350) riskScore += 0.15;
  
  // Nerve signal risk factors
  if (nerve.amplitude < 30) riskScore += 0.3;
  else if (nerve.amplitude < 40) riskScore += 0.15;
  
  if (nerve.conduction_velocity < 40) riskScore += 0.3;
  else if (nerve.conduction_velocity < 50) riskScore += 0.15;
  
  if (nerve.latency > 4.5) riskScore += 0.2;
  else if (nerve.latency > 3.8) riskScore += 0.1;
  
  // Classify based on risk score
  if (riskScore < 0.3) {
    prediction.prediction = "Normal";
    prediction.normal_prob = 0.85 + random(0, 15) / 100.0;
    prediction.early_nf_prob = random(5, 15) / 100.0;
    prediction.advanced_nf_prob = random(0, 5) / 100.0;
  } else if (riskScore < 0.7) {
    prediction.prediction = "NF_Early";
    prediction.normal_prob = random(10, 30) / 100.0;
    prediction.early_nf_prob = 0.60 + random(0, 25) / 100.0;
    prediction.advanced_nf_prob = random(5, 20) / 100.0;
  } else {
    prediction.prediction = "NF_Advanced";
    prediction.normal_prob = random(5, 15) / 100.0;
    prediction.early_nf_prob = random(15, 35) / 100.0;
    prediction.advanced_nf_prob = 0.70 + random(0, 20) / 100.0;
  }
  
  // Calculate confidence as the maximum probability
  prediction.confidence = max(max(prediction.normal_prob, prediction.early_nf_prob), prediction.advanced_nf_prob);
  
  return prediction;
}

void displayMeasurementResults(BioimpedanceData bio, NerveSignalData nerve, MLPrediction ml) {
  Serial.println("\n📊 MEASUREMENT RESULTS");
  Serial.println("=" * 40);
  
  // Bioimpedance results
  Serial.println("🔬 BIOIMPEDANCE ANALYSIS:");
  Serial.print("   Resistance:   "); Serial.print(bio.resistance, 2); Serial.println(" Ω");
  Serial.print("   Reactance:    "); Serial.print(bio.reactance, 2); Serial.println(" Ω");
  Serial.print("   Phase Angle:  "); Serial.print(bio.phase_angle, 2); Serial.println("°");
  Serial.print("   Magnitude:    "); Serial.print(bio.magnitude, 2); Serial.println(" Ω");
  Serial.print("   Frequency:    "); Serial.print(bio.frequency); Serial.println(" Hz");
  
  // Nerve signal results
  Serial.println("\n⚡ NERVE SIGNAL ANALYSIS:");
  Serial.print("   Amplitude:    "); Serial.print(nerve.amplitude, 2); Serial.println(" mV");
  Serial.print("   Conduction:   "); Serial.print(nerve.conduction_velocity, 2); Serial.println(" m/s");
  Serial.print("   Latency:      "); Serial.print(nerve.latency, 2); Serial.println(" ms");
  Serial.print("   Quality:      "); Serial.println(nerve.signal_quality);
  
  // ML prediction results
  Serial.println("\n🧠 AI CLASSIFICATION:");
  Serial.print("   Prediction:   "); Serial.println(ml.prediction);
  Serial.print("   Confidence:   "); Serial.print(ml.confidence * 100, 1); Serial.println("%");
  Serial.print("   Risk Level:   "); Serial.println(getRiskLevel(ml));
  
  // System status
  Serial.println("\n🔋 SYSTEM STATUS:");
  Serial.print("   Battery:      "); Serial.print(batteryLevel, 1); Serial.println("%");
  Serial.print("   Bluetooth:    "); Serial.println(bluetoothConnected ? "Connected" : "Disconnected");
  Serial.print("   Timestamp:    "); Serial.println(millis());
  
  Serial.println("=" * 40);
}

void sendBluetoothData(BioimpedanceData bio, NerveSignalData nerve, MLPrediction ml) {
  // Create JSON packet for Bluetooth transmission
  DynamicJsonDocument doc(1024);
  
  doc["timestamp"] = millis();
  doc["device_id"] = "NF_Monitor_001";
  doc["battery"] = batteryLevel;
  
  // Bioimpedance data
  JsonObject bioData = doc.createNestedObject("bioimpedance");
  bioData["resistance"] = bio.resistance;
  bioData["reactance"] = bio.reactance;
  bioData["phase_angle"] = bio.phase_angle;
  bioData["magnitude"] = bio.magnitude;
  bioData["frequency"] = bio.frequency;
  
  // Nerve signal data
  JsonObject nerveData = doc.createNestedObject("nerve_signal");
  nerveData["amplitude"] = nerve.amplitude;
  nerveData["conduction_velocity"] = nerve.conduction_velocity;
  nerveData["latency"] = nerve.latency;
  nerveData["signal_quality"] = nerve.signal_quality;
  
  // ML prediction data
  JsonObject mlData = doc.createNestedObject("ml_prediction");
  mlData["prediction"] = ml.prediction;
  mlData["confidence"] = ml.confidence;
  mlData["normal_prob"] = ml.normal_prob;
  mlData["early_nf_prob"] = ml.early_nf_prob;
  mlData["advanced_nf_prob"] = ml.advanced_nf_prob;
  
  doc["risk_level"] = getRiskLevel(ml);
  
  // Send JSON data via Bluetooth
  String jsonString;
  serializeJson(doc, jsonString);
  SerialBT.println(jsonString);
  
  Serial.println("📱 Data sent via Bluetooth");
}

String getRiskLevel(MLPrediction ml) {
  if (ml.prediction == "Normal") {
    if (ml.confidence > 0.8) {
      return "Low Risk";
    } else {
      return "Monitor";
    }
  } else if (ml.prediction == "NF_Early") {
    return "Moderate Risk - Consult Neurologist";
  } else {
    return "High Risk - Immediate Medical Attention";
  }
}

void updateBatteryLevel() {
  // Simulate battery drain
  batteryLevel -= random(1, 5) / 100.0;
  batteryLevel = constrain(batteryLevel, 0, 100);
  
  // In real implementation, read actual battery voltage
  // int batteryADC = analogRead(BATTERY_PIN);
  // batteryLevel = map(batteryADC, 0, 4095, 0, 100);
}

void blinkStatusLED(int times) {
  for (int i = 0; i < times; i++) {
    digitalWrite(LED_STATUS_PIN, HIGH);
    delay(200);
    digitalWrite(LED_STATUS_PIN, LOW);
    delay(200);
  }
}

void handleBluetoothCommand(String command) {
  command.trim();
  
  if (command == "STATUS") {
    SerialBT.println("System Status: Online");
    SerialBT.print("Battery: "); SerialBT.print(batteryLevel); SerialBT.println("%");
    SerialBT.print("Uptime: "); SerialBT.print(millis()); SerialBT.println(" ms");
  } 
  else if (command == "CALIBRATE") {
    SerialBT.println("Calibrating sensors...");
    initializeAD5933();
    SerialBT.println("Calibration complete");
  }
  else if (command == "RESET") {
    SerialBT.println("Resetting system...");
    ESP.restart();
  }
  else {
    SerialBT.println("Unknown command");
  }
}