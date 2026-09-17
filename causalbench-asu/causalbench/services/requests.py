import os.path
import sys
import tempfile

import requests
from requests import JSONDecodeError as RequestsJSONDecodeError
from bunch_py3 import bunchify

from causalbench.commons.constants import API_ENDPOINT
from causalbench.services.auth import get_access_token


def _get_auth_headers(force_login=False):
    return {
        'Authorization': f'Bearer {get_access_token(force_login=force_login)}'
    }


def _send_authenticated_request(send_request):
    response = send_request(_get_auth_headers())

    if response.status_code != 401:
        return response

    return send_request(_get_auth_headers(force_login=True))


def save_module(module_type, module_id, version, public, input_file, api_base, default_output_file):
    visibility = "public" if public else "private"
    if module_id is None:
        url = f'{API_ENDPOINT}/{api_base}/upload?visibility={visibility}'
    elif version is None:
        url = f'{API_ENDPOINT}/{api_base}/upload/{module_id}?visibility={visibility}'
    else:
        url = f'{API_ENDPOINT}/{api_base}/upload/{module_id}/{version}?visibility={visibility}'

    def send_request(headers):
        with open(input_file, 'rb') as file:
            files = {
                'file': (default_output_file, file, 'application/zip')
            }
            return requests.post(url, headers=headers, files=files)

    response = _send_authenticated_request(send_request)

    try:
        data = bunchify(response.json())

        if response.status_code == 200:
            print(f'Published {module_type} with module_id={data.id} and version={data.version_num} (visibility={visibility})', file=sys.stderr)
            return data.id, data.version_num

        else:
            print(f'Failed to publish {module_type} with module_id={module_id} and version={version}: {data.message} ({response.status_code})', file=sys.stderr)
            sys.exit(1)

    except (RequestsJSONDecodeError, AttributeError):
        print(f'Failed to publish {module_type} with module_id={module_id} and version={version}: {response.text} ({response.status_code})', file=sys.stderr)
        sys.exit(1)


def fetch_module(module_type, module_id, version, base_api, default_output_file):
    url = f'{API_ENDPOINT}/{base_api}/download/{module_id}/{version}'
    def send_request(headers):
        return requests.get(url, headers=headers)

    response = _send_authenticated_request(send_request)

    if response.status_code == 200:
        # Extract filename from the Content-Disposition header if available
        content_disposition = response.headers.get('Content-Disposition')
        if content_disposition:
            file_name = content_disposition.split('filename=')[-1].strip('"')
        else:
            # Fallback to a default name if the header is not present
            file_name = default_output_file

        file_path = os.path.join(tempfile.gettempdir(), file_name)
        with open(file_path, 'wb') as file:
            file.write(response.content)

        print(f'Fetched {module_type} with module_id={module_id} and version={version}', file=sys.stderr)
        return file_path

    else:
        try:
            data = bunchify(response.json())

            print(f'Failed to fetch {module_type} with module_id={module_id} and version={version}: {data.message} ({response.status_code})', file=sys.stderr)
            sys.exit(1)

        except (RequestsJSONDecodeError, AttributeError):
            print(f'Failed to fetch {module_type} with module_id={module_id} and version={version}: {response.text} ({response.status_code})', file=sys.stderr)
            sys.exit(1)
