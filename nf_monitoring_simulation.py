#!/usr/bin/env python3
"""
Neurofibromatosis (NF) Monitoring System Simulation
Embedded AI System for Continuous Bioimpedance and Nerve Signal Analysis

Author: Padmaja
Project: Wearable Biomedical Device for NF Surveillance
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import random
from datetime import datetime, timedelta
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class AD5933Simulator:
    """Simulates AD5933 Impedance Analyzer"""
    
    def __init__(self):
        self.frequency_range = np.logspace(3, 5, 100)  # 1kHz to 100kHz
        self.calibrated = False
        
    def measure_impedance(self, tissue_type="normal"):
        """Simulate bioimpedance measurement"""
        if tissue_type == "normal":
            # Normal tissue impedance characteristics
            base_resistance = np.random.normal(800, 50)  # 800±50 Ohms
            base_reactance = np.random.normal(300, 30)   # 300±30 Ohms
        elif tissue_type == "nf_early":
            # Early NF - increased fibrous tissue
            base_resistance = np.random.normal(1200, 80)  # Increased resistance
            base_reactance = np.random.normal(450, 40)    # Increased reactance
        else:  # nf_advanced
            # Advanced NF - significant tissue changes
            base_resistance = np.random.normal(1800, 120)
            base_reactance = np.random.normal(650, 60)
            
        # Add some noise and drift
        noise_factor = np.random.normal(1, 0.02)
        resistance = max(50, base_resistance * noise_factor)
        reactance = max(10, base_reactance * noise_factor)
        
        # Calculate phase angle
        phase_angle = np.arctan(reactance / resistance) * (180 / np.pi)
        
        # Calculate magnitude
        magnitude = np.sqrt(resistance**2 + reactance**2)
        
        return {
            'resistance': round(resistance, 2),
            'reactance': round(reactance, 2),
            'phase_angle': round(phase_angle, 2),
            'magnitude': round(magnitude, 2),
            'frequency': 50000  # 50kHz measurement frequency
        }

class AD620Simulator:
    """Simulates AD620 Instrumentation Amplifier for Nerve Signals"""
    
    def __init__(self, gain=1000):
        self.gain = gain
        
    def amplify_nerve_signal(self, tissue_type="normal"):
        """Simulate nerve signal measurement (EMG/ENG)"""
        if tissue_type == "normal":
            # Normal nerve conduction
            amplitude = np.random.normal(50, 5)      # 50±5 µV
            conduction_velocity = np.random.normal(55, 3)  # 55±3 m/s
            latency = np.random.normal(3.2, 0.2)     # 3.2±0.2 ms
        elif tissue_type == "nf_early":
            # Early NF - mild nerve compression
            amplitude = np.random.normal(35, 5)      # Reduced amplitude
            conduction_velocity = np.random.normal(45, 4)  # Slower conduction
            latency = np.random.normal(4.1, 0.3)     # Increased latency
        else:  # nf_advanced
            # Advanced NF - significant nerve dysfunction
            amplitude = np.random.normal(20, 8)      # Significantly reduced
            conduction_velocity = np.random.normal(30, 6)  # Much slower
            latency = np.random.normal(5.5, 0.5)     # Much higher latency
            
        # Apply amplification
        amplified_signal = max(0.1, amplitude * self.gain / 1000000)  # Convert to mV
        
        return {
            'raw_amplitude': round(amplitude, 2),
            'amplified_signal': round(amplified_signal, 2),
            'conduction_velocity': round(conduction_velocity, 2),
            'latency': round(latency, 2),
            'signal_quality': 'Good' if amplitude > 30 else 'Poor'
        }

class TinyMLClassifier:
    """Simulates TensorFlow Lite model for NF detection"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def train_model(self, training_data):
        """Train the ML model with synthetic data"""
        print("🧠 Training TinyML Model...")
        
        # Create synthetic training data
        X = np.array(training_data['features'])
        y = np.array(training_data['labels'])
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train Random Forest (simulating TensorFlow Lite)
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.model.fit(X_scaled, y)
        
        self.is_trained = True
        print("✅ Model training completed!")
        
        # Calculate accuracy on training data
        accuracy = self.model.score(X_scaled, y)
        print(f"📊 Training Accuracy: {accuracy:.2%}")
        
    def predict(self, features):
        """Make prediction on new data"""
        if not self.is_trained:
            return {'prediction': 'unknown', 'confidence': 0.0}
            
        # Scale features
        features_scaled = self.scaler.transform([features])
        
        # Get prediction and probability
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        # Convert to meaningful labels
        labels = ['Normal', 'NF_Early', 'NF_Advanced']
        predicted_label = labels[prediction]
        confidence = max(probabilities)
        
        return {
            'prediction': predicted_label,
            'confidence': round(confidence, 3),
            'probabilities': {
                'Normal': round(probabilities[0], 3),
                'NF_Early': round(probabilities[1], 3),
                'NF_Advanced': round(probabilities[2], 3)
            }
        }

