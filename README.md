# HikIOT_signature

![GitHub last commit](https://img.shields.io/github/last-commit/Little-King2022/HikIOT_signature)
![GitHub Repo stars](https://img.shields.io/github/stars/Little-King2022/HikIOT_signature)

A Python program that generates MD5 signatures for HikIOT requests data.

The HTTP request body should be as follows, and the header contains a MD5 key named 'sign'.

![1730800346569](https://github.com/user-attachments/assets/bb49dd32-2ddd-4c37-813b-43b1ac73ff5e)

## Signature Analysis
This signature function creates a unique hash by sorting an input dictionary's keys, concatenating the key-value pairs into a string, and applying MD5 hashing twice. First, it generates an MD5 hash from the concatenated string. Then, it combines this hash (in uppercase) with a fixed salt string and hashes it again, returning the final result in uppercase. 

## Notice
The salt used for encryption may change in subsequent version updates. Welcome to Pull Requests and improve this project together.

## Usage
Pass the JSON data you need to send into the get_sign function, and then return the signature.
```python
from sign import get_sign

data = {
    "deviceSerial": "",
    "longitude": new_longitude,
    "latitude": new_latitude,
    "clockSite": "xxx",
    "address": "xxx",
    "deviceName": "xxx",
    "wifiName": "xxx",
    "wifiMac": "xxx"
}

data_sign = get_sign(data)
```

## Demo Server
This repo also provides a demo Flask API server in `demo_server.py`. You can build your own backend server.
