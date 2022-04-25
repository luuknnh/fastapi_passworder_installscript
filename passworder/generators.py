import codecs
import hashlib


class Generator:
    method = None

    def prep_string(self, hashable_string):
        if type(hashable_string) != str:
            raise ValueError("Password should be a string")
        if not str:
            raise ValueError("Password should not be empty")
        return hashable_string.encode()

    def hash(self, hashable_string, salt=None):
        hashable = self.prep_string(hashable_string)
        if salt:
            hash_result = self.method(hashable)
            hash_result.update(str(salt).encode())
            return hash_result.digest()
        else:
            hash_result = self.method(hashable).digest()
            return hash_result


class Sha512Generator(Generator):
    linux_num = 6
    method = hashlib.sha512


class Sha256Generator(Generator):
    linux_num = 5
    method = hashlib.sha256


class MD5Generator(Generator):
    linux_num = 1
    method = hashlib.md5


class Rot13Generator(Generator):
    linux_num = 0

    def hash(self, hashable_string, salt=None):
        return codecs.encode(hashable_string, "rot13").encode()
