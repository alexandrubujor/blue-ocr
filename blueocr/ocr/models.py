from django.db import models
from django.contrib.postgres.fields import JSONField
from django_fsm import FSMField, transition, ConcurrentTransitionMixin
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from celery import current_app
from blueocr.ocr.utils import get_swift_token
import urllib.request
import os
import uuid
import logging

logger = logging.getLogger(__name__)


class OcrResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    scanned_data = JSONField()
    state = FSMField(default='created')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "OCR Result"
        verbose_name_plural = "OCR Results"

    def __str__(self):
        return '{}'.format(self.id)


class OcrDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document_url = models.URLField(blank=False)
    callback_url = models.URLField(blank=True)
    priority = models.IntegerField(default=10, blank=True)
    METHOD_SWIFT = "swift"
    METHOD_PLAIN = "plain"
    METHOD_TYPE = (
        (METHOD_PLAIN, 'Plain'),
        (METHOD_SWIFT, 'Swift')
    )
    method = models.CharField(max_length=20, choices=METHOD_TYPE, default=METHOD_PLAIN)
    ocr_result = models.ForeignKey(OcrResult, on_delete=models.SET_NULL, blank=True, null=True)
    state = FSMField(default='created')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "OCR Document"
        verbose_name_plural = "OCR Documents"

    def __str__(self):
        return '{}'.format(self.id)

    def create_ocr_task(self):
        current_app.send_task('blueocr.ocr.tasks.scan_document', args=(self.id,))

    def download(self):
        download_dir = settings.TEMP_DOWNLOADS
        if self.method == OcrDocument.METHOD_SWIFT:
            token = get_swift_token()
            print(token)
            opener = urllib.request.build_opener()
            opener.addheaders = [('X-Auth-Token', token)]
            urllib.request.install_opener(opener)
        try:
            download_file, h = urllib.request.urlretrieve(self.document_url, os.path.join(download_dir, "temp-{}".format(self.id)))
        except Exception as e:
            logger.info("Error while downloading file - {}".format(e))
            return None
        else:
            return download_file

    @transition(field=state, source='created', target='processed', on_error='error')
    def enter_processed(self):
        pass

    @transition(field=state, source='created', target='failed', on_error='error')
    def enter_failed(self):
        pass


@receiver(post_save, sender=OcrDocument)
def create_ocr_task(sender, instance, created, **kwargs):
    if created:
        doc = instance
        doc.create_ocr_task()


class OcrFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.FileField(blank=False, null=False)
    callback_url = models.URLField(blank=True)
    priority = models.IntegerField(default=10, blank=True)
    state = FSMField(default='created')
    ocr_result = models.ForeignKey(OcrResult, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "OCR File"
        verbose_name_plural = "OCR Files"

    def __str__(self):
        return '{}'.format(self.id)

    def create_ocr_task(self):
        current_app.send_task('blueocr.ocr.tasks.scan_file', args=(self.id,))

    @transition(field=state, source='created', target='processed', on_error='error')
    def enter_processed(self):
        pass

    @transition(field=state, source='created', target='failed', on_error='error')
    def enter_failed(self):
        pass

    def download(self):
        return os.path.join(settings.MEDIA_ROOT, str(self.document))


@receiver(post_save, sender=OcrFile)
def create_ocr_file_task(sender, instance, created, **kwargs):
    if created:
        doc = instance
        doc.create_ocr_task()


