import json


def get_serialized(dict):
    if dict:
        return json.dumps(dict).encode('utf-8')
    else:
        return None
