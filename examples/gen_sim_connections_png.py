#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont

def draw_label(draw, xy, text, anchor="la", fill=(0,0,0), font=None):
  draw.text(xy, text, fill=fill, font=font, anchor=anchor)

def main():
  W, H = 1600, 1000
  bg = (255,255,255)
  img = Image.new("RGB", (W, H), bg)
  d = ImageDraw.Draw(img)
  try:
    font = ImageFont.load_default()
  except Exception:
    font = None

  # Colors
  black = (0,0,0)
  blue = (30, 90, 200)
  green = (0, 140, 60)
  red = (200, 40, 40)
  gray = (120,120,120)

  # Title
  draw_label(d, (W//2, 40), "AD620 Frontend Simulation Connections (Single-Supply, REF=1.65V)", anchor="mm", font=font)

  # Blocks coordinates
  # Electrodes
  ex, ey, ew, eh = 120, 180, 200, 120
  d.rectangle([ex, ey, ex+ew, ey+eh], outline=black, width=2)
  draw_label(d, (ex+ew/2, ey+eh/2), "Electrodes\n(ENG source)", anchor="mm", font=font)

  # Series protection 100k each side to HP caps
  # Left side nodes
  n_inp = (ex+ew+60, ey+30)  # IN+
  n_inn = (ex+ew+60, ey+eh-30)  # IN-

  # Draw resistors 100k
  def resistor(p1, p2, label):
    d.line([p1, p2], fill=black, width=2)
    mid = ((p1[0]+p2[0])//2, (p1[1]+p2[1])//2)
    draw_label(d, (mid[0], mid[1]-18), label, anchor="mm", font=font)

  # From electrodes to node via 100k
  e_outp = (ex+ew, ey+30)
  e_outn = (ex+ew, ey+eh-30)
  resistor(e_outp, n_inp, "100k")
  resistor(e_outn, n_inn, "100k")

  # AC coupling caps 1uF to AD620 inputs
  cap_off = 120
  cap_inp_r = (n_inp[0]+cap_off, n_inp[1])
  cap_inn_r = (n_inn[0]+cap_off, n_inn[1])
  # draw caps symbol
  def cap_symbol(p1, p2, label):
    # vertical plates
    x1,y1 = p1
    x2,y2 = p2
    d.line([p1, (x1+20, y1)], fill=black, width=2)
    d.line([(x1+30,y1-12), (x1+30,y1+12)], fill=black, width=2)
    d.line([(x1+40,y1-12), (x1+40,y1+12)], fill=black, width=2)
    d.line([(x1+50,y1), p2], fill=black, width=2)
    draw_label(d, (x1+35, y1-20), label, anchor="mm", font=font)
  cap_symbol(n_inp, cap_inp_r, "1uF")
  cap_symbol(n_inn, cap_inn_r, "1uF")

  # High value resistors to VREF (1Meg)
  vref_node = (W-260, 140)
  draw_label(d, (vref_node[0], vref_node[1]-24), "VREF = 1.65V", anchor="lm", font=font, fill=green)
  d.ellipse([vref_node[0]-6, vref_node[1]-6, vref_node[0]+6, vref_node[1]+6], outline=green, width=2)

  # Nodes after caps
  inp_hp = (cap_inp_r[0]+60, cap_inp_r[1])
  inn_hp = (cap_inn_r[0]+60, cap_inn_r[1])
  d.line([cap_inp_r, inp_hp], fill=black, width=2)
  d.line([cap_inn_r, inn_hp], fill=black, width=2)
  # 1Meg to Vref
  d.line([inp_hp, (inp_hp[0], inp_hp[1]-40)], fill=gray, width=2)
  d.line([inn_hp, (inn_hp[0], inn_hp[1]+40)], fill=gray, width=2)
  draw_label(d, (inp_hp[0]+30, inp_hp[1]-20), "1M to VREF", anchor="lm", font=font, fill=gray)
  draw_label(d, (inn_hp[0]+30, inn_hp[1]+20), "1M to VREF", anchor="lm", font=font, fill=gray)

  # Connect to VREF node with bus
  d.line([(inp_hp[0], inp_hp[1]-40), (vref_node[0], inp_hp[1]-40)], fill=green, width=2)
  d.line([(inn_hp[0], inn_hp[1]+40), (vref_node[0], inn_hp[1]+40)], fill=green, width=2)
  d.line([(vref_node[0], inp_hp[1]-40), vref_node], fill=green, width=2)
  d.line([(vref_node[0], inn_hp[1]+40), vref_node], fill=green, width=2)

  # AD620 block
  ax, ay, aw, ah = 860, 200, 260, 200
  d.rectangle([ax, ay, ax+aw, ay+ah], outline=blue, width=3)
  draw_label(d, (ax+aw/2, ay-16), "AD620 (G≈100)", anchor="mm", font=font, fill=blue)
  draw_label(d, (ax+10, ay+40), "IN+", anchor="lm", font=font, fill=blue)
  draw_label(d, (ax+10, ay+ah-40), "IN-", anchor="lm", font=font, fill=blue)
  draw_label(d, (ax+aw-10, ay+ah/2), "OUT", anchor="rm", font=font, fill=blue)
  draw_label(d, (ax+aw/2, ay+ah+18), "REF=1.65V", anchor="mm", font=font, fill=green)

  # Wires into AD620
  d.line([inp_hp, (ax, ay+40)], fill=black, width=2)
  d.line([inn_hp, (ax, ay+ah-40)], fill=black, width=2)

  # REF wire from VREF to AD620 bottom center
  d.line([vref_node, (ax+aw/2, ay+ah+6)], fill=green, width=2)

  # Power labels for AD620
  draw_label(d, (ax+aw+40, ay+20), "+5V", anchor="lm", font=font, fill=red)
  draw_label(d, (ax+aw+40, ay+ah-20), "GND", anchor="lm", font=font, fill=black)

  # Output RC to ADC
  out_node = (ax+aw, ay+ah/2)
  r_end = (out_node[0]+160, out_node[1])
  d.line([out_node, r_end], fill=black, width=2)
  draw_label(d, (out_node[0]+80, out_node[1]-18), "4.7k", anchor="mm", font=font)

  adc_node = (r_end[0]+180, r_end[1])
  d.line([r_end, adc_node], fill=black, width=2)
  draw_label(d, (adc_node[0]+6, adc_node[1]), "ESP32 ADC GPIO36", anchor="lm", font=font)

  # Cap 100n to GND at ADC node
  d.line([adc_node, (adc_node[0], adc_node[1]+60)], fill=black, width=2)
  d.line([(adc_node[0]-12, adc_node[1]+60), (adc_node[0]+12, adc_node[1]+60)], fill=black, width=3)
  d.line([(adc_node[0]-12, adc_node[1]+70), (adc_node[0]+12, adc_node[1]+70)], fill=black, width=3)
  draw_label(d, (adc_node[0]+30, adc_node[1]+40), "100nF", anchor="lm", font=font)
  draw_label(d, (adc_node[0], adc_node[1]+86), "GND", anchor="mm", font=font)

  # VREF generator box
  vx, vy, vw, vh = 1240, 80, 300, 120
  d.rectangle([vx, vy, vx+vw, vy+vh], outline=green, width=2)
  draw_label(d, (vx+vw/2, vy-14), "VREF Generator", anchor="mm", font=font, fill=green)
  draw_label(d, (vx+10, vy+30), "3.3V -> 10k / 10k -> 1.65V", anchor="lm", font=font, fill=green)
  draw_label(d, (vx+10, vy+70), "Decouple: 10uF || 100nF", anchor="lm", font=font, fill=green)

  # Notes
  draw_label(d, (W//2, H-40), "Simulate with LTspice netlist sim/ltspice/ad620_frontend.cir", anchor="mm", font=font, fill=gray)

  img.save("/workspace/examples/simulation_connections.png")
  print("/workspace/examples/simulation_connections.png")

if __name__ == "__main__":
  main()