# blue-ocr

Blue OCR. Check out the project's [documentation](http://alexandrubujor.github.io/blue-ocr/).

# Description

A Django-based REST API for extracting data from scanned Passports and IDs (with mrz).

# Features

* Supply documents (images or PDFs) via URLs. Will be downloaded and processed by the API
* Process documents asynchronously and send callbacks for a snappy interaction

# Used components

* DRF (Django Rest Framework)
* Celery (for async tasks)
* [PassportEye](https://github.com/konstantint/PassportEye) (for ID processing)

# Contact & support

* email: alexandru.bujor at bluedrive.ro
* web: www.bluedrive.ro







