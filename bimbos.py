#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Make a base64 encoded version of bimbos.txt, or show it.

Author: Henrique Moreira, h@serrasqueiro.com
"""

# pylint: disable=missing-function-docstring

import sys
import os.path
from os import environ
import codex.b64wrap as b64wrap

INPUT_NAME = "bimbos.txt"
OUTPUT_NAME = "bimbos.txu"


def main():
    """ Main (non-interactive) script """
    code = process(sys.stdout, sys.stderr, sys.argv[1:])
    if code is None:
        print(f"""Usage:

python {__file__} [--show]

Copies {my_input()} into {my_output()}
""")
    sys.exit(code if code else 0)

def my_input(local_name):
    if "HOME" not in environ:
        environ["HOME"] = environ["USERPROFILE"]
    fname = os.path.join(environ["HOME"], local_name)
    return fname

def my_output():
    astr = sys.argv[0]
    if not astr.endswith(".py"):
        return OUTPUT_NAME
    return astr[:-len(".py")] + ".txu"

def process(out, err, args):
    assert err
    param = args
    opt = ""
    if param:
        opt = param[0]
        del param[0]
    if param:
        return None
    if opt == "--show":
        outname = OUTPUT_NAME + ".1"
        with open(outname, "wb") as fdout:
            code = dump_encoded(fdout, my_output())
        return code
    assert not opt
    rewrite_bimbos(my_input(INPUT_NAME), my_output(), os.path.isfile(my_output()))
    return 0

def dump_encoded(out, input_path) -> int:
    txt = b64wrap.Textual()
    txt.load(input_path)
    txt.decode()
    # Write binary content as ISO-8859-1 (latin-1):
    out.write(txt.string().encode(txt.get_encoding()))
    return 0

def rewrite_bimbos(input_path, output_path, exists:bool):
    txt = b64wrap.Textual()
    print(
        "rewrite():" if exists else "write():",
        input_path, "; output:", output_path,
    )
    txt.load(input_path)
    txt.encode()
    astr = txt.string()
    with open(output_path, "wb") as fdout:
        fdout.write(astr.encode("ascii"))
    return True


# Main script
if __name__ == "__main__":
    main()
