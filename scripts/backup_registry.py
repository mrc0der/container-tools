"""A script to backup the Docker v2 registry."""

import argparse
import json
import os
import requests
# import shutil
# import sys
# import tarfile
# import tempfile

def list_images(registry_url):
    """List all images in a Docker v2 registry."""
    print(f"Connecting to registry at: {registry_url}")

    # Get a list of all repositories (images) in the registry
    try:
        response = requests.get(f'{registry_url}/v2/_catalog')
    except Exception as e:
        error_message = str(e)
        print(error_message) # handle the error message as appropriate

    repos = json.loads(response.content)['repositories']

    images = []

    # For each repository, get a list of all tags (versions)
    for repo in repos:
        response = requests.get(f'{registry_url}/v2/{repo}/tags/list')
        tags = json.loads(response.content)['tags']

        # Print the repository name and all its tags
        print(f'{repo}:')
        for tag in tags:
            print(f'  {tag}')
            images.append((repo, tag))

    return images

# use docker pull to download a local copy of the image
def pull_image(image_name, tag, registry_url):
    """Pull an image from a Docker v2 registry."""
    print(f"Pulling image: {image_name}:{tag}")
    os.system(f"docker pull {registry_url}/{image_name}:{tag}")

# use docker save to save the image to a tar file
def save_image(image_name, tag, registry_url, tar_file):
    """Save an image from a Docker v2 registry to a tar file."""
    print(f"Saving image: {image_name}:{tag}")
    os.system(f"docker save {registry_url}/{image_name}:{tag} -o {tar_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("registry_url", help="Registry URL = http://localhost:5000")
    parser.add_argument("backup_dir", help="Backup directory = /tmp/registry_backup")
    args = parser.parse_args()

    # Reference the value of the registry_url parameter
    registry_url = args.registry_url
    backup_dir = args.backup_dir

    # Create the backup directory if it does not exist
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Get a list of all images in the registry
    images = list_images(registry_url)

    # For each image, pull it from the registry and save it to a tar file
    for image in images:
        image_name = image[0]
        tag = image[1]
        tar_file = os.path.join(backup_dir, f"{image_name}_{tag}.tar")
        pull_image(image_name, tag, registry_url)
        save_image(image_name, tag, registry_url, tar_file)

    # # Compress the backup directory
    # shutil.make_archive(backup_dir, 'gztar', backup_dir)

    # # Delete the backup directory
    # shutil.rmtree(backup_dir)

    print("Backup complete.")
