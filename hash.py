import hashlib
print(hashlib)
def convertTohash(data, type):
    if type not in ("MD5", "SHA1", "sha224", "SHA256", "sha384", "shake_128", "blake2s", "blake2b", "shake_128"):
        return None 
    match type:
        case "SHA256":
            return (hashlib.sha256(data.encode())).hexdigest()
        case "SHA1":
            return hashlib.sha1(data.encode()).hexdigest()
        case "MD5":
            return hashlib.md5(data.encode()).hexdigest()
        case "sha224":
            return hashlib.sha224(data.encode()).hexdigest()
        case "sha384":
            return hashlib.sha384(data.encode()).hexdigest()
        case "sha3_256":
            return hashlib.sha3_256(data.encode()).hexdigest()
        case "shake_128":
            return hashlib.shake_128(data.encode()).hexdigest(16)
        case "blake2s":
            return hashlib.blake2s(data.encode()).hexdigest()
        case "blake2b":
            return hashlib.blake2b(data.encode()).hexdigest()
        