import sys
from clients import ldap_client
from clients import github_client

LDAP_URL = 'ldap://ldap-lon.spotify.net'
GITHUB_BASE_URL = 'https://api.github.com'


def check_github_usernames(github_token):
    gc = github_client.GithubClient(github_token, GITHUB_BASE_URL)
    with ldap_client.LdapClient(LDAP_URL) as lc:
        for user, shell, github_user in lc.get_github_users():
            if shell == '/dev/null':
                # skip users with null shell, as they have quit spotify
                continue
            if not gc.get_user(github_user):
                print ("ldap user %s doesn't have a valid github user: %s"
                       % (user, github_user))
            else:
                print github_user


if __name__ == '__main__':
    check_github_usernames(sys.argv[1])
