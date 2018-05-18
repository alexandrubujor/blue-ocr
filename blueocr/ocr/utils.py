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


def create_contour_image(image_file):
    import cv2
    logger.debug("Importing CV2")
    img = cv2.imread(image_file)
    logger.debug("Image read by CV2")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 127, 255, 0)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    logger.debug("Created Contour Image")
    cv2.imwrite(image_file, im2)
    logger.info("Saved new Contour image")


def get_swift_token():
    from keystoneauth1.identity import v3
    from keystoneauth1 import session

    auth_url = settings.SWIFT_KEYSTONE_URL
    username = settings.SWIFT_USERNAME
    password = settings.SWIFT_PASSWORD
    project_name = settings.SWIFT_PROJECT_NAME
    user_domain_id = settings.SWIFT_USER_DOMAIN
    project_domain_id = settings.SWIFT_PROJECT_DOMAIN
    auth = v3.Password(auth_url=auth_url, username=username, password=password,
                       project_name=project_name, user_domain_id=user_domain_id, project_domain_id=project_domain_id)
    sess = session.Session(auth=auth)
    token = auth.get_token(sess)
    return token
