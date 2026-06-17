"""
Drag a folder onto ebay_shadow.bat.
For every image in that folder:
  - removes the near-white background (makes it transparent)
  - adds a soft drop shadow below the subject
  - enlarges canvas to fit the shadow
  - saves as PNG named <folder>-001.png, <folder>-002.png, ...
  - deletes the original
Folder-name prefix is truncated to 55 chars.



Setup:
Install Python (check "Add to PATH")
Open Command Prompt and run: pip install Pillow
Put both files on your Desktop
Drag any folder with images onto ebay_shadow.bat


"""

import sys, os, re
from pathlib import Path
from PIL import Image, ImageFilter, ImageChops

# ---- tuning ----
WHITE_THRESHOLD = 230     # pixels brighter than this on all channels => transparent
SHADOW_BLUR     = 15      # softness of the shadow
SHADOW_OPACITY  = 150     # 0-255
SHADOW_OFFSET_Y = 3      # how far below the subject
SHADOW_OFFSET_X = 3
CANVAS_PAD      = 100      # extra space around so shadow isn't clipped
EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}

def remove_white_bg(img: Image.Image) -> Image.Image:
    img = img.convert("RGBA")
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if r >= WHITE_THRESHOLD and g >= WHITE_THRESHOLD and b >= WHITE_THRESHOLD:
                px[x, y] = (255, 255, 255, 0)
    return img

def add_shadow(img: Image.Image) -> Image.Image:
    w, h = img.size
    new_w = w + CANVAS_PAD * 2
    new_h = h + CANVAS_PAD * 2
    canvas = Image.new("RGBA", (new_w, new_h), (0, 0, 0, 0))

    # build shadow from alpha channel
    alpha = img.split()[-1]
    shadow = Image.new("RGBA", (new_w, new_h), (0, 0, 0, 0))
    black = Image.new("RGBA", (w, h), (0, 0, 0, SHADOW_OPACITY))
    shadow.paste(black, (CANVAS_PAD + SHADOW_OFFSET_X, CANVAS_PAD + SHADOW_OFFSET_Y), alpha)
    shadow = shadow.filter(ImageFilter.GaussianBlur(SHADOW_BLUR))

    canvas = Image.alpha_composite(canvas, shadow)
    canvas.paste(img, (CANVAS_PAD, CANVAS_PAD), img)
    return canvas

def process_folder(folder: Path):
    if not folder.is_dir():
        print(f"Not a folder: {folder}"); return
    prefix = re.sub(r'[<>:"/\\|?*]', "_", folder.name)[:55]
    files = sorted([p for p in folder.iterdir() if p.suffix.lower() in EXTS])
    if not files:
        print("No images found."); return

    print(f"Processing {len(files)} image(s) in {folder}")
    for i, src in enumerate(files, start=1):
        try:
            img = Image.open(src)
            img = remove_white_bg(img)
            out = add_shadow(img)
            dst = folder / f"{prefix}-{i:03d}.png"
            # avoid clobbering source before saving
            tmp = folder / f"__tmp_{i:03d}.png"
            out.save(tmp, "PNG")
            src.unlink()
            tmp.rename(dst)
            print(f"  {src.name} -> {dst.name}")
        except Exception as e:
            print(f"  FAILED {src.name}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Drop a folder onto ebay_shadow.bat")
        input("Press Enter to exit..."); sys.exit(0)
    for arg in sys.argv[1:]:
        process_folder(Path(arg))
    input("Done. Press Enter to exit...")
