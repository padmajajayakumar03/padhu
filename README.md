## ESP32 + AD5933 + AD620 Neurofibromatosis Surveillance (Bioimpedance + Nerve ENG)

### Hardware Summary
- ESP32 DevKit (3.3 V logic)
- AD5933 bioimpedance analyzer (I2C @ 0x0D)
- AD620 instrumentation amplifier for ENG
- SSD1306 OLED 128x64 (I2C @ 0x3C)

### Wiring (quick map)
- Power: ESP32 3.3 V → AD5933 VCC, OLED VCC; 5 V → AD620 +Vs; Common GND
- I2C: ESP32 SDA=GPIO21 → AD5933 SDA, OLED SDA; SCL=GPIO22 → AD5933 SCL, OLED SCL
- Pull-ups: 4.7 kΩ to 3.3 V on SDA/SCL unless your boards have them
- AD5933 Z+/Z−: to tissue phantom through 1 kΩ series resistors (each lead)
- AD620 inputs: electrodes → 100 kΩ series → IN+, IN−; REF pin to 1.65 V
- AD620 OUT → 4.7 kΩ → ESP32 ADC GPIO36; 100 nF from ADC pin to GND
- 1.65 V reference: 10 kΩ/10 kΩ divider from 3.3 V; decouple with 10 µF || 100 nF
- AD620 gain: RG=499 Ω → G≈100

### Firmware
- Location: `firmware/esp32_neuro_surveil/esp32_neuro_surveil.ino`
- Arduino IDE: select ESP32 Dev Module, set Upload Speed/Baud as usual
- Install libs: Adafruit GFX, Adafruit SSD1306
- Flash, then connect a known 1.00 kΩ across AD5933 Z+/Z− for calibration

### Simulation
- LTspice netlist: `sim/ltspice/ad620_frontend.cir`
- Simulates the AD620 frontend with ENG input source and RC filters
- Run `.tran` to see OUT and ADC waveforms; adjust source amplitude and RG as needed

### Expected On-Device Display
- Title: `Neurofibromatosis`
- `Z@30kHz: ~1.00 kOhm` (with 1 kΩ calibrator)
- `ENG RMS: 10–100 uV` depending on your input source
- A horizontal bar grows with ENG amplitude

### Safety
- Do not connect to humans. Use phantoms and isolated sources. Clinical use requires medical-grade design and regulatory approval.