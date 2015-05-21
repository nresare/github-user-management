import sys
from github_user_management import ldap_client
from github_user_management import github_client

ORG_NAME = 'spotify'
LDAP_URL = 'ldap://ldap-lon.spotify.net'
GITHUB_BASE_URL = 'https://api.github.com'


def print_email_if_available(github_members):
    with ldap_client.LdapClient(LDAP_URL) as lc:
        for user in github_members:
            ldap_user = lc.user_from_github_login(user)
            if ldap_user:
                print ("Found email %s@spotify.com for user %s"
                       % (ldap_user, user))
            else:
                print "No email found for " + user

if __name__ == '__main__':
    print_email_if_available(github_client.get_members(
        sys.argv[1], GITHUB_BASE_URL, ORG_NAME))
