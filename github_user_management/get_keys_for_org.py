# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016 Noa Resare
from clients import github_client


def main(github_token, github_url, org):
    for key, id, member in github_client.yield_org_keys(
            github_token, github_url, org):
        with open("keys/%s-%s" % (member, id), 'w') as f:
            f.write(key)
            print member
