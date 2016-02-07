#!/usr/bin/env python
import subprocess
import json
import re

def partial_commit_json():
    dump =subprocess.check_output( ['git', 'log', '--pretty=format:{%n  \"commit\": \"%H\",%n  \"author\": \"%an <%ae>\",%n  \"date\": \"%ad\",%n  \"message\": \"%f\"%n},'] ).decode('UTF-8')
    return json.loads("[" + dump[:-1] + "]")

def update_files_per_revision():
    dump =subprocess.check_output( ['git', '--no-pager', 'log', '--name-only', '--format=\'%H', '--pretty=format:'] ).decode('UTF-8')
    chunk=[]
    for x in re.split('\n\n', dump):
        chunk.append([xx for xx in re.split('\n', x) if len(xx)!=0])
    return chunk

def merge(j, f):
    print(j)
    return dict([('author', j['author']), ('message', j['message']), ('commit', j['commit']),('date', j['date']),('files', f)])

for revision in map(merge, partial_commit_json(), update_files_per_revision()):
    print(revision)
