

def log_dict(dict):
    for key, value in dict.items():
        pass

def is_in_string(substring, string_search):
    if substring in string_search:
        return True
    else:
        return False

# Check if string contains substring
def contains_substring(fullstring, substring, lowercase=True):
    if lowercase:
        substring = substring.lower()
        fullstring = fullstring.lower()
    if substring in fullstring:
        return 1
    else:
        return 0

# Hex to int
def hex_to_int(hex):
    if '0x' in str(hex):
        #print('hex ' + hex + ' int ' + str(int(hex, 16)))
        hex = hex[2:]
        return int(hex, 16)
    else:
        return hex
