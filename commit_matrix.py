#!/usr/bin/env python
# -*- coding: utf-8 -*-

def create_commit_matrix():
    from gitlog_as_json import dump
    import functools

    revisions=dump()
    commit_hashes=[revision['commit'] for revision in revisions]

    files=list(functools.reduce(lambda acc,cmt: acc.union(cmt['files']), revisions,set()))

    commit_mtrx = {}
    # initialize the matrix(file, commit). its elements are zero.
    for f in files:
        commit_mtrx.update([(f, [0 for i in range(len(commit_hashes))])])

    for commit_index in range(len(revisions)):
        commit = revisions[commit_index]
        for f in commit['files']:
            commit_mtrx[f][commit_index]=1

    return commit_mtrx
