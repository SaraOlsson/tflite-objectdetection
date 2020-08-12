#import cv2
#import numpy as np
from PIL import Image, ImageDraw

#import io
#import json
#import dropbox

from .variables import *

# crop Pillow img
def im_crop_center(img, w, h):
    img_width, img_height = img.size
    left, right = (img_width - w) / 2, (img_width + w) / 2
    top, bottom = (img_height - h) / 2, (img_height + h) / 2
    left, top = round(max(0, left)), round(max(0, top))
    right, bottom = round(min(img_width - 0, right)), round(min(img_height - 0, bottom))
    return img.crop((left, top, right, bottom))

def our_annotation_draw(image, boxes, scores, classes, threshold, width, heigth, approved_statuses = None):

  draw = ImageDraw.Draw(image)

  """Draws the bounding box and label for each object in the results."""
  for idx,box in enumerate(boxes):
    # Convert the bounding box figures from relative coordinates
    # to absolute coordinates based on the original resolution

    if scores[idx] >= threshold:
      #continue

      ymin, xmin, ymax, xmax = box
      xmin = int(xmin * width)
      xmax = int(xmax * width)
      ymin = int(ymin * heigth)
      ymax = int(ymax * heigth)

      label = category_index[classes[idx]]["name"]

      if approved_statuses != None:

        outline_color = 'green' if approved_statuses[idx] == True else 'red'

      else:
        outline_color = 'white'

      draw.rectangle(((xmin, ymin), (xmax, ymax)), outline= outline_color, fill=None)
      draw.text((xmin, ymin), '%s\n%.3f' % (label, scores[idx]))

  return image

"""
def threaded_images_to_dropbox(dbx, images_to_save, db_folder, filename_prefix, filename_ids):

  for (idx,image_to_save) in enumerate(images_to_save):

    output = io.BytesIO()
    image_to_save.save(output, format='JPEG')

    hex_data = output.getvalue()

    filename = filename_prefix + filename_ids[idx] + '.jpg' # filename_prefix + '_' + filename_ids[idx] + '.jpg'
    path = db_folder + filename

    mode = dropbox.files.WriteMode.add

    try:
        res = dbx.files_upload(hex_data, path, mode,mute=True)
        print('dropbox img upload', filename)
    except dropbox.exceptions.ApiError as err:
        print('*** API error for image', err)

def threaded_meta_to_dropbox(dbx, metadata_objs, db_folder, filename_prefix, filename_ids):

  for (idx, meta_to_save) in enumerate(metadata_objs):

    filename = filename_prefix + filename_ids[idx] + '.json'
    path = db_folder + filename

    dumped_json_string = json.dumps(meta_to_save)
    b_string = dumped_json_string.encode('utf-8')
    meta_data = io.BytesIO(b_string)
    meta_hex_data = meta_data.getvalue()

    mode = dropbox.files.WriteMode.add

    try:
        res = dbx.files_upload(meta_hex_data, path, mode,mute=True)
        print('dropbox meta upload', filename)
    except dropbox.exceptions.ApiError as err:
        print('*** API error for textfile', err)
"""
