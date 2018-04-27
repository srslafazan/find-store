# Find Store

A CLI tool for finding nearby stores

## Usage
```bash
find_store --address="<address>"
find_store --address="<address>" [--units=(mi|km)] [--output=text|json]
find_store --zip=<zip>
find_store --zip=<zip> [--units=(mi|km)] [--output=text|json]
```

## Setup
```bash
pip install -r requirements.txt
```

## Test
```bash
python setup.py test
```

## Implementation

User address or zip is geocoded to provide lat / long, which is then compared against all store lat longs to resolve closest store.

- Uses docopt python library to easily conform to docopts CLI standards
- Uses geopy to calculate distance between lat / long coordinates

> Note: speed of calculation would improve significantly with optimized store search patten. For instance, sorting the store list by long or lat would allow a near binary search pattern, etc.

> Note: arbitrary max retries is used for requests which can time out.

> Note: number of lat / long comparison operations increases linearly with number of store locations.