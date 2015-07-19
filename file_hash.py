#!/usr/bin/env python

# file_hash.py
# desc: generate file hash signature

import sys, os
import hashlib

def get_hash(filename):
    """prints a hex hash signature of the file passed in as arg"""
    try:
        file2hash = open(filename, 'r')
        filecontents2hash = file2hash.read()
        hashobject = hashlib.md5(filecontents2hash)
        file_hashsig = hashobject.hexdigest()
        print 'file= ' + filename + ' hash signature= ' + file_hashsig
    except Exception as err:
        print 'file_hash.py: ' + str(err)
    finally:
        if 'f' in locals():
            f.close()

def main():
    # Check args
    if len(sys.argv) != 2:
        print 'usage: file_hash filename'
        sys.exit(1)
    filename = sys.argv[1]

    get_hash(filename)

if __name__ == '__main__':
    main()

