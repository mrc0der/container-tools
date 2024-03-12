import requests
import json
import argparse

def list_images(registry_url):
    print(f"Connecting to registry at: {registry_url}")

    # Get a list of all repositories (images) in the registry
    try:
        response = requests.get(f'{registry_url}/v2/_catalog')
    except Exception as e:
        error_message = str(e)
        print(error_message) # handle the error message as appropriate

    repos = json.loads(response.content)['repositories']

    # For each repository, get a list of all tags (versions)
    for repo in repos:
        response = requests.get(f'{registry_url}/v2/{repo}/tags/list')
        tags = json.loads(response.content)['tags']

        # Print the repository name and all its tags
        print(f'{repo}:')
        for tag in tags:
            print(f'  {tag}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("registry_url", help="Registry URL = http://localhost:5000")
    args = parser.parse_args()

    # Reference the value of the registry_url parameter
    registry_url = args.registry_url
    list_images(registry_url)
