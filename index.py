import numpy as np
import png
import pydicom
import os
import sys

srcPath = sys.argv[1]
dstPath = sys.argv[2]
if not os.path.exists(dstPath):
    os.makedirs(dstPath)
files = os.listdir(srcPath)
for name in files:
  fileName = os.path.splitext(name)[0]
  print(fileName)
  ds = pydicom.dcmread(srcPath+'/'+fileName+'.dcm')
  shape = ds.pixel_array.shape

  # Convert to float to avoid overflow or underflow losses.
  image_2d = ds.pixel_array.astype(float)

  # Rescaling grey scale between 0-255
  image_2d_scaled = (np.maximum(image_2d,0) / image_2d.max()) * 512.0

  # Convert to uint
  image_2d_scaled = np.uint8(image_2d_scaled)

  # Write the PNG file
  writepath = dstPath+'/'+fileName+'.png'
  # mode = 'a' if os.path.exists(writepath) else 'w'
  with open(writepath, 'wb') as png_file:
      w = png.Writer(shape[1], shape[0], greyscale=True)
      w.write(png_file, image_2d_scaled)