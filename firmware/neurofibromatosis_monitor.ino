/*
 * Neurofibromatosis Monitoring System
 * ESP32 Firmware with TinyML Integration
 * 
 * This system monitors bioimpedance and nerve signals to detect
 * potential neurofibromatosis using embedded AI inference.
 * 
 * Hardware:
 * - ESP32 DevKit
 * - AD5933 Impedance Analyzer
 * - AD620 Instrumentation Amplifier
 * - Surface Electrodes
 * - Analog Multiplexer (CD74HC4051)
 */

#include <WiFi.h>
#include <BluetoothSerial.h>
#include <Wire.h>
#include <ArduinoJson.h>
#include "TensorFlowLite_ESP32.h"
#include "tensorflow/lite/micro/all_ops_resolver.h"
#include "tensorflow/lite/micro/micro_error_reporter.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include "model.h" // TensorFlow Lite model

// Pin Definitions
#define AD5933_SDA_PIN 21
#define AD5933_SCL_PIN 22
#define AD620_OUTPUT_PIN 34
#define MUX_SELECT_A_PIN 25
#define MUX_SELECT_B_PIN 26
#define MUX_SELECT_C_PIN 27
#define LED_STATUS_PIN 2
#define BUZZER_PIN 4

// AD5933 Registers
#define AD5933_ADDR 0x0D
#define CONTROL_REG1 0x80
#define CONTROL_REG2 0x81
#define START_FREQ_REG 0x82
#define FREQ_INCREMENT_REG 0x85
#define NUM_INCREMENTS_REG 0x88
#define STATUS_REG 0x8F
#define REAL_DATA_REG 0x94
#define IMAG_DATA_REG 0x96

// System Configuration
#define SAMPLING_RATE 1000 // Hz
#define MEASUREMENT_INTERVAL 5000 // ms
#define CALIBRATION_POINTS 10
#define FEATURE_VECTOR_SIZE 8
#define ALERT_THRESHOLD 0.7

// Global Variables
BluetoothSerial SerialBT;
bool bluetoothConnected = false;
unsigned long lastMeasurement = 0;
float baselineImpedance = 0;
float baselineNerveSignal = 0;
bool systemCalibrated = false;

// TensorFlow Lite Variables
tflite::MicroErrorReporter micro_error_reporter;
tflite::AllOpsResolver resolver;
const tflite::Model* model = nullptr;
tflite::MicroInterpreter* interpreter = nullptr;
TfLiteTensor* input = nullptr;
TfLiteTensor* output = nullptr;

// Tensor arena for model execution
constexpr int kTensorArenaSize = 2000;
uint8_t tensor_arena[kTensorArenaSize];

// Data Structures
struct ImpedanceData {
  float resistance;
  float reactance;
  float magnitude;
  float phase;
  float frequency;
};

struct NerveSignalData {
  float amplitude;
  float conductionVelocity;
  float latency;
  float signalQuality;
};

struct FeatureVector {
  float resistance;
  float reactance;
  float phase;
  float nerveAmplitude;
  float conductionVelocity;
  float frequencyResponse;
  float signalNoiseRatio;
  float tissueCharacteristic;
};

// Function Prototypes
void setupTensorFlow();
void setupHardware();
void setupBluetooth();
void calibrateSystem();
ImpedanceData measureBioimpedance();
NerveSignalData measureNerveSignal();
FeatureVector extractFeatures(ImpedanceData imp, NerveSignalData nerve);
float runAIInference(FeatureVector features);
void sendBluetoothData(FeatureVector features, float prediction);
void handleAlert(float prediction);
void selectMuxChannel(int channel);
float readAD5933();
float readAD620();

void setup() {
  Serial.begin(115200);
  Serial.println("Neurofibromatosis Monitoring System Starting...");
  
  setupHardware();
  setupBluetooth();
  setupTensorFlow();
  
  delay(2000);
  calibrateSystem();
  
  Serial.println("System Ready - Starting Continuous Monitoring");
  digitalWrite(LED_STATUS_PIN, HIGH);
}

void loop() {
  if (millis() - lastMeasurement >= MEASUREMENT_INTERVAL) {
    // Measure bioimpedance
    selectMuxChannel(0); // Channel 0 for impedance
    delay(100);
    ImpedanceData impedanceData = measureBioimpedance();
    
    // Measure nerve signals
    selectMuxChannel(1); // Channel 1 for nerve signals
    delay(100);
    NerveSignalData nerveData = measureNerveSignal();
    
    // Extract features for AI model
    FeatureVector features = extractFeatures(impedanceData, nerveData);
    
    // Run AI inference
    float prediction = runAIInference(features);
    
    // Send data via Bluetooth
    sendBluetoothData(features, prediction);
    
    // Handle alerts if prediction indicates abnormality
    handleAlert(prediction);
    
    // Print to serial for debugging
    Serial.printf("R: %.2f Ω, X: %.2f Ω, Phase: %.2f°, Nerve: %.2f mV, AI: %.3f\n",
                  features.resistance, features.reactance, features.phase,
                  features.nerveAmplitude, prediction);
    
    lastMeasurement = millis();
  }
  
  delay(100); // Small delay to prevent overwhelming the system
}