class ESP32Controller:
    """Simulates ESP32 microcontroller with Bluetooth communication"""
    
    def __init__(self):
        self.bluetooth_connected = False
        self.device_id = "NF_Monitor_001"
        self.battery_level = 100
        
    def initialize(self):
        """Initialize ESP32 system"""
        print("🔌 Initializing ESP32 Controller...")
        print(f"📱 Device ID: {self.device_id}")
        print("🔵 Bluetooth: Initializing...")
        time.sleep(1)
        self.bluetooth_connected = True
        print("✅ ESP32 Ready!")
        
    def send_bluetooth_data(self, data):
        """Simulate Bluetooth data transmission"""
        if not self.bluetooth_connected:
            return {"status": "error", "message": "Bluetooth not connected"}
            
        # Simulate data packet
        packet = {
            "timestamp": datetime.now().isoformat(),
            "device_id": self.device_id,
            "battery": self.battery_level,
            "data": data
        }
        
        # Simulate transmission delay
        time.sleep(0.1)
        return {"status": "success", "packet": packet}
    
    def update_battery(self):
        """Simulate battery drain"""
        self.battery_level = max(0, self.battery_level - random.uniform(0.1, 0.3))

class NFMonitoringSystem:
    """Main Neurofibromatosis Monitoring System"""
    
    def __init__(self):
        self.ad5933 = AD5933Simulator()
        self.ad620 = AD620Simulator()
        self.ml_model = TinyMLClassifier()
        self.esp32 = ESP32Controller()
        self.monitoring_active = False
        self.data_log = []
        
    def initialize_system(self):
        """Initialize all components"""
        print("🏥 NEUROFIBROMATOSIS MONITORING SYSTEM")
        print("=" * 50)
        print("🔧 Initializing Hardware Components...")
        
        # Initialize ESP32
        self.esp32.initialize()
        
        print("📊 Calibrating AD5933 Impedance Analyzer...")
        time.sleep(1)
        print("🔬 Setting up AD620 Amplifier (Gain: 1000x)...")
        time.sleep(1)
        
        # Train ML model
        self._generate_training_data()
        
        print("✅ System Ready for Monitoring!")
        print("=" * 50)
        
    def _generate_training_data(self):
        """Generate synthetic training data for ML model"""
        print("📚 Generating training dataset...")
        
        features = []
        labels = []
        
        # Generate data for each class
        for class_idx, tissue_type in enumerate(['normal', 'nf_early', 'nf_advanced']):
            for _ in range(100):  # 100 samples per class
                # Get impedance data
                impedance = self.ad5933.measure_impedance(tissue_type)
                # Get nerve signal data
                nerve = self.ad620.amplify_nerve_signal(tissue_type)
                
                # Create feature vector
                feature_vector = [
                    impedance['resistance'],
                    impedance['reactance'],
                    impedance['phase_angle'],
                    impedance['magnitude'],
                    nerve['amplified_signal'],
                    nerve['conduction_velocity'],
                    nerve['latency']
                ]
                
                features.append(feature_vector)
                labels.append(class_idx)
        
        training_data = {
            'features': features,
            'labels': labels
        }
        
        self.ml_model.train_model(training_data)
        
    def perform_measurement(self, patient_condition="normal"):
        """Perform a complete measurement cycle"""
        # Get impedance measurement
        impedance_data = self.ad5933.measure_impedance(patient_condition)
        
        # Get nerve signal measurement
        nerve_data = self.ad620.amplify_nerve_signal(patient_condition)
        
        # Create feature vector for ML prediction
        features = [
            impedance_data['resistance'],
            impedance_data['reactance'],
            impedance_data['phase_angle'],
            impedance_data['magnitude'],
            nerve_data['amplified_signal'],
            nerve_data['conduction_velocity'],
            nerve_data['latency']
        ]
        
        # Get ML prediction
        ml_result = self.ml_model.predict(features)
        
        # Combine all data
        measurement = {
            'timestamp': datetime.now().isoformat(),
            'impedance': impedance_data,
            'nerve_signal': nerve_data,
            'ml_prediction': ml_result,
            'risk_level': self._calculate_risk_level(ml_result)
        }
        
        # Send via Bluetooth
        bluetooth_result = self.esp32.send_bluetooth_data(measurement)
        
        # Update battery
        self.esp32.update_battery()
        
        # Log data
        self.data_log.append(measurement)
        
        return measurement, bluetooth_result
    
    def _calculate_risk_level(self, ml_result):
        """Calculate risk level based on ML prediction"""
        if ml_result['prediction'] == 'Normal':
            if ml_result['confidence'] > 0.8:
                return "Low Risk"
            else:
                return "Monitor"
        elif ml_result['prediction'] == 'NF_Early':
            return "Moderate Risk - Consult Neurologist"
        else:  # NF_Advanced
            return "High Risk - Immediate Medical Attention"
    
    def continuous_monitoring(self, duration_minutes=5, patient_scenarios=None):
        """Simulate continuous monitoring"""
        print(f"\n🔄 Starting Continuous Monitoring ({duration_minutes} minutes)")
        print("-" * 60)
        
        if patient_scenarios is None:
            # Default scenarios for demonstration
            patient_scenarios = [
                ("normal", 0.7),      # 70% normal readings
                ("nf_early", 0.2),    # 20% early NF
                ("nf_advanced", 0.1)  # 10% advanced NF
            ]
        
        measurements_count = 0
        start_time = time.time()
        
        try:
            while time.time() - start_time < duration_minutes * 60:
                # Select patient condition based on probabilities
                rand = random.random()
                cumulative = 0
                selected_condition = "normal"
                
                for condition, prob in patient_scenarios:
                    cumulative += prob
                    if rand <= cumulative:
                        selected_condition = condition
                        break
                
                # Perform measurement
                measurement, bluetooth = self.perform_measurement(selected_condition)
                measurements_count += 1
                
                # Display results
                self._display_measurement_results(measurement, measurements_count)
                
                # Wait for next measurement (simulate real-time sampling)
                time.sleep(2)  # 2 seconds between measurements
                
        except KeyboardInterrupt:
            print("\n⏹️  Monitoring stopped by user")
        
        print(f"\n📊 Monitoring completed. Total measurements: {measurements_count}")
        return self.data_log
    
    def _display_measurement_results(self, measurement, count):
        """Display measurement results in real-time format"""
        timestamp = datetime.fromisoformat(measurement['timestamp']).strftime("%H:%M:%S")
        
        print(f"\n📏 Measurement #{count} - {timestamp}")
        print("=" * 40)
        
        # Impedance data
        imp = measurement['impedance']
        print(f"🔬 BIOIMPEDANCE ANALYSIS:")
        print(f"   Resistance:   {imp['resistance']:>8.2f} Ω")
        print(f"   Reactance:    {imp['reactance']:>8.2f} Ω")
        print(f"   Phase Angle:  {imp['phase_angle']:>8.2f}°")
        print(f"   Magnitude:    {imp['magnitude']:>8.2f} Ω")
        
        # Nerve signal data
        nerve = measurement['nerve_signal']
        print(f"\n⚡ NERVE SIGNAL ANALYSIS:")
        print(f"   Amplitude:    {nerve['amplified_signal']:>8.2f} mV")
        print(f"   Conduction:   {nerve['conduction_velocity']:>8.2f} m/s")
        print(f"   Latency:      {nerve['latency']:>8.2f} ms")
        print(f"   Quality:      {nerve['signal_quality']:>8}")
        
        # ML prediction
        ml = measurement['ml_prediction']
        print(f"\n🧠 AI CLASSIFICATION:")
        print(f"   Prediction:   {ml['prediction']:>12}")
        print(f"   Confidence:   {ml['confidence']:>8.1%}")
        print(f"   Risk Level:   {measurement['risk_level']}")
        
        # Battery status
        battery = self.esp32.battery_level
        print(f"\n🔋 System Status:")
        print(f"   Battery:      {battery:>8.1f}%")
        print(f"   Bluetooth:    {'Connected' if self.esp32.bluetooth_connected else 'Disconnected'}")
        
        # Alert if abnormal
        if ml['prediction'] != 'Normal':
            print(f"\n🚨 ALERT: {measurement['risk_level']}")
            print("   📱 Notification sent via Bluetooth")
        
        print("-" * 40)
    
    def generate_report(self):
        """Generate comprehensive monitoring report"""
        if not self.data_log:
            print("No data available for report generation.")
            return None
        
        print("\n📋 NEUROFIBROMATOSIS MONITORING REPORT")
        print("=" * 60)
        
        # Summary statistics
        total_measurements = len(self.data_log)
        normal_count = sum(1 for d in self.data_log if d['ml_prediction']['prediction'] == 'Normal')
        early_nf_count = sum(1 for d in self.data_log if d['ml_prediction']['prediction'] == 'NF_Early')
        advanced_nf_count = sum(1 for d in self.data_log if d['ml_prediction']['prediction'] == 'NF_Advanced')
        
        print(f"📊 SUMMARY:")
        print(f"   Total Measurements:     {total_measurements}")
        print(f"   Normal Readings:        {normal_count:>3} ({normal_count/total_measurements:.1%})")
        print(f"   Early NF Detected:      {early_nf_count:>3} ({early_nf_count/total_measurements:.1%})")
        print(f"   Advanced NF Detected:   {advanced_nf_count:>3} ({advanced_nf_count/total_measurements:.1%})")
        
        # Average values
        resistances = [d['impedance']['resistance'] for d in self.data_log]
        reactances = [d['impedance']['reactance'] for d in self.data_log]
        nerve_amplitudes = [d['nerve_signal']['amplified_signal'] for d in self.data_log]
        
        print(f"\n📈 AVERAGE VALUES:")
        print(f"   Resistance:             {np.mean(resistances):>8.2f} ± {np.std(resistances):.2f} Ω")
        print(f"   Reactance:              {np.mean(reactances):>8.2f} ± {np.std(reactances):.2f} Ω")
        print(f"   Nerve Signal:           {np.mean(nerve_amplitudes):>8.2f} ± {np.std(nerve_amplitudes):.2f} mV")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if advanced_nf_count > 0:
            print("   🔴 URGENT: Advanced NF signs detected - Immediate medical consultation required")
        elif early_nf_count > 0:
            print("   🟡 CAUTION: Early NF signs detected - Schedule neurologist appointment")
        else:
            print("   🟢 NORMAL: Continue regular monitoring")
        
        print("=" * 60)
        
        return {
            'total_measurements': total_measurements,
            'normal_percentage': normal_count/total_measurements * 100,
            'early_nf_percentage': early_nf_count/total_measurements * 100,
            'advanced_nf_percentage': advanced_nf_count/total_measurements * 100,
            'avg_resistance': np.mean(resistances),
            'avg_reactance': np.mean(reactances),
            'avg_nerve_signal': np.mean(nerve_amplitudes)
        }
    
    def save_data_to_file(self, filename="nf_monitoring_data.json"):
        """Save monitoring data to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.data_log, f, indent=2)
        print(f"💾 Data saved to {filename}")

def main():
    """Main simulation function"""
    print("🏥 NEUROFIBROMATOSIS MONITORING SYSTEM SIMULATION")
    print("🔬 Embedded AI for Bioimpedance & Nerve Signal Analysis")
    print("👨‍⚕️ By: Padmaja")
    print("=" * 70)
    
    # Initialize monitoring system
    nf_system = NFMonitoringSystem()
    nf_system.initialize_system()
    
    # Demonstrate single measurements
    print("\n🧪 DEMONSTRATION: Single Measurements")
    print("-" * 50)
    
    conditions = [
        ("Normal Patient", "normal"),
        ("Early NF Patient", "nf_early"),
        ("Advanced NF Patient", "nf_advanced")
    ]
    
    for condition_name, condition_type in conditions:
        print(f"\n👤 Testing: {condition_name}")
        measurement, bluetooth = nf_system.perform_measurement(condition_type)
        nf_system._display_measurement_results(measurement, 1)
        time.sleep(1)
    
    # Start continuous monitoring
    print("\n" + "="*70)
    input("Press Enter to start continuous monitoring simulation...")
    
    # Run continuous monitoring for 2 minutes (for demo purposes)
    monitoring_data = nf_system.continuous_monitoring(duration_minutes=2)
    
    # Generate final report
    nf_system.generate_report()
    
    # Save data
    nf_system.save_data_to_file()
    
    print("\n🎉 Simulation completed successfully!")
    print("📱 In real implementation, this data would be sent to mobile app via Bluetooth")
    print("🔬 Project ready for demonstration to faculty!")

if __name__ == "__main__":
    main()