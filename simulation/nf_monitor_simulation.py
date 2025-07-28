#!/usr/bin/env python3
"""
Neurofibromatosis Monitoring System Simulation
==============================================

This script simulates the embedded AI system for continuous neurofibromatosis 
surveillance via bioimpedance and nerve signal monitoring.

Features:
- Synthetic bioimpedance data generation
- Nerve signal simulation
- AI model inference simulation
- Real-time monitoring visualization
- Bluetooth communication simulation

Author: Padmaja
Date: 2024
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import time
import random
from datetime import datetime
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class NeurofibromatosisMonitor:
    """
    Simulates the ESP32-based neurofibromatosis monitoring system
    """
    
    def __init__(self):
        self.setup_system()
        self.setup_ai_model()
        self.baseline_calibrated = False
        self.baseline_impedance = 0
        self.baseline_nerve_signal = 0
        self.measurement_data = []
        
    def setup_system(self):
        """Initialize system parameters"""
        print("🔧 Initializing Neurofibromatosis Monitoring System...")
        print("📡 ESP32 DevKit Ready")
        print("⚡ AD5933 Impedance Analyzer Connected")
        print("🧠 AD620 Nerve Amplifier Ready")
        print("📳 Bluetooth Module Active")
        print("🤖 TensorFlow Lite Model Loading...")
        
        # System configuration
        self.config = {
            'sampling_rate': 1000,  # Hz
            'measurement_interval': 5,  # seconds
            'alert_threshold': 0.7,
            'calibration_points': 10,
            'normal_resistance_range': (800, 1200),  # Ohms
            'normal_reactance_range': (400, 800),    # Ohms
            'normal_nerve_amplitude_range': (0.5, 2.0),  # mV
            'nf_resistance_increase': 1.5,  # Multiplier for NF tissue
            'nf_nerve_amplitude_decrease': 0.6  # Multiplier for NF nerve signals
        }
        
    def setup_ai_model(self):
        """Initialize AI model for NF detection"""
        print("🧠 Training AI Model for Neurofibromatosis Detection...")
        
        # Generate training data
        n_samples = 1000
        X_train, y_train = self.generate_training_data(n_samples)
        
        # Train Random Forest model (simulating TensorFlow Lite)
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X_train)
        
        self.ai_model = RandomForestClassifier(
            n_estimators=50, 
            max_depth=10, 
            random_state=42
        )
        self.ai_model.fit(X_scaled, y_train)
        
        print("✅ AI Model Trained Successfully")
        print(f"📊 Model Accuracy: {self.ai_model.score(X_scaled, y_train):.3f}")
        
    def generate_training_data(self, n_samples):
        """Generate synthetic training data for AI model"""
        X = []
        y = []
        
        for i in range(n_samples):
            if random.random() < 0.7:  # 70% normal cases
                # Normal tissue parameters
                resistance = random.uniform(800, 1200)
                reactance = random.uniform(400, 800)
                phase = np.arctan2(reactance, resistance) * 180 / np.pi
                nerve_amplitude = random.uniform(1.0, 2.5)
                conduction_velocity = random.uniform(40, 55)
                freq_response = random.uniform(0.8, 1.2)
                snr = random.uniform(8, 12)
                tissue_char = random.uniform(0.8, 1.2)
                label = 0  # Normal
            else:  # 30% NF cases
                # NF tissue parameters (higher resistance, lower nerve signals)
                resistance = random.uniform(1200, 2000)
                reactance = random.uniform(600, 1200)
                phase = np.arctan2(reactance, resistance) * 180 / np.pi
                nerve_amplitude = random.uniform(0.2, 1.0)
                conduction_velocity = random.uniform(25, 40)
                freq_response = random.uniform(1.2, 2.0)
                snr = random.uniform(4, 8)
                tissue_char = random.uniform(1.5, 3.0)
                label = 1  # NF
                
            features = [resistance, reactance, phase, nerve_amplitude,
                       conduction_velocity, freq_response, snr, tissue_char]
            X.append(features)
            y.append(label)
            
        return np.array(X), np.array(y)
        
    def calibrate_system(self):
        """Perform system calibration"""
        print("\n🔧 Starting System Calibration...")
        
        impedance_readings = []
        nerve_readings = []
        
        for i in range(self.config['calibration_points']):
            print(f"📊 Calibration Point {i+1}/{self.config['calibration_points']}")
            
            # Simulate baseline readings
            imp_data = self.measure_bioimpedance(baseline=True)
            nerve_data = self.measure_nerve_signal(baseline=True)
            
            impedance_readings.append(imp_data['magnitude'])
            nerve_readings.append(nerve_data['amplitude'])
            
            time.sleep(0.5)
            
        self.baseline_impedance = np.mean(impedance_readings)
        self.baseline_nerve_signal = np.mean(nerve_readings)
        self.baseline_calibrated = True
        
        print(f"✅ Calibration Complete!")
        print(f"📏 Baseline Impedance: {self.baseline_impedance:.2f} Ω")
        print(f"🧠 Baseline Nerve Signal: {self.baseline_nerve_signal:.2f} mV")
        
    def measure_bioimpedance(self, baseline=False, nf_simulation=False):
        """Simulate AD5933 bioimpedance measurement"""
        if baseline:
            resistance = random.uniform(*self.config['normal_resistance_range'])
            reactance = random.uniform(*self.config['normal_reactance_range'])
        elif nf_simulation:
            # Simulate NF tissue (higher impedance)
            resistance = random.uniform(1200, 2000)
            reactance = random.uniform(600, 1200)
        else:
            # Normal variation
            resistance = random.uniform(800, 1400)
            reactance = random.uniform(400, 900)
            
        # Add measurement noise
        resistance += random.gauss(0, 20)
        reactance += random.gauss(0, 15)
        
        magnitude = np.sqrt(resistance**2 + reactance**2)
        phase = np.arctan2(reactance, resistance) * 180 / np.pi
        frequency = 50000  # 50kHz
        
        return {
            'resistance': resistance,
            'reactance': reactance,
            'magnitude': magnitude,
            'phase': phase,
            'frequency': frequency
        }
        
    def measure_nerve_signal(self, baseline=False, nf_simulation=False):
        """Simulate AD620 nerve signal measurement"""
        if baseline:
            amplitude = random.uniform(*self.config['normal_nerve_amplitude_range'])
            conduction_velocity = random.uniform(45, 55)
        elif nf_simulation:
            # Simulate NF nerve dysfunction (lower amplitude, slower conduction)
            amplitude = random.uniform(0.2, 1.0)
            conduction_velocity = random.uniform(25, 40)
        else:
            # Normal variation
            amplitude = random.uniform(0.8, 2.2)
            conduction_velocity = random.uniform(40, 55)
            
        # Add measurement noise
        amplitude += random.gauss(0, 0.1)
        conduction_velocity += random.gauss(0, 2)
        
        latency = 2.5 + random.uniform(-0.5, 0.5)
        signal_quality = min(1.0, amplitude / 0.5)
        
        return {
            'amplitude': max(0, amplitude),
            'conduction_velocity': max(0, conduction_velocity),
            'latency': latency,
            'signal_quality': signal_quality
        }
        
    def extract_features(self, imp_data, nerve_data):
        """Extract features for AI model"""
        if not self.baseline_calibrated:
            freq_response = 1.0
            tissue_characteristic = 1.0
        else:
            freq_response = imp_data['magnitude'] / self.baseline_impedance
            tissue_characteristic = (imp_data['resistance'] / self.baseline_impedance) * \
                                  (nerve_data['amplitude'] / self.baseline_nerve_signal)
        
        features = {
            'resistance': imp_data['resistance'],
            'reactance': imp_data['reactance'],
            'phase': imp_data['phase'],
            'nerve_amplitude': nerve_data['amplitude'],
            'conduction_velocity': nerve_data['conduction_velocity'],
            'frequency_response': freq_response,
            'signal_noise_ratio': nerve_data['signal_quality'] * 10,
            'tissue_characteristic': tissue_characteristic
        }
        
        return features
        
    def run_ai_inference(self, features):
        """Run AI inference for NF detection"""
        feature_vector = [
            features['resistance'],
            features['reactance'],
            features['phase'],
            features['nerve_amplitude'],
            features['conduction_velocity'],
            features['frequency_response'],
            features['signal_noise_ratio'],
            features['tissue_characteristic']
        ]
        
        # Normalize features
        feature_array = np.array(feature_vector).reshape(1, -1)
        feature_scaled = self.scaler.transform(feature_array)
        
        # Get prediction probability
        prediction_proba = self.ai_model.predict_proba(feature_scaled)[0]
        nf_probability = prediction_proba[1]  # Probability of NF
        
        return nf_probability
        
    def send_bluetooth_data(self, features, prediction):
        """Simulate Bluetooth data transmission"""
        data = {
            'timestamp': datetime.now().isoformat(),
            'resistance': round(features['resistance'], 2),
            'reactance': round(features['reactance'], 2),
            'phase': round(features['phase'], 2),
            'nerve_amplitude': round(features['nerve_amplitude'], 3),
            'conduction_velocity': round(features['conduction_velocity'], 1),
            'ai_prediction': round(prediction, 3),
            'status': 'ABNORMAL' if prediction > self.config['alert_threshold'] else 'NORMAL'
        }
        
        # Store measurement data
        self.measurement_data.append(data)
        
        return json.dumps(data, indent=2)
        
    def handle_alert(self, prediction, features):
        """Handle alert system"""
        if prediction > self.config['alert_threshold']:
            print("🚨 ALERT: Possible Neurofibromatosis Detected!")
            print("💡 LED: Blinking")
            print("🔊 Buzzer: Activated")
            print(f"📊 AI Confidence: {prediction:.3f}")
            return True
        return False
        
    def run_monitoring_cycle(self, duration_minutes=5, nf_simulation_start=None):
        """Run continuous monitoring simulation"""
        print(f"\n🔄 Starting Continuous Monitoring for {duration_minutes} minutes...")
        print("📱 Bluetooth Ready for Mobile App Connection")
        
        start_time = time.time()
        cycle_count = 0
        alert_count = 0
        
        while (time.time() - start_time) < (duration_minutes * 60):
            cycle_count += 1
            
            # Simulate NF condition after specified time
            nf_simulation = False
            if nf_simulation_start and cycle_count > nf_simulation_start:
                nf_simulation = True
                
            # Measure bioimpedance and nerve signals
            imp_data = self.measure_bioimpedance(nf_simulation=nf_simulation)
            nerve_data = self.measure_nerve_signal(nf_simulation=nf_simulation)
            
            # Extract features
            features = self.extract_features(imp_data, nerve_data)
            
            # Run AI inference
            prediction = self.run_ai_inference(features)
            
            # Send Bluetooth data
            bluetooth_json = self.send_bluetooth_data(features, prediction)
            
            # Handle alerts
            alert_triggered = self.handle_alert(prediction, features)
            if alert_triggered:
                alert_count += 1
                
            # Print monitoring output
            status = "🔴 ABNORMAL" if prediction > self.config['alert_threshold'] else "🟢 NORMAL"
            print(f"📊 Cycle {cycle_count}: R={features['resistance']:.0f}Ω, "
                  f"X={features['reactance']:.0f}Ω, "
                  f"Nerve={features['nerve_amplitude']:.2f}mV, "
                  f"AI={prediction:.3f} {status}")
            
            # Wait for next measurement interval
            time.sleep(self.config['measurement_interval'])
            
        print(f"\n✅ Monitoring Complete!")
        print(f"📈 Total Cycles: {cycle_count}")
        print(f"🚨 Alerts Triggered: {alert_count}")
        return self.measurement_data
        
    def generate_report(self):
        """Generate monitoring report with visualizations"""
        if not self.measurement_data:
            print("❌ No measurement data available for report generation")
            return
            
        # Convert to DataFrame
        df = pd.DataFrame(self.measurement_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Create visualization
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Neurofibromatosis Monitoring System - Real-time Results', 
                     fontsize=16, fontweight='bold')
        
        # Plot 1: Bioimpedance over time
        axes[0,0].plot(df.index, df['resistance'], 'b-', label='Resistance', linewidth=2)
        axes[0,0].plot(df.index, df['reactance'], 'r-', label='Reactance', linewidth=2)
        axes[0,0].set_title('Bioimpedance Parameters')
        axes[0,0].set_xlabel('Measurement Cycle')
        axes[0,0].set_ylabel('Impedance (Ω)')
        axes[0,0].legend()
        axes[0,0].grid(True, alpha=0.3)
        
        # Plot 2: Nerve signal amplitude
        axes[0,1].plot(df.index, df['nerve_amplitude'], 'g-', linewidth=2)
        axes[0,1].set_title('Nerve Signal Amplitude')
        axes[0,1].set_xlabel('Measurement Cycle')
        axes[0,1].set_ylabel('Amplitude (mV)')
        axes[0,1].grid(True, alpha=0.3)
        
        # Plot 3: AI prediction confidence
        colors = ['green' if status == 'NORMAL' else 'red' for status in df['status']]
        axes[1,0].scatter(df.index, df['ai_prediction'], c=colors, alpha=0.7)
        axes[1,0].axhline(y=self.config['alert_threshold'], color='red', 
                         linestyle='--', label='Alert Threshold')
        axes[1,0].set_title('AI Prediction Confidence')
        axes[1,0].set_xlabel('Measurement Cycle')
        axes[1,0].set_ylabel('NF Probability')
        axes[1,0].legend()
        axes[1,0].grid(True, alpha=0.3)
        
        # Plot 4: Status distribution
        status_counts = df['status'].value_counts()
        axes[1,1].pie(status_counts.values, labels=status_counts.index, 
                     autopct='%1.1f%%', colors=['lightgreen', 'lightcoral'])
        axes[1,1].set_title('Overall Status Distribution')
        
        plt.tight_layout()
        plt.savefig('docs/nf_monitoring_results.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Print summary statistics
        print("\n📊 MONITORING SUMMARY REPORT")
        print("=" * 50)
        print(f"Total Measurements: {len(df)}")
        print(f"Normal Readings: {sum(df['status'] == 'NORMAL')} ({sum(df['status'] == 'NORMAL')/len(df)*100:.1f}%)")
        print(f"Abnormal Readings: {sum(df['status'] == 'ABNORMAL')} ({sum(df['status'] == 'ABNORMAL')/len(df)*100:.1f}%)")
        print(f"Average Resistance: {df['resistance'].mean():.1f} ± {df['resistance'].std():.1f} Ω")
        print(f"Average Reactance: {df['reactance'].mean():.1f} ± {df['reactance'].std():.1f} Ω")
        print(f"Average Nerve Amplitude: {df['nerve_amplitude'].mean():.2f} ± {df['nerve_amplitude'].std():.2f} mV")
        print(f"Average AI Confidence: {df['ai_prediction'].mean():.3f} ± {df['ai_prediction'].std():.3f}")
        
        return df

def main():
    """Main simulation function"""
    print("🏥 Neurofibromatosis Monitoring System Simulation")
    print("=" * 60)
    
    # Initialize monitoring system
    monitor = NeurofibromatosisMonitor()
    
    # Perform system calibration
    monitor.calibrate_system()
    
    # Run monitoring simulation
    print("\n🎯 Choose simulation scenario:")
    print("1. Normal monitoring (no NF)")
    print("2. NF detection simulation (NF appears after 30 seconds)")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "2":
        # Simulate NF condition appearing after 6 cycles (30 seconds)
        measurement_data = monitor.run_monitoring_cycle(
            duration_minutes=2, 
            nf_simulation_start=6
        )
    else:
        # Normal monitoring
        measurement_data = monitor.run_monitoring_cycle(duration_minutes=2)
    
    # Generate report
    monitor.generate_report()
    
    print("\n🎉 Simulation Complete!")
    print("📁 Results saved to 'docs/nf_monitoring_results.png'")

if __name__ == "__main__":
    main()