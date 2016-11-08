import collections
import sys


from clients import ldap_client
from clients import github_client

LDAP_URL = 'ldap://ldap-lon.spotify.net'
GITHUB_BASE_URL = 'https://api.github.com'


def print_dict_keys_per_value(d, exclude, check_existence_for_these):
    by_value = collections.defaultdict(list)
    for k in d:
        by_value[d[k]].append(k)
    printed_categories = []
    for v in sorted(by_value.iterkeys()):
        if v in exclude:
            continue
        print v
        printed_categories.append(v)
        for k in sorted(by_value[v]):
            print " " + k
    for cat in check_existence_for_these:
        if cat not in printed_categories:
            print "Good news, category %s is empty!" % cat


def check_github_usernames(github_token):
    gc = github_client.GithubClient(github_token, GITHUB_BASE_URL)

    members = dict(
        map(lambda x: (x.lower(), "github"), gc.get_members("spotify"))
    )

    with ldap_client.LdapClient(LDAP_URL) as lc:
        for user, shell, github_user in lc.get_github_users():
            github_user = github_user.lower()
            if shell == '/dev/null':
                if github_user in members:
                    members[github_user] = 'github_user_that_quit'
                continue
            if github_user not in members:
                members[github_user] = 'to_add_to_github'
            else:
                members[github_user] = 'matching'
                # print "matching %s@spotify.com" % user

    print_dict_keys_per_value(
        members, ("matching", "to_add_to_github"),
        ("github", "github_user_that_quit")
    )


if __name__ == '__main__':
    check_github_usernames(sys.argv[1])
