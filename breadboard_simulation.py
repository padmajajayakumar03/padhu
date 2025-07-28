#!/usr/bin/env python3
"""
NF Monitoring System - Realistic Breadboard Connection Diagram
Shows exact wiring connections using real component representations

Author: Padmaja
Project: Embedded AI Neurofibromatosis Monitoring System
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, Polygon
import matplotlib.lines as mlines
import warnings
warnings.filterwarnings('ignore')

plt.ioff()  # Disable interactive mode

class BreadboardSimulation:
    """Creates realistic breadboard wiring diagrams with actual components"""
    
    def __init__(self):
        self.breadboard_color = '#F5F5DC'  # Beige
        self.hole_color = '#8B4513'        # Brown
        self.wire_colors = {
            'power': '#FF0000',      # Red
            'ground': '#000000',     # Black
            'signal': '#0000FF',     # Blue
            'i2c_sda': '#00FF00',    # Green
            'i2c_scl': '#FFFF00',    # Yellow
            'analog': '#FF6600',     # Orange
            'digital': '#9900FF',    # Purple
            'uart': '#FF1493'        # Deep Pink
        }
        
    def draw_breadboard(self, ax, x, y, width=15, height=10):
        """Draw a realistic breadboard"""
        # Main breadboard body
        breadboard = Rectangle((x, y), width, height, 
                             facecolor=self.breadboard_color, 
                             edgecolor='black', linewidth=2)
        ax.add_patch(breadboard)
        
        # Power rails (top and bottom)
        for rail_y in [y + height - 0.5, y + 0.5]:
            # Positive rail
            pos_rail = Rectangle((x + 0.5, rail_y - 0.2), width - 1, 0.4,
                               facecolor='red', alpha=0.3)
            ax.add_patch(pos_rail)
            # Negative rail  
            neg_rail = Rectangle((x + 0.5, rail_y - 0.6), width - 1, 0.4,
                               facecolor='blue', alpha=0.3)
            ax.add_patch(neg_rail)
        
        # Tie points (holes)
        rows = 30
        cols = 60
        for i in range(cols):
            for j in range(rows):
                hole_x = x + 0.5 + (i * (width-1)/cols)
                hole_y = y + 1 + (j * (height-2)/rows)
                hole = Circle((hole_x, hole_y), 0.05, 
                            facecolor=self.hole_color, edgecolor='black')
                ax.add_patch(hole)
        
        # Center divider
        divider = Rectangle((x + width/2 - 0.1, y + 1), 0.2, height - 2,
                          facecolor='gray', alpha=0.5)
        ax.add_patch(divider)
        
        # Labels
        ax.text(x + width/2, y + height + 0.5, 'Breadboard', 
               ha='center', va='center', fontweight='bold', fontsize=12)
        
        return breadboard
    
    def draw_esp32(self, ax, x, y):
        """Draw ESP32 development board"""
        # Main board
        board = Rectangle((x, y), 2.5, 1.2, facecolor='#4169E1', 
                        edgecolor='black', linewidth=2)
        ax.add_patch(board)
        
        # Chip
        chip = Rectangle((x + 0.8, y + 0.3), 0.9, 0.6, facecolor='black', 
                       edgecolor='gray', linewidth=1)
        ax.add_patch(chip)
        
        # Pins (left side)
        pin_labels_left = ['3V3', 'GND', 'GPIO21', 'GPIO22', 'GPIO34', 'GPIO35']
        for i, label in enumerate(pin_labels_left):
            pin_y = y + 0.1 + i * 0.17
            pin = Rectangle((x - 0.1, pin_y), 0.1, 0.05, facecolor='gold')
            ax.add_patch(pin)
            ax.text(x - 0.3, pin_y + 0.025, label, ha='right', va='center', 
                   fontsize=8, fontweight='bold')
        
        # Pins (right side)
        pin_labels_right = ['GPIO25', 'GPIO2', 'GPIO0', 'RX', 'TX', 'VIN']
        for i, label in enumerate(pin_labels_right):
            pin_y = y + 0.1 + i * 0.17
            pin = Rectangle((x + 2.5, pin_y), 0.1, 0.05, facecolor='gold')
            ax.add_patch(pin)
            ax.text(x + 2.7, pin_y + 0.025, label, ha='left', va='center', 
                   fontsize=8, fontweight='bold')
        
        ax.text(x + 1.25, y + 1.35, 'ESP32 DevKit', ha='center', va='center',
               fontweight='bold', fontsize=10)
        
        return [(x - 0.05, y + 0.125), (x + 2.55, y + 0.125)]  # Connection points
    
    def draw_ad5933(self, ax, x, y):
        """Draw AD5933 Impedance Analyzer breakout board"""
        # Main board
        board = Rectangle((x, y), 1.8, 1.0, facecolor='#8B0000', 
                        edgecolor='black', linewidth=2)
        ax.add_patch(board)
        
        # Chip
        chip = Rectangle((x + 0.4, y + 0.3), 1.0, 0.4, facecolor='black', 
                       edgecolor='gray', linewidth=1)
        ax.add_patch(chip)
        
        # Pins
        pin_labels = ['VCC', 'GND', 'SDA', 'SCL', 'OUT1', 'OUT2']
        for i, label in enumerate(pin_labels):
            pin_x = x + 0.1 + i * 0.28
            pin = Rectangle((pin_x, y - 0.1), 0.05, 0.1, facecolor='gold')
            ax.add_patch(pin)
            ax.text(pin_x + 0.025, y - 0.3, label, ha='center', va='center', 
                   fontsize=7, fontweight='bold', rotation=90)
        
        ax.text(x + 0.9, y + 1.15, 'AD5933', ha='center', va='center',
               fontweight='bold', fontsize=10)
        
        return [(x + 0.125 + i * 0.28, y - 0.05) for i in range(6)]  # Pin positions
    
    def draw_ad620(self, ax, x, y):
        """Draw AD620 Instrumentation Amplifier"""
        # Main board
        board = Rectangle((x, y), 1.5, 0.8, facecolor='#006400', 
                        edgecolor='black', linewidth=2)
        ax.add_patch(board)
        
        # Chip (8-pin DIP)
        chip = Rectangle((x + 0.35, y + 0.25), 0.8, 0.3, facecolor='black', 
                       edgecolor='gray', linewidth=1)
        ax.add_patch(chip)
        
        # Pins
        pin_labels = ['VCC', 'IN+', 'IN-', 'OUT', 'GND', 'RG1', 'RG2', 'REF']
        for i, label in enumerate(pin_labels):
            if i < 4:  # Left side
                pin_y = y + 0.1 + i * 0.15
                pin = Rectangle((x - 0.05, pin_y), 0.05, 0.05, facecolor='gold')
                ax.add_patch(pin)
                ax.text(x - 0.2, pin_y + 0.025, label, ha='right', va='center', 
                       fontsize=7, fontweight='bold')
            else:  # Right side
                pin_y = y + 0.1 + (i-4) * 0.15
                pin = Rectangle((x + 1.5, pin_y), 0.05, 0.05, facecolor='gold')
                ax.add_patch(pin)
                ax.text(x + 1.7, pin_y + 0.025, label, ha='left', va='center', 
                       fontsize=7, fontweight='bold')
        
        ax.text(x + 0.75, y + 0.9, 'AD620', ha='center', va='center',
               fontweight='bold', fontsize=10)
        
        return [(x - 0.025, y + 0.125 + i * 0.15) for i in range(4)] + \
               [(x + 1.525, y + 0.125 + i * 0.15) for i in range(4)]
    
    def draw_multiplexer(self, ax, x, y):
        """Draw CD4051 Multiplexer"""
        # Main board
        board = Rectangle((x, y), 1.6, 1.2, facecolor='#800080', 
                        edgecolor='black', linewidth=2)
        ax.add_patch(board)
        
        # Chip (16-pin DIP)
        chip = Rectangle((x + 0.3, y + 0.3), 1.0, 0.6, facecolor='black', 
                       edgecolor='gray', linewidth=1)
        ax.add_patch(chip)
        
        # Pins (simplified - showing key pins only)
        pin_labels = ['VCC', 'A0', 'A1', 'A2', 'INH', 'Y0-Y7', 'COM', 'GND']
        for i, label in enumerate(pin_labels):
            if i < 4:  # Left side
                pin_y = y + 0.2 + i * 0.2
                pin = Rectangle((x - 0.05, pin_y), 0.05, 0.05, facecolor='gold')
                ax.add_patch(pin)
                ax.text(x - 0.25, pin_y + 0.025, label, ha='right', va='center', 
                       fontsize=7, fontweight='bold')
            else:  # Right side
                pin_y = y + 0.2 + (i-4) * 0.2
                pin = Rectangle((x + 1.6, pin_y), 0.05, 0.05, facecolor='gold')
                ax.add_patch(pin)
                ax.text(x + 1.85, pin_y + 0.025, label, ha='left', va='center', 
                       fontsize=7, fontweight='bold')
        
        ax.text(x + 0.8, y + 1.35, 'CD4051 MUX', ha='center', va='center',
               fontweight='bold', fontsize=10)
        
        return [(x - 0.025, y + 0.225 + i * 0.2) for i in range(4)] + \
               [(x + 1.625, y + 0.225 + i * 0.2) for i in range(4)]
    
    def draw_electrodes(self, ax, x, y):
        """Draw surface electrodes"""
        # Electrode 1
        electrode1 = Circle((x, y), 0.3, facecolor='silver', 
                          edgecolor='black', linewidth=2)
        ax.add_patch(electrode1)
        # Wire connection
        wire_conn1 = Rectangle((x + 0.25, y - 0.05), 0.5, 0.1, 
                             facecolor='red', edgecolor='black')
        ax.add_patch(wire_conn1)
        
        # Electrode 2
        electrode2 = Circle((x + 2, y), 0.3, facecolor='silver', 
                          edgecolor='black', linewidth=2)
        ax.add_patch(electrode2)
        # Wire connection
        wire_conn2 = Rectangle((x + 1.25, y - 0.05), 0.5, 0.1, 
                             facecolor='blue', edgecolor='black')
        ax.add_patch(wire_conn2)
        
        ax.text(x, y - 0.6, 'Electrode 1\n(Impedance)', ha='center', va='center',
               fontweight='bold', fontsize=9)
        ax.text(x + 2, y - 0.6, 'Electrode 2\n(Nerve Signal)', ha='center', va='center',
               fontweight='bold', fontsize=9)
        
        return [(x + 0.75, y), (x + 1.25, y)]  # Connection points
    
    def draw_bluetooth_module(self, ax, x, y):
        """Draw Bluetooth module (HC-05/ESP32 built-in)"""
        # Module body
        module = Rectangle((x, y), 1.2, 0.8, facecolor='#00CED1', 
                         edgecolor='black', linewidth=2)
        ax.add_patch(module)
        
        # Antenna representation
        antenna = Rectangle((x + 0.1, y + 0.6), 1.0, 0.1, facecolor='gold')
        ax.add_patch(antenna)
        
        # Pins
        pin_labels = ['VCC', 'GND', 'RX', 'TX']
        for i, label in enumerate(pin_labels):
            pin_x = x + 0.15 + i * 0.25
            pin = Rectangle((pin_x, y - 0.1), 0.05, 0.1, facecolor='gold')
            ax.add_patch(pin)
            ax.text(pin_x + 0.025, y - 0.25, label, ha='center', va='center', 
                   fontsize=7, fontweight='bold')
        
        ax.text(x + 0.6, y + 0.9, 'Bluetooth', ha='center', va='center',
               fontweight='bold', fontsize=9)
        
        return [(x + 0.175 + i * 0.25, y - 0.05) for i in range(4)]
    
    def draw_power_supply(self, ax, x, y):
        """Draw 3.3V power supply/battery"""
        # Battery symbol
        battery = Rectangle((x, y), 1.0, 0.6, facecolor='#32CD32', 
                          edgecolor='black', linewidth=2)
        ax.add_patch(battery)
        
        # Positive terminal
        pos_term = Rectangle((x + 0.85, y + 0.2), 0.15, 0.2, facecolor='red')
        ax.add_patch(pos_term)
        
        # Negative terminal
        neg_term = Rectangle((x - 0.15, y + 0.2), 0.15, 0.2, facecolor='black')
        ax.add_patch(neg_term)
        
        ax.text(x + 0.5, y + 0.8, '3.3V Li-Po', ha='center', va='center',
               fontweight='bold', fontsize=9)
        ax.text(x + 0.925, y + 0.1, '+', ha='center', va='center',
               fontweight='bold', fontsize=12, color='white')
        ax.text(x - 0.075, y + 0.1, '-', ha='center', va='center',
               fontweight='bold', fontsize=12, color='white')
        
        return [(x + 0.925, y + 0.3), (x - 0.075, y + 0.3)]  # +/- terminals
    
    def draw_wire(self, ax, start, end, color, label='', style='-'):
        """Draw connecting wire with label"""
        x1, y1 = start
        x2, y2 = end
        
        # Draw wire
        line = ax.plot([x1, x2], [y1, y2], color=color, linewidth=3, 
                      linestyle=style, alpha=0.8)[0]
        
        # Add label at midpoint
        if label:
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mid_x, mid_y + 0.1, label, ha='center', va='center',
                   bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8),
                   fontsize=8, fontweight='bold')
        
        return line
    
    def create_breadboard_diagram(self):
        """Create complete breadboard wiring diagram"""
        fig, ax = plt.subplots(1, 1, figsize=(20, 14))
        
        # Draw breadboard
        breadboard = self.draw_breadboard(ax, 5, 5, 15, 10)
        
        # Component positions
        esp32_pos = (8, 16)
        ad5933_pos = (2, 12)
        ad620_pos = (12, 12)
        mux_pos = (8, 8)
        electrodes_pos = (2, 18)
        bluetooth_pos = (15, 16)
        power_pos = (1, 8)
        
        # Draw components
        esp32_pins = self.draw_esp32(ax, *esp32_pos)
        ad5933_pins = self.draw_ad5933(ax, *ad5933_pos)
        ad620_pins = self.draw_ad620(ax, *ad620_pos)
        mux_pins = self.draw_multiplexer(ax, *mux_pos)
        electrode_pins = self.draw_electrodes(ax, *electrodes_pos)
        bluetooth_pins = self.draw_bluetooth_module(ax, *bluetooth_pos)
        power_pins = self.draw_power_supply(ax, *power_pos)
        
        # Define connections
        connections = [
            # Power connections
            (power_pins[0], (5.5, 14.5), 'power', '3.3V'),  # Power rail
            (power_pins[1], (5.5, 4.5), 'ground', 'GND'),   # Ground rail
            
            # ESP32 power
            ((7.95, 16.125), (5.5, 14.5), 'power', '3.3V'),  # ESP32 VCC
            ((7.95, 16.295), (5.5, 4.5), 'ground', 'GND'),   # ESP32 GND
            
            # AD5933 connections
            (ad5933_pins[0], (5.5, 14.5), 'power', '3.3V'),     # AD5933 VCC
            (ad5933_pins[1], (5.5, 4.5), 'ground', 'GND'),      # AD5933 GND
            (ad5933_pins[2], (7.95, 16.465), 'i2c_sda', 'SDA'), # I2C SDA (GPIO21)
            (ad5933_pins[3], (7.95, 16.635), 'i2c_scl', 'SCL'), # I2C SCL (GPIO22)
            
            # AD620 connections
            (ad620_pins[0], (5.5, 14.5), 'power', '3.3V'),      # AD620 VCC
            (ad620_pins[4], (5.5, 4.5), 'ground', 'GND'),       # AD620 GND
            (ad620_pins[3], mux_pins[5], 'analog', 'Amp Out'),   # AD620 OUT to MUX
            
            # Multiplexer connections
            (mux_pins[0], (5.5, 14.5), 'power', '3.3V'),        # MUX VCC
            (mux_pins[7], (5.5, 4.5), 'ground', 'GND'),         # MUX GND
            (mux_pins[6], (7.95, 16.805), 'analog', 'COM'),     # MUX COM to ESP32 ADC
            (mux_pins[1], (10.55, 16.125), 'digital', 'A0'),    # MUX control GPIO25
            
            # Electrode connections
            (electrode_pins[0], ad5933_pins[4], 'signal', 'Imp+'), # Electrode 1 to AD5933
            (electrode_pins[1], ad620_pins[1], 'signal', 'Sig+'),  # Electrode 2 to AD620
            
            # Bluetooth (using ESP32 built-in)
            # UART connections already internal to ESP32
            
            # Additional ground connections
            (ad5933_pins[5], (5.5, 4.5), 'ground', 'Ref'),     # AD5933 reference
            (ad620_pins[7], (5.5, 4.5), 'ground', 'Ref'),      # AD620 reference
        ]
        
        # Draw all connections
        for start, end, color_key, label in connections:
            color = self.wire_colors.get(color_key, '#808080')
            self.draw_wire(ax, start, end, color, label)
        
        # Add component labels and specifications
        specs_text = """WIRING SPECIFICATIONS:
        
