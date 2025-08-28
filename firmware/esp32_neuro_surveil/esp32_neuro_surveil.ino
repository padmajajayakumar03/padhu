#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <math.h>

#define I2C_SDA 21
#define I2C_SCL 22
#define OLED_ADDR 0x3C
#define AD5933_ADDR 0x0D
#define OLED_W 128
#define OLED_H 64

Adafruit_SSD1306 display(OLED_W, OLED_H, &Wire, -1);

const int adcPin = 36; // ADC1_CH0

#define CTRL_REG_HIGH 0x80
#define CTRL_REG_LOW  0x81
#define START_FREQ    0x82
#define FREQ_INC      0x85
#define NUM_INCR      0x88
#define NUM_SETTLING  0x8A
#define STATUS_REG    0x8F
#define REAL_DATA     0x94
#define IMAG_DATA     0x96

#define CTRL_INIT_START_FREQ  0x10
#define CTRL_START_SWEEP      0x20
#define CTRL_REPEAT_FREQ      0x40
#define CTRL_STANDBY          0xB0
#define CTRL_POWER_DOWN       0xA0
#define CTRL_RANGE_1_GAIN_X1  0x01

const uint32_t mclkHz = 16000000UL;
const double   targetFreqHz = 30000.0;
double gainFactor = 1.0;
const double knownResOhm = 1000.0;

void write8(uint8_t reg, uint8_t val) {
  Wire.beginTransmission(AD5933_ADDR);
  Wire.write(reg);
  Wire.write(val);
  Wire.endTransmission();
}

void write16(uint8_t reg, uint16_t val) {
  Wire.beginTransmission(AD5933_ADDR);
  Wire.write(reg);
  Wire.write((val >> 8) & 0xFF);
  Wire.write(val & 0xFF);
  Wire.endTransmission();
}

void write24(uint8_t reg, uint32_t val24) {
  Wire.beginTransmission(AD5933_ADDR);
  Wire.write(reg);
  Wire.write((val24 >> 16) & 0xFF);
  Wire.write((val24 >> 8) & 0xFF);
  Wire.write(val24 & 0xFF);
  Wire.endTransmission();
}

uint8_t read8(uint8_t reg) {
  Wire.beginTransmission(AD5933_ADDR);
  Wire.write(reg);
  Wire.endTransmission(false);
  Wire.requestFrom(AD5933_ADDR, 1);
  return Wire.read();
}

void burstRead(uint8_t reg, uint8_t *buf, uint8_t n) {
  Wire.beginTransmission(AD5933_ADDR);
  Wire.write(reg);
  Wire.endTransmission(false);
  Wire.requestFrom(AD5933_ADDR, (int)n);
  for (uint8_t i=0;i<n;i++) buf[i]=Wire.read();
}

uint32_t freqToReg(double freqHz) {
  double f = (freqHz * (double)(1UL<<27)) / (double)mclkHz;
  if (f < 0) f = 0;
  if (f > 0xFFFFFF) f = 0xFFFFFF;
  return (uint32_t)f;
}

void ad5933Standby() {
  write8(CTRL_REG_HIGH, CTRL_STANDBY);
  write8(CTRL_REG_LOW, CTRL_RANGE_1_GAIN_X1);
}

void ad5933InitSingleTone(double freqHz) {
  ad5933Standby();
  delay(5);
  write24(START_FREQ, freqToReg(freqHz));
  write24(FREQ_INC, 0);
  write16(NUM_INCR, 0);
  write16(NUM_SETTLING, 10);
  write8(CTRL_REG_HIGH, CTRL_INIT_START_FREQ);
  write8(CTRL_REG_LOW, CTRL_RANGE_1_GAIN_X1);
  delay(2);
}

void ad5933StartMeasure() {
  write8(CTRL_REG_HIGH, CTRL_START_SWEEP);
  write8(CTRL_REG_LOW, CTRL_RANGE_1_GAIN_X1);
}

bool ad5933DataReady() {
  uint8_t s = read8(STATUS_REG);
  return (s & 0x02);
}

void ad5933ReadComplex(int16_t &re, int16_t &im) {
  uint8_t buf[4];
  burstRead(REAL_DATA, buf, 2);
  re = (int16_t)((buf[0] << 8) | buf[1]);
  burstRead(IMAG_DATA, buf, 2);
  im = (int16_t)((buf[0] << 8) | buf[1]);
}

double calibrateGainFactor(double knownRes) {
  ad5933InitSingleTone(targetFreqHz);
  ad5933StartMeasure();
  for (int i=0;i<200;i++) {
    if (ad5933DataReady()) break;
    delay(5);
  }
  int16_t re=0, im=0;
  ad5933ReadComplex(re, im);
  double mag = sqrt((double)re*re + (double)im*im);
  return knownRes * mag;
}

double readImpedanceOnce() {
  ad5933InitSingleTone(targetFreqHz);
  ad5933StartMeasure();
  for (int i=0;i<200;i++) {
    if (ad5933DataReady()) break;
    delay(5);
  }
  int16_t re=0, im=0;
  ad5933ReadComplex(re, im);
  double mag = sqrt((double)re*re + (double)im*im);
  if (mag <= 1e-9) return NAN;
  return gainFactor / mag;
}

double readAdcRms(size_t samples, double sampleRateHz) {
  uint64_t sumSq = 0;
  for (size_t i=0;i<samples;i++) {
    int raw = analogRead(adcPin);
    double v = (raw / 4095.0) * 3.3;
    double ac = v - 1.65;
    ac /= (10.0/(10.0+4.7));
    sumSq += (int32_t)((ac*1000.0)*(ac*1000.0));
    delayMicroseconds((int)(1e6 / sampleRateHz));
  }
  double meanSq_mV2 = (double)sumSq / (double)samples;
  double rms_mV = sqrt(meanSq_mV2);
  return rms_mV / 1000.0;
}

void setup() {
  analogReadResolution(12);
  Wire.begin(I2C_SDA, I2C_SCL);
  display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR);
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);

  display.setCursor(0,0);
  display.println("AD5933/AD620 Init");
  display.display();

  gainFactor = calibrateGainFactor(knownResOhm);

  display.setCursor(0,10);
  display.print("GF:");
  display.println(gainFactor, 2);
  display.display();
  delay(800);
}

void loop() {
  double z = readImpedanceOnce();
  double engRmsV = readAdcRms(1024, 4000.0);
  double engRms_uV = engRmsV * 1e6;

  display.clearDisplay();
  display.setCursor(0,0);
  display.println("Neurofibromatosis");
  display.setCursor(0,12);
  display.print("Z@30kHz: ");
  if (isnan(z)) display.print("---");
  else {
    if (z >= 1000.0) { display.print(z/1000.0, 3); display.print(" k"); }
    else display.print(z, 1);
    display.print("Ohm");
  }

  display.setCursor(0,24);
  display.print("ENG RMS: ");
  if (engRms_uV < 1000.0) { display.print(engRms_uV, 0); display.print(" uV"); }
  else { display.print(engRms_uV/1000.0, 2); display.print(" mV"); }

  int bar = (int)min(120.0, engRms_uV / 10.0);
  display.fillRect(0, 40, bar, 10, SSD1306_WHITE);

  display.display();
  delay(250);
}

