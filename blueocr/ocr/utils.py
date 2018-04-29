from django.conf import settings
import imghdr
import subprocess
import logging
import shlex

logger = logging.getLogger(__name__)


def adjust_data(data_dict):
    keys = data_dict.keys()
    for key in keys:
        if isinstance(data_dict[key], str):
            data_dict[key] = data_dict[key].strip(" <>")
    if 'sex' in keys:
        s = data_dict['sex']
        if s in "HK":
            data_dict['sex'] = 'M'
        if s in "PR":
            data_dict['sex'] = 'F'


def is_image(filename):
    image_type = imghdr.what(filename)
    logger.info("Detected image type {}".format(image_type))
    return image_type is not None


def convert_to_image(download_file):
    logger.info("Converting image {} to tiff".format(download_file))
    tiff_image = "{}.tiff".format(download_file)
    convert_shell = settings.CONVERT_SHELL
    convert_command = "{} -density 300 {} -depth 8 -strip -background white -alpha off {}".format(convert_shell, download_file, tiff_image)
    print(convert_command)
    try:
        subprocess.run(shlex.split(convert_command), check=True)
    except subprocess.CalledProcessError:
        return download_file
    logger.info("Conversion to tiff completed for {}".format(tiff_image))
    return tiff_image
