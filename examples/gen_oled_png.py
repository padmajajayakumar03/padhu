#!/usr/bin/env python3
import sys
from PIL import Image, ImageDraw, ImageFont

# Usage: python gen_oled_png.py [output_path]
# Renders an OLED-like 128x64 UI and scales it for readability.

def main():
  out_path = sys.argv[1] if len(sys.argv) > 1 else "/workspace/examples/oled_output.png"

  width, height = 128, 64
  scale = 4  # upscale for readability
  img = Image.new("L", (width, height), color=0)
  d = ImageDraw.Draw(img)

  try:
    font = ImageFont.load_default()
  except Exception:
    font = None

  # Text content
  title = "Neurofibromatosis"
  z_line = "Z@30kHz: 1.02 kOhm"
  eng_line = "ENG RMS: 38 uV"

  # Draw text
  d.text((0, 0), title, fill=255, font=font)
  d.text((0, 12), z_line, fill=255, font=font)
  d.text((0, 24), eng_line, fill=255, font=font)

  # Bar graph (10 uV per pixel → 38 uV ≈ 4 px)
  bar_pixels = min(120, int(38 / 10 * 10))  # exaggerate a bit for visibility
  d.rectangle((0, 40, bar_pixels, 50), fill=255)

  # Upscale
  img_big = img.resize((width * scale, height * scale), resample=Image.NEAREST)
  img_big.save(out_path)
  print(out_path)

if __name__ == "__main__":
  main()