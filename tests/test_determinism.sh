#!/bin/sh
# Check that two runs of main.py write byte-identical output, that the
# output matches entry.txt in this repo, and that it passes the gate
# (UTF-8 text, 1 to 200 characters, not only white space, one line).
set -e
cd "$(dirname "$0")/.."
rm -rf /tmp/osa_a /tmp/osa_b
mkdir -p /tmp/osa_a /tmp/osa_b
MAKEFUN_OUTPUT_DIR=/tmp/osa_a python3 main.py > /tmp/osa_a.stdout
MAKEFUN_OUTPUT_DIR=/tmp/osa_b python3 main.py > /tmp/osa_b.stdout
cmp /tmp/osa_a/entry.txt /tmp/osa_b/entry.txt && echo "deterministic: identical bytes"
cmp /tmp/osa_a/entry.txt entry.txt && echo "matches entry.txt in repo"
cmp /tmp/osa_a.stdout /tmp/osa_b.stdout && echo "stdout deterministic"
python3 -c "
import os
p = '/tmp/osa_a/entry.txt'
d = open(p, 'rb').read()
t = d.decode('utf-8')
assert 1 <= len(t) <= 200, len(t)
assert t.strip(), 'only white space'
assert '\n' not in t, 'must be one line'
assert not t.endswith('\n'), 'no trailing newline'
assert (os.stat(p).st_mode & 0o777) == 0o644, oct(os.stat(p).st_mode)
print('gate ok: %d chars, %d bytes, mode 0644' % (len(t), len(d)))
print('entry:', t)
"
