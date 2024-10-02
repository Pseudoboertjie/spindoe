import imageio.v2 as imageio
import numpy as np
from pathlib import Path


file_path = Path().cwd() / "preprocessing"

image_path = file_path / "c.webp"
output_path = file_path / "c.png"

webp_img = imageio.imread(image_path)
png_img = webp_img.astype(np.uint8)
imageio.imwrite(output_path, png_img)