void setupHardware() {
  // Initialize pins
  pinMode(LED_STATUS_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(MUX_SELECT_A_PIN, OUTPUT);
  pinMode(MUX_SELECT_B_PIN, OUTPUT);
  pinMode(MUX_SELECT_C_PIN, OUTPUT);
  pinMode(AD620_OUTPUT_PIN, INPUT);
  
  // Initialize I2C for AD5933
  Wire.begin(AD5933_SDA_PIN, AD5933_SCL_PIN);
  Wire.setClock(400000); // 400kHz I2C speed
  
  // Configure AD5933
  Wire.beginTransmission(AD5933_ADDR);
  Wire.write(CONTROL_REG1);
  Wire.write(0x10); // Initialize with internal clock
  Wire.endTransmission();
  
  Serial.println("Hardware initialized");
}

void setupBluetooth() {
  SerialBT.begin("NF_Monitor_Device");
  Serial.println("Bluetooth initialized - Device: NF_Monitor_Device");
  
  SerialBT.register_callback([](esp_spp_cb_event_t event, esp_spp_cb_param_t *param) {
    if (event == ESP_SPP_SRV_OPEN_EVT) {
      bluetoothConnected = true;
      Serial.println("Bluetooth client connected");
    } else if (event == ESP_SPP_CLOSE_EVT) {
      bluetoothConnected = false;
      Serial.println("Bluetooth client disconnected");
    }
  });
}

void setupTensorFlow() {
  // Load the TensorFlow Lite model
  model = tflite::GetModel(g_model);
  if (model->version() != TFLITE_SCHEMA_VERSION) {
    Serial.println("Model schema version mismatch!");
    return;
  }
  
  // Create interpreter
  static tflite::MicroInterpreter static_interpreter(
    model, resolver, tensor_arena, kTensorArenaSize, &micro_error_reporter);
  interpreter = &static_interpreter;
  
  // Allocate memory for model tensors
  TfLiteStatus allocate_status = interpreter->AllocateTensors();
  if (allocate_status != kTfLiteOk) {
    Serial.println("AllocateTensors() failed");
    return;
  }
  
  // Get pointers to input and output tensors
  input = interpreter->input(0);
  output = interpreter->output(0);
  
  Serial.println("TensorFlow Lite model loaded successfully");
}

void calibrateSystem() {
  Serial.println("Starting system calibration...");
  
  float impedanceSum = 0;
  float nerveSum = 0;
  
  for (int i = 0; i < CALIBRATION_POINTS; i++) {
    selectMuxChannel(0);
    delay(100);
    ImpedanceData imp = measureBioimpedance();
    impedanceSum += imp.magnitude;
    
    selectMuxChannel(1);
    delay(100);
    NerveSignalData nerve = measureNerveSignal();
    nerveSum += nerve.amplitude;
    
    Serial.printf("Calibration point %d/10\n", i + 1);
    delay(500);
  }
  
  baselineImpedance = impedanceSum / CALIBRATION_POINTS;
  baselineNerveSignal = nerveSum / CALIBRATION_POINTS;
  systemCalibrated = true;
  
  Serial.printf("Calibration complete - Baseline Impedance: %.2f Ω, Nerve: %.2f mV\n",
                baselineImpedance, baselineNerveSignal);
}

ImpedanceData measureBioimpedance() {
  ImpedanceData data;
  
  // Configure AD5933 for sweep
  Wire.beginTransmission(AD5933_ADDR);
  Wire.write(START_FREQ_REG);
  Wire.write(0x0E); Wire.write(0x30); Wire.write(0x00); // 50kHz start frequency
  Wire.endTransmission();
  
  // Start frequency sweep
  Wire.beginTransmission(AD5933_ADDR);
  Wire.write(CONTROL_REG1);
  Wire.write(0x11); // Start frequency sweep
  Wire.endTransmission();
  
  delay(10);
  
  // Read real and imaginary components
  Wire.beginTransmission(AD5933_ADDR);
  Wire.write(REAL_DATA_REG);
  Wire.endTransmission();
  Wire.requestFrom(AD5933_ADDR, 2);
  int16_t realPart = (Wire.read() << 8) | Wire.read();
  
  Wire.beginTransmission(AD5933_ADDR);
  Wire.write(IMAG_DATA_REG);
  Wire.endTransmission();
  Wire.requestFrom(AD5933_ADDR, 2);
  int16_t imagPart = (Wire.read() << 8) | Wire.read();
  
  // Calculate impedance parameters
  data.resistance = realPart * 0.1; // Scale factor
  data.reactance = imagPart * 0.1;
  data.magnitude = sqrt(data.resistance * data.resistance + data.reactance * data.reactance);
  data.phase = atan2(data.reactance, data.resistance) * 180.0 / PI;
  data.frequency = 50000; // 50kHz
  
  return data;
}

NerveSignalData measureNerveSignal() {
  NerveSignalData data;
  
  // Sample nerve signal from AD620 amplifier
  float samples[100];
  float maxValue = 0, minValue = 4095;
  
  for (int i = 0; i < 100; i++) {
    samples[i] = analogRead(AD620_OUTPUT_PIN);
    if (samples[i] > maxValue) maxValue = samples[i];
    if (samples[i] < minValue) minValue = samples[i];
    delayMicroseconds(1000); // 1kHz sampling
  }
  
  // Calculate nerve signal parameters
  data.amplitude = (maxValue - minValue) * 3.3 / 4095.0; // Convert to voltage
  data.conductionVelocity = 45.0 + random(-10, 10); // Simulated with variation
  data.latency = 2.5 + random(-5, 5) * 0.1; // Simulated latency in ms
  data.signalQuality = data.amplitude > 0.1 ? 0.8 : 0.3; // Simple quality metric
  
  return data;
}

FeatureVector extractFeatures(ImpedanceData imp, NerveSignalData nerve) {
  FeatureVector features;
  
  features.resistance = imp.resistance;
  features.reactance = imp.reactance;
  features.phase = imp.phase;
  features.nerveAmplitude = nerve.amplitude;
  features.conductionVelocity = nerve.conductionVelocity;
  features.frequencyResponse = imp.magnitude / baselineImpedance;
  features.signalNoiseRatio = nerve.signalQuality * 10;
  features.tissueCharacteristic = (imp.resistance / baselineImpedance) * 
                                  (nerve.amplitude / baselineNerveSignal);
  
  return features;
}

float runAIInference(FeatureVector features) {
  // Normalize features and copy to input tensor
  input->data.f[0] = features.resistance / 2000.0;
  input->data.f[1] = features.reactance / 1000.0;
  input->data.f[2] = features.phase / 90.0;
  input->data.f[3] = features.nerveAmplitude / 5.0;
  input->data.f[4] = features.conductionVelocity / 60.0;
  input->data.f[5] = features.frequencyResponse;
  input->data.f[6] = features.signalNoiseRatio / 10.0;
  input->data.f[7] = features.tissueCharacteristic;
  
  // Run inference
  TfLiteStatus invoke_status = interpreter->Invoke();
  if (invoke_status != kTfLiteOk) {
    Serial.println("Invoke failed!");
    return 0.0;
  }
  
  // Return prediction probability
  return output->data.f[0];
}

void sendBluetoothData(FeatureVector features, float prediction) {
  if (bluetoothConnected) {
    StaticJsonDocument<512> doc;
    
    doc["timestamp"] = millis();
    doc["resistance"] = features.resistance;
    doc["reactance"] = features.reactance;
    doc["phase"] = features.phase;
    doc["nerve_amplitude"] = features.nerveAmplitude;
    doc["conduction_velocity"] = features.conductionVelocity;
    doc["ai_prediction"] = prediction;
    doc["status"] = prediction > ALERT_THRESHOLD ? "ABNORMAL" : "NORMAL";
    
    String jsonString;
    serializeJson(doc, jsonString);
    SerialBT.println(jsonString);
  }
}

void handleAlert(float prediction) {
  if (prediction > ALERT_THRESHOLD) {
    // Visual alert
    for (int i = 0; i < 3; i++) {
      digitalWrite(LED_STATUS_PIN, HIGH);
      delay(200);
      digitalWrite(LED_STATUS_PIN, LOW);
      delay(200);
    }
    
    // Audio alert
    for (int i = 0; i < 2; i++) {
      digitalWrite(BUZZER_PIN, HIGH);
      delay(100);
      digitalWrite(BUZZER_PIN, LOW);
      delay(100);
    }
    
    Serial.println("ALERT: Possible neurofibromatosis detected!");
  } else {
    digitalWrite(LED_STATUS_PIN, HIGH);
  }
}

void selectMuxChannel(int channel) {
  digitalWrite(MUX_SELECT_A_PIN, channel & 0x01);
  digitalWrite(MUX_SELECT_B_PIN, (channel >> 1) & 0x01);
  digitalWrite(MUX_SELECT_C_PIN, (channel >> 2) & 0x01);
}