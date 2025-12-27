#-*- coding: utf-8 -*-
# b64wrap.py  (c)2022  Henrique Moreira

""" base64 wrapper for text files
"""

# pylint: disable=missing-function-docstring

from base64 import b64encode, b64decode

DEF_ENCODING = "ISO-8859-1"
#	...or UTF-8


class Codex():
    """ Codex abstract class """
    def __init__(self, name, encoding):
        self._encoding = encoding if encoding else DEF_ENCODING
        self.name = name
        self.header = None

    def get_encoding(self) -> str:
        return self._encoding


class Textual(Codex):
    """ Textual in/ out class
    """
    def __init__(self, name="", encoding=""):
        """ Initializer: name is any user name to be stored here, not a filename.
        """
        super().__init__(name, encoding)
        self._fname = ""
        self._lines = []

    def lines(self) -> list:
        """ Return textual lines """
        return self._lines

    def string(self) -> str:
        if self.header:
            astr = self.header
        else:
            astr = ""
        astr += ''.join(self._lines)
        return astr

    def load(self, fname:str, preserve_header="t") -> bool:
        """ Inject a specific table to this instance. """
        with open(fname, "r", encoding=self._encoding) as fdin:
            txt = fdin.readlines()
        self._lines = txt
        self.header = ""
        if not txt:
            return True
        if preserve_header in ("t",):
            first = txt[0]
            if first.startswith("#"):
                self.header, self._lines = first, txt[1:]
        return True

    def save(self, fname:str) -> bool:
        if self.header is None:
            return False
        astr = self.string()
        with open(fname, "wb") as fdout:
            fdout.write(astr.encode(self._encoding))
        return True

    def encode(self) -> bool:
        """ Encodes to base64 """
        txt = self._lines
        self._lines = [self._encode_text(line.rstrip("\n")) + "\n" for line in txt]
        return True

    def decode(self):
        txt = self._lines
        self._lines = [self._decode_text(line.rstrip("\n")) + "\n" for line in txt]
        return True

    def _encode_text(self, astr:str):
        new = b64encode(bytes(astr, self._encoding))
        return new.decode(self._encoding)

    def _decode_text(self, astr:str):
        new = b64decode(bytes(astr, self._encoding))
        return new.decode(self._encoding)


# Main script
if __name__ == "__main__":
    print("Please import me!")
    #  base64.b64encode(bytes(line.rstrip("\n"), "ISO-8859-1"))
