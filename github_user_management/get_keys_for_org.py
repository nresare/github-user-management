# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016 Noa Resare
import sys

from clients import github_client


GITHUB_BASE_URL = 'https://api.github.com'


def main(github_token):
    for key, id, member in github_client.yield_org_keys(
            github_token, GITHUB_BASE_URL, 'spotify'):
        with open("keys/%s-%s" % (member, id), 'w') as f:
            f.write(key)
            print member


if __name__ == '__main__':
    main(sys.argv[1])
