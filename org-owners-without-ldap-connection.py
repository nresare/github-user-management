import sys
import requests
import ldap

GITHUB_BASE_URL = 'https://api.github.com'

ORG_NAME = 'spotify'

LDAP_URL = 'ldap://ldap-lon.spotify.net'
LDAP_BASE = 'cn=users,dc=carmen,dc=int,dc=sto,dc=spotify,dc=net'


class GithubClient(object):
    def __init__(self, auth_token):
        self.auth_token = auth_token

    def get_owners_team(self, org_name):
        owners_team = None
        url = '%s/orgs/%s/teams' % (GITHUB_BASE_URL, org_name)
        for team in self.traverse_pagination(url):
            if team.get('name') == 'Owners':
                owners_team = team
        if not owners_team:
            raise Exception('Failed to find owners team in org ' + org_name)
        return owners_team

    def traverse_pagination(self, url):
        while url:
            response = self.get(url)
            for item in response.json():
                yield item
            link = response.links.get('next')
            url = link['url'] if link else None

    def get(self, url):
        return requests.get(url, headers={
            'Authorization': 'token ' + self.auth_token})


class LdapClient(object):
    def __init__(self, ldap_url):
        self.ldap_url = ldap_url

    def __enter__(self):
        self.conn = ldap.initialize(self.ldap_url)
        return self

    def __exit__(self, *ignored):
        self.conn.unbind_s()

    def user_from_github_login(self, github_login):
        result = self.conn.search_s(
            LDAP_BASE, ldap.SCOPE_ONELEVEL,
            '(githubcomAccount=%s)' % github_login, ('uid',))
        if not result:
            return None
        return result[0][1]['uid'][0]


def get_members(auth_token):
    client = GithubClient(auth_token)
    url = "%s/teams/%d/members" % (
        GITHUB_BASE_URL, client.get_owners_team(ORG_NAME).get('id'))
    return (m['login'] for m in client.traverse_pagination(url))


def print_email_if_available(github_members):
    with LdapClient(LDAP_URL) as lc:
        for user in github_members:
            ldap_user = lc.user_from_github_login(user)
            if ldap_user:
                print ("Found email %s@spotify.com for user %s"
                       % (ldap_user, user))
            else:
                print "No email found for " + user


if __name__ == '__main__':
    print_email_if_available(get_members(sys.argv[1]))