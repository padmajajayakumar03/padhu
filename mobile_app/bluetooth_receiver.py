#!/usr/bin/env python3
"""
Mobile App Bluetooth Receiver Simulation
========================================

This script simulates a mobile application that receives data from the 
ESP32 Neurofibromatosis monitoring device via Bluetooth.

Features:
- Bluetooth Low Energy (BLE) connection simulation
- Real-time data reception and processing
- Alert notifications
- Data logging and visualization
- Patient monitoring dashboard

Author: Padmaja
Date: 2024
"""

import json
import time
import threading
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import queue
import random

class NeurofibromatosisApp:
    """
    Mobile app simulation for receiving neurofibromatosis monitoring data
    """
    
    def __init__(self):
        self.setup_gui()
        self.data_queue = queue.Queue()
        self.monitoring_data = []
        self.alert_threshold = 0.7
        self.bluetooth_connected = False
        self.monitoring_active = False
        
    def setup_gui(self):
        """Initialize the GUI interface"""
        self.root = tk.Tk()
        self.root.title("Neurofibromatosis Monitor - Mobile App")
        self.root.geometry("800x700")
        self.root.configure(bg='#f0f0f0')
        
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="🏥 Neurofibromatosis Monitor", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Connection status frame
        conn_frame = ttk.LabelFrame(main_frame, text="📡 Connection Status", padding="5")
        conn_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_label = ttk.Label(conn_frame, text="❌ Disconnected", 
                                     font=('Arial', 10, 'bold'))
        self.status_label.grid(row=0, column=0, padx=(0, 10))
        
        self.connect_btn = ttk.Button(conn_frame, text="Connect to Device", 
                                     command=self.toggle_connection)
        self.connect_btn.grid(row=0, column=1)
        
        # Current readings frame
        readings_frame = ttk.LabelFrame(main_frame, text="📊 Current Readings", padding="10")
        readings_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Create reading displays
        ttk.Label(readings_frame, text="Resistance:").grid(row=0, column=0, sticky=tk.W)
        self.resistance_var = tk.StringVar(value="-- Ω")
        ttk.Label(readings_frame, textvariable=self.resistance_var, 
                 font=('Arial', 12, 'bold')).grid(row=0, column=1, sticky=tk.W, padx=(10, 20))
        
        ttk.Label(readings_frame, text="Reactance:").grid(row=0, column=2, sticky=tk.W)
        self.reactance_var = tk.StringVar(value="-- Ω")
        ttk.Label(readings_frame, textvariable=self.reactance_var, 
                 font=('Arial', 12, 'bold')).grid(row=0, column=3, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(readings_frame, text="Nerve Amplitude:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.nerve_var = tk.StringVar(value="-- mV")
        ttk.Label(readings_frame, textvariable=self.nerve_var, 
                 font=('Arial', 12, 'bold')).grid(row=1, column=1, sticky=tk.W, padx=(10, 20), pady=(5, 0))
        
        ttk.Label(readings_frame, text="AI Prediction:").grid(row=1, column=2, sticky=tk.W, pady=(5, 0))
        self.ai_var = tk.StringVar(value="--")
        self.ai_label = ttk.Label(readings_frame, textvariable=self.ai_var, 
                                 font=('Arial', 12, 'bold'))
        self.ai_label.grid(row=1, column=3, sticky=tk.W, padx=(10, 0), pady=(5, 0))
        
        # Status indicator
        status_frame = ttk.LabelFrame(main_frame, text="🚦 Status", padding="10")
        status_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_var = tk.StringVar(value="⚪ WAITING")
        self.status_indicator = ttk.Label(status_frame, textvariable=self.status_var, 
                                         font=('Arial', 14, 'bold'))
        self.status_indicator.grid(row=0, column=0)
        
        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=4, column=0, columnspan=3, pady=(0, 10))
        
        self.start_btn = ttk.Button(control_frame, text="▶️ Start Monitoring", 
                                   command=self.start_monitoring, state='disabled')
        self.start_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.stop_btn = ttk.Button(control_frame, text="⏹️ Stop Monitoring", 
                                  command=self.stop_monitoring, state='disabled')
        self.stop_btn.grid(row=0, column=1, padx=(0, 10))
        
        self.export_btn = ttk.Button(control_frame, text="📁 Export Data", 
                                    command=self.export_data, state='disabled')
        self.export_btn.grid(row=0, column=2)
        
        # Data visualization frame
        viz_frame = ttk.LabelFrame(main_frame, text="📈 Real-time Visualization", padding="5")
        viz_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Create matplotlib figure
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(8, 4))
        self.fig.tight_layout(pad=3.0)
        
        self.canvas = FigureCanvasTkAgg(self.fig, viz_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0)
        
        # Initialize plots
        self.setup_plots()
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
    def setup_plots(self):
        """Initialize the plotting areas"""
        self.ax1.set_title('Bioimpedance (Resistance & Reactance)')
        self.ax1.set_xlabel('Time (seconds)')
        self.ax1.set_ylabel('Impedance (Ω)')
        self.ax1.grid(True, alpha=0.3)
        
        self.ax2.set_title('AI Prediction Confidence')
        self.ax2.set_xlabel('Time (seconds)')
        self.ax2.set_ylabel('NF Probability')
        self.ax2.set_ylim(0, 1)
        self.ax2.axhline(y=self.alert_threshold, color='red', linestyle='--', 
                        label='Alert Threshold')
        self.ax2.legend()
        self.ax2.grid(True, alpha=0.3)
        
        self.canvas.draw()
        
    def toggle_connection(self):
        """Toggle Bluetooth connection"""
        if not self.bluetooth_connected:
            # Simulate connection
            self.bluetooth_connected = True
            self.status_label.config(text="✅ Connected to NF_Monitor_Device")
            self.connect_btn.config(text="Disconnect")
            self.start_btn.config(state='normal')
            messagebox.showinfo("Connection", "Successfully connected to Neurofibromatosis Monitor!")
        else:
            # Simulate disconnection
            self.bluetooth_connected = False
            self.status_label.config(text="❌ Disconnected")
            self.connect_btn.config(text="Connect to Device")
            self.start_btn.config(state='disabled')
            self.stop_monitoring()
            
    def start_monitoring(self):
        """Start receiving monitoring data"""
        if not self.bluetooth_connected:
            messagebox.showerror("Error", "Device not connected!")
            return
            
        self.monitoring_active = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.export_btn.config(state='disabled')
        
        # Start data simulation thread
        self.monitoring_thread = threading.Thread(target=self.simulate_data_reception)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
        
        # Start GUI update thread
        self.update_gui()
        
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring_active = False
        self.start_btn.config(state='normal' if self.bluetooth_connected else 'disabled')
        self.stop_btn.config(state='disabled')
        self.export_btn.config(state='normal' if self.monitoring_data else 'disabled')
        self.status_var.set("⏸️ STOPPED")
        
    def simulate_data_reception(self):
        """Simulate receiving data from ESP32 device"""
        start_time = time.time()
        cycle_count = 0
        
        while self.monitoring_active:
            cycle_count += 1
            current_time = time.time() - start_time
            
            # Simulate NF condition after 30 seconds for demonstration
            nf_simulation = current_time > 30
            
            # Generate simulated data
            if nf_simulation:
                resistance = random.uniform(1400, 1800)
                reactance = random.uniform(700, 1100)
                nerve_amplitude = random.uniform(0.3, 0.8)
                ai_prediction = random.uniform(0.75, 0.95)
            else:
                resistance = random.uniform(900, 1300)
                reactance = random.uniform(450, 750)
                nerve_amplitude = random.uniform(1.2, 2.0)
                ai_prediction = random.uniform(0.1, 0.4)
            
            # Create data packet
            data = {
                'timestamp': datetime.now().isoformat(),
                'resistance': round(resistance, 2),
                'reactance': round(reactance, 2),
                'phase': round(np.arctan2(reactance, resistance) * 180 / np.pi, 2),
                'nerve_amplitude': round(nerve_amplitude, 3),
                'conduction_velocity': round(random.uniform(35, 55), 1),
                'ai_prediction': round(ai_prediction, 3),
                'status': 'ABNORMAL' if ai_prediction > self.alert_threshold else 'NORMAL'
            }
            
            # Add to queue for GUI processing
            self.data_queue.put(data)
            
            time.sleep(5)  # 5-second intervals
            
    def update_gui(self):
        """Update GUI with new data"""
        try:
            # Process all queued data
            while not self.data_queue.empty():
                data = self.data_queue.get_nowait()
                self.process_new_data(data)
                
        except queue.Empty:
            pass
            
        # Schedule next update if monitoring is active
        if self.monitoring_active:
            self.root.after(100, self.update_gui)
            
    def process_new_data(self, data):
        """Process new data point"""
        # Update current readings
        self.resistance_var.set(f"{data['resistance']:.1f} Ω")
        self.reactance_var.set(f"{data['reactance']:.1f} Ω")
        self.nerve_var.set(f"{data['nerve_amplitude']:.2f} mV")
        self.ai_var.set(f"{data['ai_prediction']:.3f}")
        
        # Update status and color
        if data['status'] == 'ABNORMAL':
            self.status_var.set("🔴 ABNORMAL - ALERT!")
            self.ai_label.config(foreground='red')
            self.show_alert(data)
        else:
            self.status_var.set("🟢 NORMAL")
            self.ai_label.config(foreground='green')
            
        # Store data
        data['time'] = len(self.monitoring_data) * 5  # 5-second intervals
        self.monitoring_data.append(data)
        
        # Update plots
        self.update_plots()
        
    def show_alert(self, data):
        """Show alert notification"""
        alert_msg = f"⚠️ NEUROFIBROMATOSIS ALERT!\n\n"
        alert_msg += f"AI Confidence: {data['ai_prediction']:.3f}\n"
        alert_msg += f"Resistance: {data['resistance']:.1f} Ω\n"
        alert_msg += f"Nerve Signal: {data['nerve_amplitude']:.2f} mV\n\n"
        alert_msg += "Please consult your healthcare provider immediately."
        
        messagebox.showwarning("Medical Alert", alert_msg)
        
    def update_plots(self):
        """Update real-time plots"""
        if not self.monitoring_data:
            return
            
        # Extract data for plotting
        times = [d['time'] for d in self.monitoring_data]
        resistances = [d['resistance'] for d in self.monitoring_data]
        reactances = [d['reactance'] for d in self.monitoring_data]
        predictions = [d['ai_prediction'] for d in self.monitoring_data]
        
        # Clear and update bioimpedance plot
        self.ax1.clear()
        self.ax1.plot(times, resistances, 'b-', label='Resistance', linewidth=2)
        self.ax1.plot(times, reactances, 'r-', label='Reactance', linewidth=2)
        self.ax1.set_title('Bioimpedance (Resistance & Reactance)')
        self.ax1.set_xlabel('Time (seconds)')
        self.ax1.set_ylabel('Impedance (Ω)')
        self.ax1.legend()
        self.ax1.grid(True, alpha=0.3)
        
        # Clear and update AI prediction plot
        self.ax2.clear()
        colors = ['red' if d['status'] == 'ABNORMAL' else 'green' for d in self.monitoring_data]
        self.ax2.scatter(times, predictions, c=colors, alpha=0.7)
        self.ax2.axhline(y=self.alert_threshold, color='red', linestyle='--', 
                        label='Alert Threshold')
        self.ax2.set_title('AI Prediction Confidence')
        self.ax2.set_xlabel('Time (seconds)')
        self.ax2.set_ylabel('NF Probability')
        self.ax2.set_ylim(0, 1)
        self.ax2.legend()
        self.ax2.grid(True, alpha=0.3)
        
        # Refresh canvas
        self.canvas.draw()
        
    def export_data(self):
        """Export monitoring data to file"""
        if not self.monitoring_data:
            messagebox.showwarning("Export", "No data to export!")
            return
            
        try:
            # Save as JSON
            filename = f"nf_monitoring_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(self.monitoring_data, f, indent=2)
                
            # Generate summary report
            normal_count = sum(1 for d in self.monitoring_data if d['status'] == 'NORMAL')
            abnormal_count = len(self.monitoring_data) - normal_count
            avg_resistance = np.mean([d['resistance'] for d in self.monitoring_data])
            avg_prediction = np.mean([d['ai_prediction'] for d in self.monitoring_data])
            
            report = f"""
NEUROFIBROMATOSIS MONITORING REPORT
===================================
Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total Measurements: {len(self.monitoring_data)}
Normal Readings: {normal_count} ({normal_count/len(self.monitoring_data)*100:.1f}%)
Abnormal Readings: {abnormal_count} ({abnormal_count/len(self.monitoring_data)*100:.1f}%)
Average Resistance: {avg_resistance:.1f} Ω
Average AI Confidence: {avg_prediction:.3f}

Recommendation: {"Consult healthcare provider immediately" if abnormal_count > 0 else "Continue regular monitoring"}
"""
            
            report_filename = f"nf_monitoring_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(report_filename, 'w') as f:
                f.write(report)
                
            messagebox.showinfo("Export Complete", 
                              f"Data exported successfully!\n\n"
                              f"Files created:\n"
                              f"• {filename}\n"
                              f"• {report_filename}")
                              
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export data: {str(e)}")
            
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main function"""
    print("📱 Starting Neurofibromatosis Mobile App Simulation...")
    
    # Add numpy import for calculations
    import numpy as np
    globals()['np'] = np
    
    app = NeurofibromatosisApp()
    app.run()

if __name__ == "__main__":
    main()