#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess, json, re, functools

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

def get_commit_hashes(json_frmt_log):
    return [revision['commit'] for revision in json_frmt_log]

def get_files(json_frmt_log):
    return list(functools.reduce(lambda acc,e: acc.union(e['files']), json_frmt_log,set()))

def dump():
    return list(map(_merge, _fetch_partial_commits(), _fetch_updated_files_per_revision()))
