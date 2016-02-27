#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess, json, re

def _fetch_partial_commits():
    dump =subprocess.check_output( ['git', 'log', '--pretty=format:{%n  \"commit\": \"%H\",%n  \"author\": \"%an <%ae>\",%n  \"date\": \"%ad\",%n  \"message\": \"%f\"%n},'] ).decode('UTF-8')
    return json.loads("[" + dump[:-1] + "]")

def _fetch_updated_files_per_revision():
    dump =subprocess.check_output( ['git', '--no-pager', 'log', '--name-only', '--format=\'%H', '--pretty=format:'] ).decode('UTF-8')
    chunk=[]
    for x in re.split('\n\n', dump):
        chunk.append([xx for xx in re.split('\n', x) if len(xx)!=0])
    return chunk

def _merge(j, f):
    return dict([('author', j['author']), ('message', j['message']), ('commit', j['commit']),('date', j['date']),('files', f)])

def dump():
    return list(map(_merge, _fetch_partial_commits(), _fetch_updated_files_per_revision()))
