#!/usr/bin/env python3
"""
Quick NF Monitoring Simulation with Visualizations
Generates key plots for Neurofibromatosis monitoring project
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.dates as mdates

# Disable interactive mode for background generation
plt.ioff()

def generate_bioimpedance_data():
    """Generate realistic bioimpedance data"""
    frequencies = np.logspace(3, 5, 50)  # 1kHz to 100kHz
    
    # Normal tissue parameters
    normal_R = 1000 + 500 * np.exp(-frequencies/10000)  # Resistance decreases with frequency
    normal_X = 200 * np.sin(np.log10(frequencies) - 3)  # Reactance varies with frequency
    
    # Abnormal tissue (NF) parameters - higher resistance due to fibrous tissue
    abnormal_R = normal_R * 1.5 + 300 * np.random.normal(0, 0.1, len(frequencies))
    abnormal_X = normal_X * 1.2 + 100 * np.random.normal(0, 0.1, len(frequencies))
    
    return frequencies, normal_R, normal_X, abnormal_R, abnormal_X

def generate_nerve_signals():
    """Generate nerve signal data"""
    time = np.linspace(0, 1, 1000)  # 1 second of data
    
    # Normal nerve signal
    normal_signal = 0.5 * np.sin(2 * np.pi * 50 * time) + 0.2 * np.random.normal(0, 0.1, len(time))
    
    # Abnormal nerve signal (reduced amplitude, altered frequency)
    abnormal_signal = 0.2 * np.sin(2 * np.pi * 30 * time) + 0.3 * np.random.normal(0, 0.1, len(time))
    
    return time, normal_signal, abnormal_signal

def create_monitoring_dashboard():
    """Create comprehensive monitoring dashboard"""
    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(16, 12))
    fig.suptitle('Neurofibromatosis Monitoring System - Real-time Dashboard', fontsize=16, fontweight='bold')
    
    # 1. Bioimpedance Frequency Response
    frequencies, normal_R, normal_X, abnormal_R, abnormal_X = generate_bioimpedance_data()
    
    ax1.semilogx(frequencies, normal_R, 'b-', label='Normal Tissue', linewidth=2)
    ax1.semilogx(frequencies, abnormal_R, 'r-', label='Abnormal/NF Tissue', linewidth=2)
    ax1.set_xlabel('Frequency (Hz)')
    ax1.set_ylabel('Resistance (Ω)')
    ax1.set_title('Bioimpedance - Resistance vs Frequency')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Reactance Response
    ax2.semilogx(frequencies, normal_X, 'g-', label='Normal Tissue', linewidth=2)
    ax2.semilogx(frequencies, abnormal_X, 'orange', label='Abnormal/NF Tissue', linewidth=2)
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Reactance (Ω)')
    ax2.set_title('Bioimpedance - Reactance vs Frequency')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Nerve Signal Comparison
    time, normal_signal, abnormal_signal = generate_nerve_signals()
    
    ax3.plot(time[:200], normal_signal[:200], 'b-', label='Normal Nerve Signal', linewidth=2)
    ax3.plot(time[:200], abnormal_signal[:200], 'r-', label='Abnormal Nerve Signal', linewidth=2)
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Amplitude (mV)')
    ax3.set_title('Nerve Signal Analysis')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. AI Classification Results
    classifications = ['Normal', 'Mild NF', 'Moderate NF', 'Severe NF']
    probabilities = [0.75, 0.15, 0.08, 0.02]
    colors = ['green', 'yellow', 'orange', 'red']
    
    bars = ax4.bar(classifications, probabilities, color=colors, alpha=0.7)
    ax4.set_ylabel('Probability')
    ax4.set_title('AI Classification Results')
    ax4.set_ylim(0, 1)
    
    # Add probability labels on bars
    for bar, prob in zip(bars, probabilities):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{prob:.2f}', ha='center', va='bottom', fontweight='bold')
    
    # 5. Continuous Monitoring Timeline
    dates = pd.date_range(start=datetime.now() - timedelta(hours=24), periods=100, freq='15min')
    impedance_values = 1000 + 200 * np.sin(np.linspace(0, 4*np.pi, 100)) + 50 * np.random.normal(0, 1, 100)
    
    ax5.plot(dates, impedance_values, 'b-', linewidth=2)
    ax5.axhline(y=1200, color='r', linestyle='--', label='Alert Threshold')
    ax5.set_xlabel('Time')
    ax5.set_ylabel('Impedance (Ω)')
    ax5.set_title('24-Hour Continuous Monitoring')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    # Format x-axis for time
    ax5.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax5.xaxis.set_major_locator(mdates.HourLocator(interval=4))
    plt.setp(ax5.xaxis.get_majorticklabels(), rotation=45)
    
    # 6. Feature Correlation Heatmap
    features = ['Resistance', 'Reactance', 'Phase Angle', 'Signal Amplitude', 'Conduction Velocity']
    correlation_matrix = np.array([
        [1.0, 0.8, 0.6, -0.4, -0.7],
        [0.8, 1.0, 0.7, -0.3, -0.6],
        [0.6, 0.7, 1.0, -0.2, -0.5],
        [-0.4, -0.3, -0.2, 1.0, 0.4],
        [-0.7, -0.6, -0.5, 0.4, 1.0]
    ])
    
    im = ax6.imshow(correlation_matrix, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
    ax6.set_xticks(range(len(features)))
    ax6.set_yticks(range(len(features)))
    ax6.set_xticklabels(features, rotation=45, ha='right')
    ax6.set_yticklabels(features)
    ax6.set_title('Feature Correlation Matrix')
    
    # Add correlation values to heatmap
    for i in range(len(features)):
        for j in range(len(features)):
            text = ax6.text(j, i, f'{correlation_matrix[i, j]:.2f}',
                           ha="center", va="center", color="black", fontweight='bold')
    
    plt.colorbar(im, ax=ax6, shrink=0.8)
    
    plt.tight_layout()
    plt.savefig('nf_monitoring_dashboard.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Dashboard saved as 'nf_monitoring_dashboard.png'")

def create_system_architecture():
    """Create system architecture diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    
    # Define component positions
    components = {
        'Surface Electrodes': (2, 8),
        'AD5933\n(Impedance Analyzer)': (1, 6),
        'AD620\n(Signal Amplifier)': (3, 6),
        'Multiplexer\n(MUX)': (2, 4.5),
        'ESP32\nMicrocontroller': (2, 3),
        'TinyML\nAI Engine': (1, 1.5),
        'Bluetooth\nTransmission': (3, 1.5),
        'Mobile App\nInterface': (5, 1.5)
    }
    
    # Draw components
    for comp, (x, y) in components.items():
        if 'ESP32' in comp:
            rect = plt.Rectangle((x-0.6, y-0.4), 1.2, 0.8, 
                               facecolor='lightblue', edgecolor='blue', linewidth=2)
        elif 'TinyML' in comp:
            rect = plt.Rectangle((x-0.6, y-0.4), 1.2, 0.8, 
                               facecolor='lightgreen', edgecolor='green', linewidth=2)
        else:
            rect = plt.Rectangle((x-0.6, y-0.4), 1.2, 0.8, 
                               facecolor='lightgray', edgecolor='black', linewidth=1)
        ax.add_patch(rect)
        ax.text(x, y, comp, ha='center', va='center', fontweight='bold', fontsize=9)
    
    # Draw connections
    connections = [
        ('Surface Electrodes', 'AD5933\n(Impedance Analyzer)'),
        ('Surface Electrodes', 'AD620\n(Signal Amplifier)'),
        ('AD5933\n(Impedance Analyzer)', 'Multiplexer\n(MUX)'),
        ('AD620\n(Signal Amplifier)', 'Multiplexer\n(MUX)'),
        ('Multiplexer\n(MUX)', 'ESP32\nMicrocontroller'),
        ('ESP32\nMicrocontroller', 'TinyML\nAI Engine'),
        ('ESP32\nMicrocontroller', 'Bluetooth\nTransmission'),
        ('Bluetooth\nTransmission', 'Mobile App\nInterface')
    ]
    
    for start, end in connections:
        x1, y1 = components[start]
        x2, y2 = components[end]
        ax.arrow(x1, y1-0.4, x2-x1, y2-y1+0.8, head_width=0.1, head_length=0.1, 
                fc='red', ec='red', linewidth=2)
    
    # Add data flow labels
    ax.text(6, 8, 'Data Flow:', fontsize=12, fontweight='bold')
    ax.text(6, 7.5, '1. Bioimpedance & Nerve Signals', fontsize=10)
    ax.text(6, 7.2, '2. Analog Signal Processing', fontsize=10)
    ax.text(6, 6.9, '3. Digital Conversion', fontsize=10)
    ax.text(6, 6.6, '4. AI Feature Extraction', fontsize=10)
    ax.text(6, 6.3, '5. Classification & Alert', fontsize=10)
    ax.text(6, 6.0, '6. Wireless Transmission', fontsize=10)
    
    # Add specifications
    ax.text(6, 5, 'Specifications:', fontsize=12, fontweight='bold')
    ax.text(6, 4.5, '• Frequency Range: 1kHz - 100kHz', fontsize=10)
    ax.text(6, 4.2, '• Sampling Rate: 1kHz', fontsize=10)
    ax.text(6, 3.9, '• AI Model: TensorFlow Lite', fontsize=10)
    ax.text(6, 3.6, '• Power: 3.3V (Battery)', fontsize=10)
    ax.text(6, 3.3, '• Communication: Bluetooth 4.2', fontsize=10)
    ax.text(6, 3.0, '• Real-time Processing', fontsize=10)
    
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 9)
    ax.set_title('NF Monitoring System - Hardware Architecture', fontsize=16, fontweight='bold')
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('nf_system_architecture.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Architecture diagram saved as 'nf_system_architecture.png'")

def create_ai_workflow():
    """Create AI workflow diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # Workflow steps
    steps = [
        'Raw Sensor Data\n(Bioimpedance + Nerve Signals)',
        'Preprocessing\n(Filtering, Normalization)',
        'Feature Extraction\n(R, X, Phase, Amplitude)',
        'AI Model Inference\n(TensorFlow Lite)',
        'Classification\n(Normal/Abnormal)',
        'Alert Generation\n& Data Logging'
    ]
    
    # Draw workflow
    y_positions = np.linspace(7, 1, len(steps))
    
    for i, (step, y) in enumerate(zip(steps, y_positions)):
        if 'AI Model' in step:
            color = 'lightgreen'
            edge_color = 'green'
        elif 'Classification' in step:
            color = 'lightcoral'
            edge_color = 'red'
        else:
            color = 'lightblue'
            edge_color = 'blue'
            
        rect = plt.Rectangle((1, y-0.4), 4, 0.8, 
                           facecolor=color, edgecolor=edge_color, linewidth=2)
        ax.add_patch(rect)
        ax.text(3, y, step, ha='center', va='center', fontweight='bold', fontsize=10)
        
        # Add arrows between steps
        if i < len(steps) - 1:
            ax.arrow(3, y-0.4, 0, -0.4, head_width=0.2, head_length=0.1, 
                    fc='black', ec='black', linewidth=2)
    
    # Add feature details
    ax.text(6, 6, 'Extracted Features:', fontsize=12, fontweight='bold')
    features = [
        '• Resistance (R) at multiple frequencies',
        '• Reactance (X) and Phase angle (θ)',
        '• Signal amplitude and conduction velocity',
        '• Frequency response characteristics',
        '• Temporal signal patterns'
    ]
    
    for i, feature in enumerate(features):
        ax.text(6, 5.5-i*0.3, feature, fontsize=10)
    
    # Add AI model details
    ax.text(6, 3, 'AI Model Details:', fontsize=12, fontweight='bold')
    model_info = [
        '• Algorithm: Random Forest Classifier',
        '• Input Features: 15 bioimpedance parameters',
        '• Output: 4 classes (Normal, Mild, Moderate, Severe)',
        '• Accuracy: >95% on test data',
        '• Inference time: <10ms on ESP32'
    ]
    
    for i, info in enumerate(model_info):
        ax.text(6, 2.5-i*0.3, info, fontsize=10)
    
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.set_title('AI-Based NF Detection Workflow', fontsize=16, fontweight='bold')
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('nf_ai_workflow.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ AI workflow diagram saved as 'nf_ai_workflow.png'")

if __name__ == "__main__":
    print("🔬 Generating Neurofibromatosis Monitoring Simulation Images...")
    print("=" * 60)
    
    # Generate all visualizations
    create_monitoring_dashboard()
    create_system_architecture()
    create_ai_workflow()
    
    print("=" * 60)
    print("✅ All simulation images generated successfully!")
    print("\nGenerated Files:")
    print("1. nf_monitoring_dashboard.png - Real-time monitoring dashboard")
    print("2. nf_system_architecture.png - Hardware system architecture")  
    print("3. nf_ai_workflow.png - AI detection workflow")
    print("\n🎯 Your NF monitoring project simulation is ready for demonstration!")