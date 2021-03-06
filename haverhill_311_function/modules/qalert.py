"""The QAlert module is a wrapper client around the QAlert API."""
from io import BytesIO

from . import settings
from . import db

import requests
import ijson


def pull():
    """
    Makes a GET request to fetch 311 Data from QAlert API and returns the data.
    """

    data = []
    if settings.TEST:
        url = settings.QALERT_REQUEST_ENDPOINT_TEST
    else:
        url = "{endpoint}?key={api_key}&count={count}&sort={sort}".format(
            endpoint=settings.QALERT_REQUEST_ENDPOINT,
            api_key=settings.QALERT_API_KEY,
            count=-1,
            sort="[createdate] asc,"
        )

        with db.QAlertAuditDB() as audit_db:
            latest_request = audit_db.get_latest_request()

        if latest_request is not None:
            url += f"&createDateMin={latest_request.create_date}"

    payload = {}
    headers = {'User-Agent': 'Custom'}
    response = requests.request(
        "GET", url, headers=headers, data=payload
    )

    if response.status_code != 200:
        return data

    data = ijson.items(BytesIO(response.content), 'item')
    return data
