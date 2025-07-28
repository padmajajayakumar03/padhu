# Embedded AI System for Continuous Neurofibromatosis Surveillance

**"Embedded AI System for Continuous Neurofibromatosis Surveillance via Wearable Bioimpedance and Nerve Signal Sensors"**

## 📌 Project Overview

This project implements a **wearable biomedical device** that continuously monitors changes in nerve and skin tissue using **bioimpedance and nerve signal analysis** for **early detection and surveillance of neurofibromatosis (NF)**. The system uses **AI/ML models** to predict abnormalities and alerts patients or doctors through Bluetooth communication.

## 🔬 About Neurofibromatosis

Neurofibromatosis is a **genetic disorder** causing **tumors** to form on nerve tissues, affecting:
- **Nerves, skin, and bones**
- Three types: **NF1, NF2, and Schwannomatosis**
- Early symptoms: skin changes, lumps, pain, nerve dysfunction
- Requires regular monitoring to prevent complications

## 🧠 Biological Mechanism

- **Neurofibromas (tumors)** alter nerve and connective tissue structure
- Increases **fibrous tissue** leading to higher **electrical resistance**
- Affects **nerve signal conduction** (weaker/faulty transmission)
- Changes in **bioimpedance** can indicate tissue abnormalities

## ⚙️ System Architecture

```
[Surface Electrodes] 
       ↓ 
[AD5933 (Impedance)]   [AD620 (Nerve Amplifier)]
       ↓                        ↓
    [Multiplexer (MUX)] → [ESP32 Microcontroller]
                               ↓
         [TinyML Feature Extraction & Classification]
                               ↓
              [Bluetooth → Mobile App Alert]
```

## 🧪 Hardware Components

| Component | Purpose |
|-----------|---------|
| **Surface Electrodes** | Collect bioimpedance and nerve signals |
| **AD5933** | Measures complex impedance (R & X) |
| **AD620** | Amplifies small nerve signals (EMG/ENG) |
| **MUX** | Switches between impedance/nerve channels |
| **ESP32** | Main controller with Bluetooth + AI inference |
| **TinyML/TFLite** | On-device AI for NF detection |

## 🧠 AI Features

**Extracted Features:**
- Resistance (R) and Reactance (X)
- Phase angle (θ)
- Signal amplitude and conduction time
- Frequency response characteristics

**Model:** TensorFlow Lite classification (Normal/Abnormal)

## 📁 Project Structure

```
├── firmware/                 # ESP32 firmware code
├── ai_model/                # TensorFlow Lite model files
├── simulation/              # Proteus simulation files
├── mobile_app/              # Bluetooth receiver app
├── docs/                    # Documentation and images
└── test_data/               # Sample bioimpedance data
```

## 🚀 Quick Start

1. **Hardware Setup:** Connect AD5933, AD620, and electrodes to ESP32
2. **Flash Firmware:** Upload code to ESP32
3. **Install App:** Load Bluetooth receiver on mobile device
4. **Calibrate:** Run baseline measurements
5. **Monitor:** Place sensor and start real-time monitoring

## 📊 Expected Output

```
Resistance: 1250 Ohms
Reactance: 650 Ohms  
Nerve Conduction: Weak
AI Prediction: 0.92 (ABNORMAL)
Status: Possible NF - Alert Sent
```

## 🎯 Applications

- **Early NF screening** for high-risk individuals
- **Remote monitoring** for neurologists
- **Non-invasive** alternative to frequent biopsies
- **Home-based** continuous surveillance

## 🔧 Development Environment

- **Platform:** ESP32 Arduino IDE
- **AI Framework:** TensorFlow Lite for Microcontrollers
- **Simulation:** Proteus Design Suite
- **Communication:** Bluetooth Low Energy (BLE)

---

*This project demonstrates the integration of embedded AI, biomedical sensors, and wireless communication for innovative healthcare monitoring solutions.*