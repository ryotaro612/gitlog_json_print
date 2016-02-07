#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess, json, re, csv, sys
from jubatus.recommender import client
from jubatus.recommender import types
from jubatus.common import Datum


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
    return dict([('author', j['author']), ('message', j['message']), ('commit', j['commit']),('date', j['date']),('files', f)])

def get_log_as_json():
    return list(map(merge, partial_commit_json(), update_files_per_revision()))

# print(get_log_as_json())

log_as_json = get_log_as_json()

commits=[]
for revision in log_as_json:
    commits.append(revision['commit'])

files=set()
for f in log_as_json:
    files.update(f['files'])
files = list(files)

# print(commits)
# print(files)

log_csv={}
for f in files:
    log_csv.update([(f, [0 for x in range(len(commits))])])

# print(log_csv)


for commit_index in range(len(log_as_json)):
    commit = log_as_json[commit_index]
    for f in commit['files']:
        log_csv[f][commit_index]=1

print(log_csv)

recommender = client.Recommender("127.0.0.1", 9199, "my_recommender")

for filename,cmts in log_csv.items():
    d={}
    for i in range(len(cmts)):
        d.update([(commits[i], cmts[i])])
    recommender.update_row(filename, Datum(d))

"""
f = open('log_as.csv', 'w')
writer = csv.writer(f)

writer.writerows([['#'] + commits] + [[k] + v for k,v in log_csv.items()])
f.close()
"""
