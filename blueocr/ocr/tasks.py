# Create your tasks here
from __future__ import absolute_import, unicode_literals
from blueocr.ocr.celeryapp import app
from blueocr.ocr.models import OcrDocument, OcrResult, OcrUploadedFile
from blueocr.ocr.utils import adjust_data, is_image, convert_to_image
from django.core import serializers
from passporteye import read_mrz
import json
import os
import requests
import logging


logger = logging.getLogger(__name__)


@app.task
def scan_document(document_id):
    from blueocr.ocr.utils import create_contour_image
    doc = OcrDocument.objects.get(id=document_id)
    try:
        download_file = doc.download()
        logger.info("Downloaded file to {}".format(download_file))
    except Exception as e:
        logger.warning("Couldn't download file - {}".format(e))
        doc.enter_failed()
        doc.save()
        result = OcrResult.objects.create(state='failed', scanned_data={})
        doc.ocr_result = result
        doc.save()
    else:
        try:
            if not is_image(download_file):
                converted_file = convert_to_image(download_file)
                os.remove(download_file)
                download_file = converted_file
            mrz = read_mrz(download_file)
            if mrz is None or mrz.valid_score < 70:
                create_contour_image(download_file)
                mrz = read_mrz(download_file)
            if mrz is None:
                raise Exception("MRZ zone not identified")
        except Exception as e:
            logger.warning("Couldn't process document {} - {}".format(document_id, e))
            doc.enter_failed()
            result = OcrResult.objects.create(state='failed', scanned_data={})
            doc.ocr_result = result
            doc.save()
        else:
            mrz_dict = mrz.to_dict()
            adjust_data(mrz_dict)
            result = OcrResult.objects.create(state='completed', scanned_data=mrz_dict)
            doc.ocr_result = result
            logger.info("OCR finished for file document {}".format(doc))
            os.remove(download_file)
            doc.enter_processed()
            doc.save()
    send_callback(document_id)


@app.task
def scan_file(file_id):
    from blueocr.ocr.utils import create_contour_image
    doc = OcrUploadedFile.objects.get(id=file_id)
    try:
        download_file = doc.download()
        logger.info("Downloaded file to {}".format(download_file))
    except Exception as e:
        logger.warning("Couldn't download file - {}".format(e))
        doc.enter_failed()
        doc.save()
        result = OcrResult.objects.create(state='failed', scanned_data={})
        doc.ocr_result = result
        doc.save()
    else:
        try:
            if not is_image(download_file):
                converted_file = convert_to_image(download_file)
                os.remove(download_file)
                download_file = converted_file
            mrz = read_mrz(download_file)
            if mrz is None or mrz.valid_score < 70:
                create_contour_image(download_file)
                mrz = read_mrz(download_file)
            if mrz is None:
                raise Exception("MRZ zone not identified")
        except Exception as e:
            logger.warning("Couldn't process document {} - {}".format(file_id, e))
            doc.enter_failed()
            result = OcrResult.objects.create(state='failed', scanned_data={})
            doc.ocr_result = result
            doc.save()
        else:
            mrz_dict = mrz.to_dict()
            adjust_data(mrz_dict)
            result = OcrResult.objects.create(state='completed', scanned_data=mrz_dict)
            doc.ocr_result = result
            logger.info("OCR finished for file document {}".format(doc))
            os.remove(download_file)
            doc.enter_processed()
            doc.save()
    send_file_callback(file_id)


@app.task
def send_callback(document_id):
    doc = OcrDocument.objects.get(id=document_id)
    result = doc.ocr_result
    if doc.callback_url is None or doc.callback_url is "":
        logger.info("No callback to be executed for {}".format(doc))
        return
    json_data = serializers.serialize('json', [result,])
    json_obj = json.loads(json_data)
    r = requests.post(doc.callback_url, json=json_obj[0])


@app.task
def send_file_callback(document_id):
    doc = OcrUploadedFile.objects.get(id=document_id)
    result = doc.ocr_result
    if doc.callback_url is None or doc.callback_url is "":
        logger.info("No callback to be executed for {}".format(doc))
        return
    json_data = serializers.serialize('json', [result,])
    json_obj = json.loads(json_data)
    r = requests.post(doc.callback_url, json=json_obj[0])
