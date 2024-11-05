import hashlib

def get_sign(t):
    # Sort the keys of the dictionary
    sorted_keys = sorted(t.keys())
    
    # Build the string
    o = ""
    for i, key in enumerate(sorted_keys):
        value = t[key]
        o += f"{key}={value}"
        if i < len(sorted_keys) - 1:
            o += "&"
    
    # Calculate MD5
    n = hashlib.md5(o.encode('utf-8')).hexdigest()
    
    # Concatenate fixed string and calculate MD5 again
    final_sign = hashlib.md5((n.upper() + "WE1mfER7artAoJEwXKaCjw==").encode('utf-8')).hexdigest().upper()
    
    return final_sign

# Example usage
example_dict = {
    "deviceSerial": "",
    "longitude": xxx,
    "latitude": xxx,
    "clockSite": "xxx",
    "address": "xxx",
    "deviceName": "微信小程序",
    "wifiName": "xxx",
    "wifiMac": "xxx"
}

sign = get_sign(example_dict)
print(sign)
