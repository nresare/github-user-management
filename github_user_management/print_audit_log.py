# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016 Noa Resare
import json
import pprint


def print_sorted(json_input):
    with open(json_input, 'rb') as f:
        pprint.pprint(json.load(f))
