#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from jubatus.recommender import client
from jubatus.recommender import types


recommender = client.Recommender("127.0.0.1", 9199, "my_recommender")

sr = recommender.similar_row_from_id("gitlog_json_print.py", 4)
print(sr)
