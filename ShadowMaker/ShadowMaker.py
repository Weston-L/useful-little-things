"""
ShadowMaker.py
Drag a folder onto this file.

For every image in the folder:
  - Keep the original pixels untouched (no white removal).
  - Place the image on a larger transparent canvas.
  - Draw a soft drop shadow OUTSIDE / BEHIND the image on the transparent area.
  - Save as PNG named <foldername[:55]>-001.png, -002.png, ...
  - Delete the original file after the new PNG is saved.

  

Setup:
Install Python (check "Add to PATH")
Open Command Prompt and run: pip install Pillow
Put both files on your Desktop
Drag any folder with images onto ShadowMaker.py


"""

import os
import sys
from PIL import Image, ImageFilter

# ---- Shadow / canvas settings (tweak to taste) ----
CANVAS_PAD       = 50     # transparent padding added around the image (px)
SHADOW_BLUR      = 15     # gaussian blur radius for the shadow
SHADOW_OPACITY   = 220    # 0-255, how dark the shadow is
SHADOW_OFFSET_X  = 5      # horizontal shadow offset (px)
SHADOW_OFFSET_Y  = 15     # vertical shadow offset (px, positive = down)

SUPPORTED_EXT = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp")


def process_image(src_path: str, dst_path: str) -> None:
    img = Image.open(src_path).convert("RGBA")
    w, h = img.size

    canvas_w = w + CANVAS_PAD * 2
    canvas_h = h + CANVAS_PAD * 2

    # Shadow layer: solid rectangle the size of the image, blurred.
    shadow = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    rect = Image.new("RGBA", (w, h), (0, 0, 0, SHADOW_OPACITY))
    shadow.paste(
        rect,
        (CANVAS_PAD + SHADOW_OFFSET_X, CANVAS_PAD + SHADOW_OFFSET_Y),
        rect,
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(SHADOW_BLUR))

    # Final canvas: transparent, shadow first, then original image on top.
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    canvas.alpha_composite(shadow)
    canvas.alpha_composite(img, (CANVAS_PAD, CANVAS_PAD))

    canvas.save(dst_path, "PNG")


def main() -> None:
    if len(sys.argv) < 2:
        print("Drag a folder onto ShadowMaker.py (or pass a folder path).")
        return

    folder = os.path.abspath(sys.argv[1])
    if not os.path.isdir(folder):
        print(f"Not a folder: {folder}")
        return

    base = os.path.basename(folder.rstrip("\\/"))[:55]

    files = sorted(
        f for f in os.listdir(folder)
        if f.lower().endswith(SUPPORTED_EXT)
        and os.path.isfile(os.path.join(folder, f))
    )

    if not files:
        print("No images found.")
        return

    for i, name in enumerate(files, start=1):
        src = os.path.join(folder, name)
        dst = os.path.join(folder, f"{base}-{i:03d}.png")

        tmp_dst = dst + ".tmp.png"
        try:
            process_image(src, tmp_dst)
            if os.path.exists(dst):
                os.remove(dst)
            os.rename(tmp_dst, dst)
            if os.path.abspath(src) != os.path.abspath(dst):
                os.remove(src)
            print(f"OK  {name}  ->  {os.path.basename(dst)}")
        except Exception as e:
            if os.path.exists(tmp_dst):
                try: os.remove(tmp_dst)
                except: pass
            print(f"ERR {name}: {e}")

    print("Done.")


if __name__ == "__main__":
    main()
