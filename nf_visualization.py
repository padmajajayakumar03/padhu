#!/usr/bin/env python3
"""
Neurofibromatosis Monitoring System - Data Visualization
Creates professional charts and graphs for project demonstration

Author: Padmaja
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings('ignore')

# Set style for professional plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class NFVisualization:
    """Creates visualizations for NF monitoring data"""
    
    def __init__(self):
        self.fig_size = (12, 8)
        self.dpi = 300
        
    def create_sample_data(self, n_samples=100):
        """Generate sample data for visualization"""
        np.random.seed(42)  # For reproducible results
        
        # Time series data
        start_time = datetime.now() - timedelta(hours=24)
        timestamps = [start_time + timedelta(minutes=15*i) for i in range(n_samples)]
        
        data = []
        
        for i, timestamp in enumerate(timestamps):
            # Simulate different patient conditions throughout the day
            if i < 30:  # Normal condition
                condition = "normal"
                resistance = np.random.normal(800, 50)
                reactance = np.random.normal(300, 30)
                nerve_amplitude = np.random.normal(50, 5)
                nerve_velocity = np.random.normal(55, 3)
                prediction = np.random.choice(['Normal'], p=[1.0])
                confidence = np.random.uniform(0.85, 0.98)
            elif i < 70:  # Mixed normal and early NF
                if np.random.random() < 0.8:
                    condition = "normal"
                    resistance = np.random.normal(800, 50)
                    reactance = np.random.normal(300, 30)
                    nerve_amplitude = np.random.normal(50, 5)
                    nerve_velocity = np.random.normal(55, 3)
                    prediction = 'Normal'
                    confidence = np.random.uniform(0.8, 0.95)
                else:
                    condition = "nf_early"
                    resistance = np.random.normal(1200, 80)
                    reactance = np.random.normal(450, 40)
                    nerve_amplitude = np.random.normal(35, 5)
                    nerve_velocity = np.random.normal(45, 4)
                    prediction = 'NF_Early'
                    confidence = np.random.uniform(0.7, 0.9)
            else:  # Advanced NF detection
                condition = "nf_advanced"
                resistance = np.random.normal(1800, 120)
                reactance = np.random.normal(650, 60)
                nerve_amplitude = np.random.normal(20, 8)
                nerve_velocity = np.random.normal(30, 6)
                prediction = 'NF_Advanced'
                confidence = np.random.uniform(0.8, 0.95)
            
            # Calculate derived values
            phase_angle = np.arctan(reactance / resistance) * (180 / np.pi)
            magnitude = np.sqrt(resistance**2 + reactance**2)
            
            data.append({
                'timestamp': timestamp,
                'resistance': max(50, resistance),
                'reactance': max(10, reactance),
                'phase_angle': phase_angle,
                'magnitude': magnitude,
                'nerve_amplitude': max(5, nerve_amplitude),
                'nerve_velocity': max(20, nerve_velocity),
                'prediction': prediction,
                'confidence': confidence,
                'condition': condition
            })
        
        return pd.DataFrame(data)
    
    def plot_impedance_time_series(self, df, save_path="impedance_timeline.png"):
        """Plot impedance parameters over time"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Bioimpedance Monitoring - 24 Hour Timeline\nNeurofibromatosis Detection System', 
                     fontsize=16, fontweight='bold')
        
        # Resistance plot
        axes[0,0].plot(df['timestamp'], df['resistance'], linewidth=2, color='blue', alpha=0.8)
        axes[0,0].set_title('Tissue Resistance', fontweight='bold')
        axes[0,0].set_ylabel('Resistance (Ω)')
        axes[0,0].grid(True, alpha=0.3)
        axes[0,0].axhline(y=800, color='green', linestyle='--', alpha=0.7, label='Normal Range')
        axes[0,0].axhline(y=1200, color='orange', linestyle='--', alpha=0.7, label='Early NF Threshold')
        axes[0,0].axhline(y=1800, color='red', linestyle='--', alpha=0.7, label='Advanced NF Threshold')
        axes[0,0].legend()
        
        # Reactance plot
        axes[0,1].plot(df['timestamp'], df['reactance'], linewidth=2, color='red', alpha=0.8)
        axes[0,1].set_title('Tissue Reactance', fontweight='bold')
        axes[0,1].set_ylabel('Reactance (Ω)')
        axes[0,1].grid(True, alpha=0.3)
        axes[0,1].axhline(y=300, color='green', linestyle='--', alpha=0.7, label='Normal Range')
        axes[0,1].axhline(y=450, color='orange', linestyle='--', alpha=0.7, label='Early NF Threshold')
        axes[0,1].legend()
        
        # Phase angle plot
        axes[1,0].plot(df['timestamp'], df['phase_angle'], linewidth=2, color='purple', alpha=0.8)
        axes[1,0].set_title('Phase Angle', fontweight='bold')
        axes[1,0].set_ylabel('Phase Angle (°)')
        axes[1,0].set_xlabel('Time')
        axes[1,0].grid(True, alpha=0.3)
        
        # Magnitude plot
        axes[1,1].plot(df['timestamp'], df['magnitude'], linewidth=2, color='orange', alpha=0.8)
        axes[1,1].set_title('Impedance Magnitude', fontweight='bold')
        axes[1,1].set_ylabel('Magnitude (Ω)')
        axes[1,1].set_xlabel('Time')
        axes[1,1].grid(True, alpha=0.3)
        
        # Format x-axis for all subplots
        for ax in axes.flat:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            ax.xaxis.set_major_locator(mdates.HourLocator(interval=4))
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
        plt.show()
        
    def plot_nerve_signal_analysis(self, df, save_path="nerve_signals.png"):
        """Plot nerve signal parameters"""
        fig, axes = plt.subplots(2, 1, figsize=(15, 10))
        fig.suptitle('Nerve Signal Analysis - Neurofibromatosis Detection\nEMG/ENG Signal Processing', 
                     fontsize=16, fontweight='bold')
        
        # Nerve amplitude plot
        axes[0].plot(df['timestamp'], df['nerve_amplitude'], linewidth=2, color='green', alpha=0.8)
        axes[0].set_title('Nerve Signal Amplitude', fontweight='bold')
        axes[0].set_ylabel('Amplitude (mV)')
        axes[0].grid(True, alpha=0.3)
        axes[0].axhline(y=50, color='green', linestyle='--', alpha=0.7, label='Normal Range (>45 mV)')
        axes[0].axhline(y=35, color='orange', linestyle='--', alpha=0.7, label='Early NF Range (30-45 mV)')
        axes[0].axhline(y=20, color='red', linestyle='--', alpha=0.7, label='Advanced NF (<30 mV)')
        axes[0].legend()
        
        # Nerve conduction velocity plot
        axes[1].plot(df['timestamp'], df['nerve_velocity'], linewidth=2, color='blue', alpha=0.8)
        axes[1].set_title('Nerve Conduction Velocity', fontweight='bold')
        axes[1].set_ylabel('Velocity (m/s)')
        axes[1].set_xlabel('Time')
        axes[1].grid(True, alpha=0.3)
        axes[1].axhline(y=55, color='green', linestyle='--', alpha=0.7, label='Normal Range (>50 m/s)')
        axes[1].axhline(y=45, color='orange', linestyle='--', alpha=0.7, label='Early NF Range (40-50 m/s)')
        axes[1].axhline(y=30, color='red', linestyle='--', alpha=0.7, label='Advanced NF (<40 m/s)')
        axes[1].legend()
        
        # Format x-axis
        for ax in axes:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            ax.xaxis.set_major_locator(mdates.HourLocator(interval=4))
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
        plt.show()
        
    def plot_ml_predictions(self, df, save_path="ml_predictions.png"):
        """Plot ML model predictions and confidence"""
        fig, axes = plt.subplots(2, 1, figsize=(15, 10))
        fig.suptitle('AI Model Predictions - TinyML Classification\nReal-time Neurofibromatosis Detection', 
                     fontsize=16, fontweight='bold')
        
        # Create color mapping for predictions
        color_map = {'Normal': 'green', 'NF_Early': 'orange', 'NF_Advanced': 'red'}
        colors = [color_map[pred] for pred in df['prediction']]
        
        # Prediction scatter plot
        for pred_type in ['Normal', 'NF_Early', 'NF_Advanced']:
            mask = df['prediction'] == pred_type
            if mask.any():
                axes[0].scatter(df[mask]['timestamp'], df[mask]['confidence'], 
                              c=color_map[pred_type], label=pred_type, alpha=0.7, s=50)
        
        axes[0].set_title('ML Model Predictions Over Time', fontweight='bold')
        axes[0].set_ylabel('Prediction Confidence')
        axes[0].grid(True, alpha=0.3)
        axes[0].legend()
        axes[0].set_ylim(0, 1)
        
        # Confidence plot
        axes[1].plot(df['timestamp'], df['confidence'], linewidth=2, color='purple', alpha=0.8)
        axes[1].fill_between(df['timestamp'], df['confidence'], alpha=0.3, color='purple')
        axes[1].set_title('Model Confidence Level', fontweight='bold')
        axes[1].set_ylabel('Confidence Score')
        axes[1].set_xlabel('Time')
        axes[1].grid(True, alpha=0.3)
        axes[1].axhline(y=0.8, color='green', linestyle='--', alpha=0.7, label='High Confidence (>0.8)')
        axes[1].axhline(y=0.6, color='orange', linestyle='--', alpha=0.7, label='Medium Confidence (0.6-0.8)')
        axes[1].legend()
        axes[1].set_ylim(0, 1)
        
        # Format x-axis
        for ax in axes:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            ax.xaxis.set_major_locator(mdates.HourLocator(interval=4))
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
        plt.show()
        
    def plot_system_overview(self, df, save_path="system_overview.png"):
        """Create comprehensive system overview dashboard"""
        fig = plt.figure(figsize=(20, 12))
        gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)
        
        fig.suptitle('Neurofibromatosis Monitoring System - Complete Dashboard\nEmbedded AI Bioimpedance Analysis by Padmaja', 
                     fontsize=18, fontweight='bold')
        
        # Main impedance plot
        ax1 = fig.add_subplot(gs[0, :2])
        ax1.plot(df['timestamp'], df['resistance'], linewidth=2, label='Resistance', color='blue')
        ax1.plot(df['timestamp'], df['reactance'], linewidth=2, label='Reactance', color='red')
        ax1.set_title('Bioimpedance Parameters', fontweight='bold', fontsize=14)
        ax1.set_ylabel('Impedance (Ω)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Nerve signals plot
        ax2 = fig.add_subplot(gs[0, 2:])
        ax2.plot(df['timestamp'], df['nerve_amplitude'], linewidth=2, label='Amplitude', color='green')
        ax2_twin = ax2.twinx()
        ax2_twin.plot(df['timestamp'], df['nerve_velocity'], linewidth=2, label='Velocity', color='orange')
        ax2.set_title('Nerve Signal Analysis', fontweight='bold', fontsize=14)
        ax2.set_ylabel('Amplitude (mV)', color='green')
        ax2_twin.set_ylabel('Velocity (m/s)', color='orange')
        ax2.legend(loc='upper left')
        ax2_twin.legend(loc='upper right')
        ax2.grid(True, alpha=0.3)
        
        # Prediction pie chart
        ax3 = fig.add_subplot(gs[1, 0])
        pred_counts = df['prediction'].value_counts()
        colors_pie = [color_map.get(pred, 'gray') for pred in pred_counts.index]
        color_map = {'Normal': '#2ecc71', 'NF_Early': '#f39c12', 'NF_Advanced': '#e74c3c'}
        ax3.pie(pred_counts.values, labels=pred_counts.index, autopct='%1.1f%%', 
                colors=colors_pie, startangle=90)
        ax3.set_title('Classification Results', fontweight='bold', fontsize=12)
        
        # Statistics box
        ax4 = fig.add_subplot(gs[1, 1])
        ax4.axis('off')
        stats_text = f"""SYSTEM STATISTICS
        
Total Measurements: {len(df)}
Average Resistance: {df['resistance'].mean():.1f} Ω
Average Reactance: {df['reactance'].mean():.1f} Ω
Avg Nerve Amplitude: {df['nerve_amplitude'].mean():.1f} mV
Avg Confidence: {df['confidence'].mean():.2%}

ALERTS GENERATED:
Normal: {(df['prediction'] == 'Normal').sum()}
Early NF: {(df['prediction'] == 'NF_Early').sum()}
Advanced NF: {(df['prediction'] == 'NF_Advanced').sum()}"""
        
        ax4.text(0.1, 0.9, stats_text, transform=ax4.transAxes, fontsize=10,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
        
        # Feature correlation heatmap
        ax5 = fig.add_subplot(gs[1, 2:])
        correlation_data = df[['resistance', 'reactance', 'nerve_amplitude', 'nerve_velocity', 'confidence']].corr()
        im = ax5.imshow(correlation_data, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
        ax5.set_xticks(range(len(correlation_data.columns)))
        ax5.set_yticks(range(len(correlation_data.columns)))
        ax5.set_xticklabels(correlation_data.columns, rotation=45)
        ax5.set_yticklabels(correlation_data.columns)
        ax5.set_title('Feature Correlation Matrix', fontweight='bold', fontsize=12)
        
        # Add correlation values
        for i in range(len(correlation_data.columns)):
            for j in range(len(correlation_data.columns)):
                text = ax5.text(j, i, f'{correlation_data.iloc[i, j]:.2f}',
                               ha="center", va="center", color="black", fontsize=8)
        
        # Timeline with alerts
        ax6 = fig.add_subplot(gs[2, :])
        
        # Plot main timeline
        ax6.plot(df['timestamp'], df['magnitude'], linewidth=2, color='purple', alpha=0.7, label='Impedance Magnitude')
        
        # Highlight alerts
        for idx, row in df.iterrows():
            if row['prediction'] != 'Normal':
                color = color_map[row['prediction']]
                ax6.axvline(x=row['timestamp'], color=color, alpha=0.5, linewidth=3)
                
        ax6.set_title('Alert Timeline - Anomaly Detection', fontweight='bold', fontsize=14)
        ax6.set_ylabel('Impedance Magnitude (Ω)')
        ax6.set_xlabel('Time')
        ax6.legend()
        ax6.grid(True, alpha=0.3)
        
        # Format time axis
        ax6.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax6.xaxis.set_major_locator(mdates.HourLocator(interval=4))
        plt.setp(ax6.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
        plt.show()
        
    def plot_circuit_diagram(self, save_path="circuit_diagram.png"):
        """Create a simplified circuit diagram visualization"""
        fig, ax = plt.subplots(1, 1, figsize=(14, 10))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 8)
        ax.set_aspect('equal')
        
        # Title
        ax.text(5, 7.5, 'NF Monitoring System - Circuit Block Diagram', 
                ha='center', va='center', fontsize=16, fontweight='bold')
        
        # Draw components
        components = [
            {'name': 'Surface\nElectrodes', 'pos': (1, 6), 'size': (1.2, 0.8), 'color': 'lightblue'},
            {'name': 'AD5933\nImpedance\nAnalyzer', 'pos': (3, 6.5), 'size': (1.2, 1), 'color': 'lightgreen'},
            {'name': 'AD620\nAmplifier\n(1000x)', 'pos': (3, 5), 'size': (1.2, 1), 'color': 'lightcoral'},
            {'name': 'MUX\nSelector', 'pos': (5.5, 5.75), 'size': (1, 1), 'color': 'lightyellow'},
            {'name': 'ESP32\nMicrocontroller\n+ TinyML', 'pos': (7.5, 5.75), 'size': (1.5, 1.5), 'color': 'lightpink'},
            {'name': 'Bluetooth\nTransmission', 'pos': (7.5, 3.5), 'size': (1.2, 0.8), 'color': 'lightsteelblue'},
            {'name': 'Mobile App\nAlert System', 'pos': (7.5, 1.5), 'size': (1.2, 1), 'color': 'lightgray'}
        ]
        
        for comp in components:
            rect = Rectangle((comp['pos'][0] - comp['size'][0]/2, comp['pos'][1] - comp['size'][1]/2), 
                           comp['size'][0], comp['size'][1], 
                           facecolor=comp['color'], edgecolor='black', linewidth=2)
            ax.add_patch(rect)
            ax.text(comp['pos'][0], comp['pos'][1], comp['name'], 
                   ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Draw connections
        connections = [
            ((1.6, 6), (2.4, 6.5)),      # Electrodes to AD5933
            ((1.6, 6), (2.4, 5)),        # Electrodes to AD620
            ((4.2, 6.5), (5, 6)),        # AD5933 to MUX
            ((4.2, 5), (5, 5.5)),        # AD620 to MUX
            ((6.5, 5.75), (6.75, 5.75)), # MUX to ESP32
            ((7.5, 5), (7.5, 4.3)),      # ESP32 to Bluetooth
            ((7.5, 2.7), (7.5, 2.5))     # Bluetooth to Mobile
        ]
        
        for start, end in connections:
            ax.annotate('', xy=end, xytext=start,
                       arrowprops=dict(arrowstyle='->', lw=2, color='blue'))
        
        # Add signal labels
        ax.text(2.2, 6.8, 'Bioimpedance\nSignal', ha='center', fontsize=8, color='blue')
        ax.text(2.2, 4.2, 'Nerve Signal\n(EMG/ENG)', ha='center', fontsize=8, color='red')
        ax.text(8.7, 5.75, 'AI\nClassification', ha='center', fontsize=8, color='purple')
        ax.text(8.7, 2.5, 'Real-time\nAlerts', ha='center', fontsize=8, color='green')
        
        # Add technical specifications
        specs_text = """Key Specifications:
• Frequency Range: 1kHz - 100kHz
• Amplifier Gain: 1000x
• AI Model: TensorFlow Lite
• Wireless: Bluetooth LE
• Real-time Processing"""
        
        ax.text(0.5, 3, specs_text, fontsize=10, 
               bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
        
        ax.set_title('Embedded AI System Architecture', fontsize=14, fontweight='bold', pad=20)
        ax.axis('off')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
        plt.show()

def main():
    """Generate all visualization plots"""
    print("🎨 Generating Neurofibromatosis Monitoring Visualizations...")
    print("=" * 60)
    
    # Create visualization instance
    viz = NFVisualization()
    
    # Generate sample data
    print("📊 Generating sample monitoring data...")
    df = viz.create_sample_data(100)
    
    # Create all visualizations
    print("📈 Creating impedance timeline plot...")
    viz.plot_impedance_time_series(df, "impedance_timeline.png")
    
    print("⚡ Creating nerve signal analysis plot...")
    viz.plot_nerve_signal_analysis(df, "nerve_signals.png")
    
    print("🧠 Creating ML predictions plot...")
    viz.plot_ml_predictions(df, "ml_predictions.png")
    
    print("📋 Creating system overview dashboard...")
    viz.plot_system_overview(df, "system_overview.png")
    
    print("🔌 Creating circuit diagram...")
    viz.plot_circuit_diagram("circuit_diagram.png")
    
    print("\n✅ All visualizations generated successfully!")
    print("📁 Files created:")
    print("   • impedance_timeline.png")
    print("   • nerve_signals.png") 
    print("   • ml_predictions.png")
    print("   • system_overview.png")
    print("   • circuit_diagram.png")
    print("\n🎯 Ready for project demonstration!")

if __name__ == "__main__":
    main()