Power Supply: 3.3V Li-Po Battery
• Red wires: +3.3V power
• Black wires: Ground (GND)
• Blue wires: Signal lines
• Green wires: I2C SDA
• Yellow wires: I2C SCL
• Orange wires: Analog signals
• Purple wires: Digital control

Pin Connections:
ESP32 GPIO21 → AD5933 SDA
ESP32 GPIO22 → AD5933 SCL  
ESP32 GPIO34 → MUX COM (ADC)
ESP32 GPIO25 → MUX A0 (Control)
AD5933 OUT1 → Electrode 1
AD620 IN+ → Electrode 2
AD620 OUT → MUX Y0"""
        
        ax.text(22, 12, specs_text, fontsize=10, va='center',
               bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow', alpha=0.9))
        
        # Connection legend
        legend_elements = [
            mlines.Line2D([0], [0], color=self.wire_colors['power'], lw=3, label='Power (3.3V)'),
            mlines.Line2D([0], [0], color=self.wire_colors['ground'], lw=3, label='Ground'),
            mlines.Line2D([0], [0], color=self.wire_colors['i2c_sda'], lw=3, label='I2C SDA'),
            mlines.Line2D([0], [0], color=self.wire_colors['i2c_scl'], lw=3, label='I2C SCL'),
            mlines.Line2D([0], [0], color=self.wire_colors['analog'], lw=3, label='Analog Signal'),
            mlines.Line2D([0], [0], color=self.wire_colors['signal'], lw=3, label='Sensor Signal'),
            mlines.Line2D([0], [0], color=self.wire_colors['digital'], lw=3, label='Digital Control')
        ]
        
        ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))
        
        ax.set_xlim(-1, 25)
        ax.set_ylim(0, 22)
        ax.set_title('NF Monitoring System - Complete Breadboard Wiring Diagram', 
                    fontsize=16, fontweight='bold', pad=20)
        ax.axis('off')
        
        plt.tight_layout()
        plt.savefig('nf_breadboard_wiring.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✅ Breadboard wiring diagram saved as 'nf_breadboard_wiring.png'")
    
    def create_component_pinout_guide(self):
        """Create detailed component pinout reference"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # ESP32 Pinout
        ax1.set_xlim(0, 10)
        ax1.set_ylim(0, 10)
        
        # ESP32 diagram
        esp32_rect = Rectangle((2, 3), 6, 4, facecolor='#4169E1', 
                             edgecolor='black', linewidth=2)
        ax1.add_patch(esp32_rect)
        
        # Left pins
        left_pins = ['3V3', 'GND', 'GPIO21 (SDA)', 'GPIO22 (SCL)', 'GPIO34 (ADC)', 'GPIO35']
        for i, pin in enumerate(left_pins):
            y_pos = 6.5 - i * 0.6
            ax1.plot([1.5, 2], [y_pos, y_pos], 'k-', linewidth=2)
            ax1.text(1.4, y_pos, pin, ha='right', va='center', fontweight='bold', fontsize=9)
        
        # Right pins
        right_pins = ['GPIO25 (MUX)', 'GPIO2 (LED)', 'GPIO0', 'RX', 'TX', 'VIN']
        for i, pin in enumerate(right_pins):
            y_pos = 6.5 - i * 0.6
            ax1.plot([8, 8.5], [y_pos, y_pos], 'k-', linewidth=2)
            ax1.text(8.6, y_pos, pin, ha='left', va='center', fontweight='bold', fontsize=9)
        
        ax1.text(5, 5, 'ESP32', ha='center', va='center', fontweight='bold', 
                fontsize=14, color='white')
        ax1.set_title('ESP32 DevKit Pinout', fontweight='bold', fontsize=14)
        ax1.axis('off')
        
        # AD5933 Pinout
        ax2.set_xlim(0, 10)
        ax2.set_ylim(0, 10)
        
        ad5933_rect = Rectangle((2, 4), 6, 2, facecolor='#8B0000', 
                              edgecolor='black', linewidth=2)
        ax2.add_patch(ad5933_rect)
        
        ad5933_pins = ['VCC (3.3V)', 'GND', 'SDA', 'SCL', 'OUT1 (Electrode)', 'OUT2 (Ref)']
        for i, pin in enumerate(ad5933_pins):
            x_pos = 2.5 + i * 0.9
            ax2.plot([x_pos, x_pos], [3.5, 4], 'k-', linewidth=2)
            ax2.text(x_pos, 3.3, pin, ha='center', va='top', fontweight='bold', 
                    fontsize=8, rotation=45)
        
        ax2.text(5, 5, 'AD5933', ha='center', va='center', fontweight='bold', 
                fontsize=12, color='white')
        ax2.set_title('AD5933 Impedance Analyzer', fontweight='bold', fontsize=14)
        ax2.axis('off')
        
        # AD620 Pinout
        ax3.set_xlim(0, 10)
        ax3.set_ylim(0, 10)
        
        ad620_rect = Rectangle((3, 4), 4, 2, facecolor='#006400', 
                             edgecolor='black', linewidth=2)
        ax3.add_patch(ad620_rect)
        
        # Left pins
        left_pins_620 = ['VCC', 'IN+', 'IN-', 'REF']
        for i, pin in enumerate(left_pins_620):
            y_pos = 5.5 - i * 0.3
            ax3.plot([2.5, 3], [y_pos, y_pos], 'k-', linewidth=2)
            ax3.text(2.4, y_pos, pin, ha='right', va='center', fontweight='bold', fontsize=9)
        
        # Right pins
        right_pins_620 = ['OUT', 'GND', 'RG1', 'RG2']
        for i, pin in enumerate(right_pins_620):
            y_pos = 5.5 - i * 0.3
            ax3.plot([7, 7.5], [y_pos, y_pos], 'k-', linewidth=2)
            ax3.text(7.6, y_pos, pin, ha='left', va='center', fontweight='bold', fontsize=9)
        
        ax3.text(5, 5, 'AD620', ha='center', va='center', fontweight='bold', 
                fontsize=12, color='white')
        ax3.set_title('AD620 Instrumentation Amplifier', fontweight='bold', fontsize=14)
        ax3.axis('off')
        
        # Connection summary
        ax4.set_xlim(0, 10)
        ax4.set_ylim(0, 10)
        
        connection_text = """COMPLETE WIRING CONNECTIONS:

POWER DISTRIBUTION:
• 3.3V Battery → Power Rails
• All VCC pins → 3.3V Rail
• All GND pins → Ground Rail

I2C COMMUNICATION:
• ESP32 GPIO21 → AD5933 SDA
• ESP32 GPIO22 → AD5933 SCL
• 4.7kΩ pull-up resistors on SDA/SCL

SIGNAL PROCESSING:
• Electrode 1 → AD5933 OUT1 (Impedance)
• Electrode 2 → AD620 IN+ (Nerve Signal)
• AD620 OUT → MUX Y0
• MUX COM → ESP32 GPIO34 (ADC)

DIGITAL CONTROL:
• ESP32 GPIO25 → MUX A0 (Channel Select)
• ESP32 GPIO2 → Status LED

AMPLIFIER GAIN SETTING:
• AD620 RG1-RG2: 1.2kΩ (Gain = 1000)"""
        
        ax4.text(0.5, 5, connection_text, ha='left', va='center', fontweight='bold', 
                fontsize=10, transform=ax4.transData)
        ax4.set_title('Complete Wiring Summary', fontweight='bold', fontsize=14)
        ax4.axis('off')
        
        plt.suptitle('NF Monitoring System - Component Pinout & Wiring Guide', 
                    fontsize=16, fontweight='bold', y=0.98)
        
        plt.tight_layout()
        plt.savefig('nf_component_pinouts.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✅ Component pinout guide saved as 'nf_component_pinouts.png'")

def main():
    """Generate breadboard simulation images"""
    print("🔌 Generating NF Monitoring Breadboard Simulation...")
    print("=" * 60)
    
    simulator = BreadboardSimulation()
    
    # Generate breadboard diagrams
    simulator.create_breadboard_diagram()
    simulator.create_component_pinout_guide()
    
    print("=" * 60)
    print("✅ All breadboard simulation images generated successfully!")
    print("\nGenerated Files:")
    print("1. nf_breadboard_wiring.png - Complete breadboard wiring diagram")
    print("2. nf_component_pinouts.png - Detailed component pinout guide")
    print("\n🎯 Clear breadboard connections ready for implementation!")

if __name__ == "__main__":
    main()