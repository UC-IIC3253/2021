def _check_strings(*args):
    for arg in args:
        if not isinstance(arg, str):
            raise AttributeError("Expected a string")


def xor(k, m):
    _check_strings(k, m)

    result = ""
    for i in range(len(m)):
        result += chr((ord(k[i % len(k)]) ^ ord(m[i])) % 128)

    return result


def as_binary_strings(string):
    _check_strings(string)
    return [bin(n)[2:].zfill(7) for n in as_integers(string)]


def as_binary_string(string):
    _check_strings(string)
    return "".join(as_binary_strings(string))


def as_integers(string):
    _check_strings(string)
    return [ord(c) for c in string]


def print_as_binary(*args):
    _check_strings(*args)
    result = ""
    for a in args:
        result += as_binary_string(a) + "\n"
    print(result[:-1])
