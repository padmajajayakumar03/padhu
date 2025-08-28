#!/usr/bin/env python3
import math
from PIL import Image, ImageDraw, ImageFont

# Generate synthetic waveforms matching the LTspice netlist intent
# ENG diff = 250 uV pk @ 500 Hz
# AD620 G≈100 => OUT pk ≈ 25 mV around 1.65 V
# RC (4.7k, 100nF) low-pass => fc≈339 Hz, so 500 Hz attenuated ≈ 0.56

def generate_data(fs=20000, duration_s=0.05):
  n = int(fs*duration_s)
  t = [i/fs for i in range(n)]
  freq = 500.0
  vin_diff = [250e-6 * math.sin(2*math.pi*freq*ti) for ti in t]
  vref = 1.65
  vout = [vref + 100.0*vd for vd in vin_diff]  # 25 mV pk
  # Apply simple single-pole LPF to get ADC waveform
  rc = 4.7e3 * 100e-9
  alpha = (1.0/(fs*rc)) / (1.0 + 1.0/(fs*rc))
  y = vref
  vadc = []
  for x in vout:
    y = y + alpha*(x - y)
    vadc.append(y)
  return t, vout, vadc


def plot(t, v1, v2, labels=("V(OUT)", "V(ADC)")):
  W, H = 1600, 900
  img = Image.new("RGB", (W, H), (255,255,255))
  d = ImageDraw.Draw(img)
  try:
    font = ImageFont.load_default()
  except Exception:
    font = None

  # Margins and axes
  left, top, right, bottom = 120, 100, W-80, H-140
  d.rectangle([left, top, right, bottom], outline=(0,0,0), width=2)
  # Grid
  for i in range(1,10):
    x = left + i*(right-left)/10
    d.line([(x, top), (x, bottom)], fill=(230,230,230), width=1)
  for i in range(1,8):
    y = top + i*(bottom-top)/8
    d.line([(left, y), (right, y)], fill=(230,230,230), width=1)

  # Determine y-scale around 1.65V ±30 mV
  y_min, y_max = 1.65-0.035, 1.65+0.035
  def xy(tt, vv):
    x = left + (tt - t[0])/(t[-1]-t[0])*(right-left)
    y = bottom - (vv - y_min)/(y_max - y_min)*(bottom-top)
    return (int(x), int(y))

  # Title and labels
  d.text((W//2, 40), "Simulated Output: V(OUT) vs V(ADC)", fill=(0,0,0), anchor="mm", font=font)
  d.text((W//2, H-80), "Time (ms)", fill=(0,0,0), anchor="mm", font=font)
  d.text((60, (top+bottom)//2), "Voltage (V)", fill=(0,0,0), anchor="mm", font=font)

  # Draw waveforms (downsample for speed)
  colors = [(30,90,200), (200,40,40)]
  for series, color in zip([v1, v2], colors):
    last = None
    step = max(1, len(t)//2000)
    for i in range(0, len(t), step):
      pt = xy(t[i], series[i])
      if last is not None:
        d.line([last, pt], fill=color, width=2)
      last = pt

  # Legend
  d.rectangle([left+20, top+20, left+280, top+90], fill=(255,255,255), outline=(0,0,0))
  d.line([(left+40, top+40), (left+90, top+40)], fill=(30,90,200), width=3)
  d.text((left+100, top+40), labels[0], fill=(0,0,0), anchor="lm", font=font)
  d.line([(left+40, top+70), (left+90, top+70)], fill=(200,40,40), width=3)
  d.text((left+100, top+70), labels[1], fill=(0,0,0), anchor="lm", font=font)

  # Axis ticks (time)
  for i in range(6):
    tx = i*(t[-1]-t[0])/5
    x = left + i*(right-left)/5
    d.line([(x, bottom), (x, bottom+6)], fill=(0,0,0), width=2)
    d.text((x, bottom+24), f"{tx*1000:.0f}", fill=(0,0,0), anchor="mm", font=font)
  d.text((right+30, bottom+24), "ms", fill=(0,0,0), anchor="lm", font=font)

  # Axis ticks (voltage)
  for i in range(5):
    vy = y_min + i*(y_max-y_min)/4
    y = bottom - i*(bottom-top)/4
    d.line([(left-6, y), (left, y)], fill=(0,0,0), width=2)
    d.text((left-12, y), f"{vy:.3f}", fill=(0,0,0), anchor="rm", font=font)

  img.save("/workspace/examples/simulation_output.png")
  print("/workspace/examples/simulation_output.png")

if __name__ == "__main__":
  t, vout, vadc = generate_data()
  plot(t, vout, vadc)