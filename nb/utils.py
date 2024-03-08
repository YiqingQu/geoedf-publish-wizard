import os
import subprocess
from datetime import datetime

import requests

from nb.config import GEOEDF_PORTAL_API_URL, PAGESIZE


def get_resource_list(page=1):
    """GeoEDF Portal API"""
    # make request to portal
    api_token = os.getenv('JUPYTERHUB_API_TOKEN')
    # log.debug(f"api_token = {api_token}")

    if not api_token:
        return None

    url = f"{GEOEDF_PORTAL_API_URL}/resource/list-user/"
    headers = {
        'Authorization': f'{api_token}',
    }
    params = {"page": page}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"Error fetching user resources: {response.status_code}")
        return None, 0, 0

    response_json = response.json()
    resource_list = response_json['results']['list']
    total_resources = response_json['results']['total']
    total_pages = total_resources // PAGESIZE + 1

    return resource_list, page, total_pages


def send_publish_request(target_path):
    """GeoEDF Portal API"""

    api_token = os.getenv('JUPYTERHUB_API_TOKEN')
    url = f"{GEOEDF_PORTAL_API_URL}/resource/publish/"
    headers = {
        'Authorization': f'{api_token}',
    }
    body_json = {"target_path": target_path}

    response = requests.post(url, headers=headers, json=body_json)
    if response.status_code != 200:
        print(f"Error fetching user info: {response.status_code}")
        return None
    response_json = response.json()
    resource_list = response_json['results']['list']


def copy_directories(sources_json, base_target):
    # Generate a unique timestamped target directory
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    target = os.path.join(base_target, timestamp)

    # create the timestamped subdirectory
    subprocess.run(['mkdir', '-p', target], check=True)
    print(f"Created target directory: {target}")

    responses = []

    for source in sources_json:
        source_name = source['name']
        source_path = source['path']
        specific_target = os.path.join(target, source_name)

        # create the specific target subdirectory
        subprocess.run(['mkdir', '-p', specific_target], check=True)

        if os.path.isdir(source_path):
            copy_cmd = ['cp', '-r', f"{source_path}/.", specific_target]
        elif os.path.isfile(source_path):
            copy_cmd = ['cp', source_path, specific_target]
        else:
            responses.append({"success": False, "message": f"Source path does not exist: {source_path}"})
            continue
        print(f"Created specific target for {source_name}: {specific_target}")

        try:
            # Execute the copy command
            subprocess.run(copy_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            responses.append({"success": True, "message": f"Copied {source_path} to {specific_target} successfully."})
        except subprocess.CalledProcessError as e:
            responses.append({"success": False,
                              "message": f"Failed to copy {source_path} to {specific_target}: {e.stderr.decode()}."})

    return target, responses
