import sys
from github_user_management import ldap_client
from github_user_management import github_client

ORG_NAME = 'spotify'
LDAP_URL = 'ldap://ldap-lon.spotify.net'
GITHUB_BASE_URL = 'https://api.github.com'


def print_email_if_available(github_members):
    missing_ldap_mappings = []
    users = []
    with ldap_client.LdapClient(LDAP_URL) as lc:
        for user in github_members:
            ldap_user = lc.user_from_github_login(user)
            if ldap_user:
                users.append(ldap_user + "@spotify.com")

                #print ("Found email %s@spotify.com for user %s"
                #       % (ldap_user, user))
            else:
                missing_ldap_mappings.append(user)

    print "there are %d users" % len(users)
    print ", ".join(users)

    if missing_ldap_mappings:
        print "\nDrop these users from the team (they lack LDAP mapping)"
        for user in missing_ldap_mappings:
            print user
    else:
        print "\nNo users lacking LDAP mapping. Yay!"

if __name__ == '__main__':
    print_email_if_available(
        github_client.GithubClient(sys.argv[1]).get_members(ORG_NAME, "admin"))
