#!/usr/bin/env python2

import glob
import sys
import re
import os
import os.path
from pprint import pprint
import getopt

def help(xcode=0):
    print("""{name}:

{bname} [-s <re>] [-S] [-X] [-P] [-f <format>] [-y <filenames>] [-x <sep>] [-z <num>] [-Z <num>]

-s <re>       split filenames on regex (groups will be saved in terms)
-S            same as -s '[\s-_.]+'
-X            do not extract extensions
-x <sep>      extension separator (default = '.')
-z <num>      extension segment size limit (default = 4)
-Z <num>      extension segment count limit (default = 99999)
-P            do not extract path
-f <format>   target filename format
-y            execute the move""".format(bname=os.path.basename(sys.argv[0]), name=sys.argv[0]))
    sys.exit(xcode)


ext_size_limit=4
ext_total_limit=99999
ext_sep='.'

def extract_extension(sep, nxt):
    heuristic_extensions_re = re.compile(r'([%s][a-z0-9A-Z]{1,%d}){1,%d}$'%(ext_sep, ext_size_limit, ext_total_limit))

    def inner(f, heap):
        f = f[0]
        ext_match = heuristic_extensions_re.search(f)
        if ext_match:
            ext = ext_match.group(0)
            heap['ext'] = ext.lstrip('.')
            rest = f[:-(len(ext))]
            return nxt([rest], heap)
        else:
            heap['ext'] = ''
            return nxt([f], heap)
    return inner

def extract_path(nxt):
    def inner(f, heap):
        path, f = os.path.split(f[0])
        heap['path'] = path
        return nxt([f], heap)
    return inner

def split(sep, nxt):
    def inner(f, heap):
        return [nxt(re.split(sep, e), heap) for e in f]
    return inner

def stop(f, heap):
    return f

#transform = extract_path(extract_extensions('.', split(r'(\s|\.)+', split(r'[-_]', stop()))))

def extract_tree(t, heap, prel=[]):
    if type(t) == str:
        heap['p'+'.'.join([str(x) for x in prel])] = t
    else:
        for i in range(len(t)):
            extract_tree(t[i], heap, prel + [i+1])
try:
    optlist, args = getopt.gnu_getopt(sys.argv[1:], 's:SXPf:yz:Z:x:')
except:
    help(1)

transform = stop
xpath = True
xext = True
fmt = None
doit = False
verbose = False

for opt, optarg in reversed(optlist):
    if opt == '-X':
        xext = False
    elif opt == '-z':
        # limit of extension segment size
        ext_size_limit = int(optarg)
    elif opt == '-Z':
        # limit of total extension segments
        ext_total_limit = int(optarg)
    elif opt == '-x':
        # extension separator
        ext_sep = optarg
    elif opt == '-P':
        xpath = False
    elif opt == '-s':
        transform = split(optarg, transform)
    elif opt == '-S':
        transform = split(r'[ ._-\s]+', transform)
    elif opt == '-f':
        fmt = optarg
    elif opt == '-v':
        verbose = True
    elif opt == '-y':
        doit = True
    elif opt == '-h':
        help(0)

if transform == stop:
    transform = split(r'[\s._-]+', stop)

if xext:
    transform = extract_extension('.', transform)

if xpath:
    transform = extract_path(transform)

renames = {}

nl = False

for f in args:
    heap = {'fullname': f}
    t = extract_tree(transform([f], heap)[0], heap)

    if 'p' in heap and 'p1' not in heap:
        heap['p1'] = heap['p']

    for k,v in heap.items():
        try:
            iv = int(v)
            heap[k] = iv
        except ValueError:
            # it's not an integer so... uh... nm
            pass

    if fmt:
        try:
            newname = fmt.format(**heap)
            renames[f] = newname
        except:
            print "Error formatting %s"%(f)
            sys.exit(1)
    else:
        if nl:
            print
        nl = True
        print f
        pprint(heap)

if renames == {}:
    sys.exit(0)

if not doit:
    for k,v in renames.items():
        print 'move', k
        print '  ->', v

if len(set(renames.values())) != len(renames.values()):
    if doit:
        print "There are duplicates in your rename list!  Aborting!"
        sys.exit(1)
    else:
        print "There are duplicates in your rename list!"

if doit:
    for k,v in renames.items():
        os.rename(k, v)
