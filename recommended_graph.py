#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jubatus_handler import recommend

def create_links(recommended):
    sorted_filenames=sorted(recommended.keys())

    def create_link(name):
        def get_index_by_name(name):
            return sorted_filenames.index(name)

        idx=get_index_by_name(name)
        related_indices=[get_index_by_name(n) for n in recommended[name] if (n in sorted_filenames)]
        return [{'source': idx, 'target': i, 'value': 1} for i in related_indices if i > idx]

    return [create_link(n) for n in sorted_filenames]

recommended = recommend()
a=create_links(recommended)
sorted_filenames = sorted(recommended.keys())

import json
with open('hoge.json', 'w') as f:
    json.dump({'nodes': [{'name': name, 'group': 1} for name in sorted_filenames],
    'links': [e for aa in a for e in aa]}, f,indent=2)
