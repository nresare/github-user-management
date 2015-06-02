from github_user_management import github_client

import sys

GITHUB_BASE_URL = 'https://api.github.com'

if __name__ == '__main__':
    for key, id, member in github_client.yield_org_keys(
            sys.argv[1], GITHUB_BASE_URL, 'spotify'):
        with open("keys/%s-%s" % (member, id), 'w') as f:
            f.write(key)
            print member
