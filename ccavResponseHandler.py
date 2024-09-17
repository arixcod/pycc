#!/usr/bin/python

import json
from ccavutil import encrypt, decrypt


def res(encResp):
    '''
    Please put in the 32-bit alphanumeric key in quotes provided by CCAvenue.
    '''
    workingKey = '79B8D8AA336EDF95D51C1FA98272E119'
    
    # Decrypt the encrypted response
    decResp = decrypt(encResp, workingKey)
    
    # Split the decrypted response into key-value pairs
    key_value_pairs = decResp.split('&')
    
    # Create a dictionary to hold the parsed response
    response_dict = {}
    
    # Iterate over each key-value pair and add them to the dictionary
    for pair in key_value_pairs:
        if '=' in pair:
            key, value = pair.split('=')
            response_dict[key] = value
    
    # Convert the dictionary to a JSON response
    json_response = json.dumps(response_dict, indent=4)
    
    return json_response
