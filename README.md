# blue-ocr

Blue OCR. Check out the project's [documentation](http://alexandrubujor.github.io/blue-ocr/).

# Description

A Django-based REST API for extracting data from scanned Passports and IDs (with mrz).

# Features

* Supply documents (images or PDFs) via URLs. Will be downloaded and processed by the API
* Process documents asynchronously and send callbacks for a snappy interaction

# REST Methods

### Send DOC for processing

POST http://127.0.0.1:8080/api/v1/ocr/ocrdocument/

```json
{
    "document_url": "http://5.154.188.179:8080/v1/AUTH_59255eb886674f5a9fa9b71b3e30fc9c/alex2/alex-passport.pdf",
    "callback_url": "http://bluedrive.proxy.beeceptor.com",
    "method": "swift",
    "priority": 12
}
```

### Receive Callback POSTed on the callback_url

```json
{
  "model": "ocr.ocrresult",
  "pk": "fdbac46e-4482-43dd-90ac-9f0d96aa7eeb",
  "fields": {
    "ocr_document": "58a96e97-5181-43c7-8601-f180911109a8",
    "scanned_data": {
      "sex": "M",
      "type": "PE",
      "names": "ALEXANDRU CATALIN",
      "method": "direct",
      "number": "1234561",
      "country": "ROU",
      "surname": "BUJOR",
      "mrz_type": "TD3",
      "nationality": "ROU",
      "valid_score": 100,
      "check_number": "9",
      "valid_number": true,
      "date_of_birth": "890816",
      "check_composite": "8",
      "expiration_date": "170823",
      "personal_number": "1234567890",
      "valid_composite": true,
      "check_date_of_birth": "8",
      "valid_date_of_birth": true,
      "check_expiration_date": "2",
      "check_personal_number": "1",
      "valid_expiration_date": true,
      "valid_personal_number": true
    },
    "state": "completed",
    "created": "2018-05-04T21:58:02.914Z",
    "updated": "2018-05-04T21:58:02.914Z"
  }
}
```

### Check document processing state

GET http://127.0.0.1:8080/api/v1/ocr/ocrdocument/58a96e97-5181-43c7-8601-f180911109a8/

```json
{
    "id": "58a96e97-5181-43c7-8601-f180911109a8",
    "document_url": "http://5.154.188.179:8080/v1/AUTH_59255eb886674f5a9fa9b71b3e30fc9c/alex2/alex-passport.pdf",
    "callback_url": "http://bluedrive.proxy.beeceptor.com",
    "method": "swift",
    "priority": 12,
    "state": "processed",
    "result": "fdbac46e-4482-43dd-90ac-9f0d96aa7eeb",
    "created": "2018-05-04T21:57:55+0000",
    "updated": "2018-05-04T21:58:02+0000"
}
```

### Check document result

GET http://127.0.0.1:8080/api/v1/ocr/ocrresult/fdbac46e-4482-43dd-90ac-9f0d96aa7eeb/

```json
{
    "id": "fdbac46e-4482-43dd-90ac-9f0d96aa7eeb",
    "ocr_document": "58a96e97-5181-43c7-8601-f180911109a8",
    "scanned_data": {
        "sex": "M",
        "type": "PE",
        "names": "ALEXANDRU CATALIN",
        "method": "direct",
        "number": "1234561",
        "country": "ROU",
        "surname": "BUJOR",
        "mrz_type": "TD3",
        "nationality": "ROU",
        "valid_score": 100,
        "check_number": "9",
        "valid_number": true,
        "date_of_birth": "890816",
        "check_composite": "8",
        "expiration_date": "170823",
        "personal_number": "1234567890",
        "valid_composite": true,
        "check_date_of_birth": "8",
        "valid_date_of_birth": true,
        "check_expiration_date": "2",
        "check_personal_number": "1",
        "valid_expiration_date": true,
        "valid_personal_number": true
    },
    "state": "completed",
    "created": "2018-05-04T21:58:02+0000",
    "updated": "2018-05-04T21:58:02+0000"
}
```


# Used components

* DRF (Django Rest Framework)
* Celery (for async tasks)
* [PassportEye](https://github.com/konstantint/PassportEye) (for ID processing)

# Contact & support

* email: alexandru.bujor at bluedrive.ro
* web: www.bluedrive.ro







