# AWS Instance Metadata Fetcher

This script (aws_metadata_fetcher.py) queries the AWS Instance Metadata Service to retrieve metadata for an EC2 instance and outputs it in JSON format.

## Features
- Fetches detailed metadata from the AWS metadata service.
- Recursively explores nested metadata paths.
- Outputs the metadata in a structured and formatted JSON format.
- Handles errors gracefully with timeouts and exception handling.

## Prerequisites
- Python 3.x
- `requests` library installed. You can install it using:
  ```bash
  pip install requests
  ```

## Usage
1. Clone or download this repository.
2. Save the script as `aws_metadata_fetcher.py`.
3. Run the script on an EC2 instance or any environment with access to the AWS Instance Metadata Service:
   ```bash
   python aws_metadata_fetcher.py
   ```

## Output
The script outputs the instance metadata as a JSON-formatted object. Below is an example of what the output might look like:

```json
{
    "ami-id": "ami-0abcdef1234567890",
    "hostname": "ip-172-31-32-33.ec2.internal",
    "instance-id": "i-0123456789abcdef0",
    "instance-type": "t2.micro",
    "local-ipv4": "172.31.32.33",
    "public-ipv4": "203.x.xxx.25",
    "placement": {
        "availability-zone": "us-east-1a",
        "region": "us-east-1"
    },
    "security-groups": "default"
}
```

## Script Details
The script performs the following steps:
1. Connects to the AWS metadata service endpoint (`http://169.254.169.254/latest/meta-data/`).
2. Recursively retrieves all metadata, handling nested paths and subdirectories.
3. Formats the metadata as JSON and outputs it to the console.

### Code
Here is the core functionality:
```python
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
```

## Notes
- This script works only on AWS EC2 instances or environments with access to the AWS Instance Metadata Service.
- Ensure the instance has proper permissions and network configurations to access the metadata endpoint.
- Use this script responsibly, as it fetches sensitive instance information.

