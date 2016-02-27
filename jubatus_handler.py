#!/usr/bin/env python
# -*- coding: utf-8 -*-

_host = "127.0.0.1"
_port = 9199
_name = "mokumoku2_recommender"

def recommend():
    from jubatus.recommender import client
    from jubatus.recommender import types
    from jubatus.common import Datum
    from commit_matrix import create_commit_matrix
    from gitlog import dump, get_files, get_commit_hashes

    json_frmt_log = dump()
    mtrx=create_commit_matrix(json_frmt_log)
    commit_hashes=get_commit_hashes(json_frmt_log)

    recommender = client.Recommender(_host, _port, _name)
    for filename,cmts in mtrx.items():
        d={}
        for i in range(len(cmts)):
            d.update([(commit_hashes[i], cmts[i])])
        recommender.update_row(filename, Datum(d))

    recommended={}

    for f in get_files(json_frmt_log):
        r = [x.id for x in recommender.similar_row_from_id(f, 4)]
        # print(r[0] + ' -> ' + ', '.join(r[1:]))
        recommended.update([(f, [x for x in r[1:]])])
                # print(relation_map)
                # [file1, file2, ll]
    return recommended
