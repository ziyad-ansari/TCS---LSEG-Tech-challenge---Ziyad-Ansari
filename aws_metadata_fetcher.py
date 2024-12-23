import requests
import json

def fetch_metadata(metadata_url="http://169.254.169.254/latest/meta-data/"):
    def get_metadata(url):
        try:
            response = requests.get(url, timeout=2)
            response.raise_for_status()
            if response.headers.get("Content-Type") == "text/plain":
                return response.text
            elif response.headers.get("Content-Type") == "application/json":
                return response.json()
            else:
                items = response.text.splitlines()
                metadata = {}
                for item in items:
                    item_url = url + item
                    if item.endswith("/"):  # Check for sub-paths
                        metadata[item[:-1]] = get_metadata(item_url)
                    else:
                        metadata[item] = requests.get(item_url).text
                return metadata
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    return get_metadata(metadata_url)

def main():
    metadata = fetch_metadata()
    print(json.dumps(metadata, indent=4))

if __name__ == "__main__":
    main()
