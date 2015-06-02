import requests


class GithubClient(object):
    def __init__(self, auth_token, github_base_url):
        self.auth_token = auth_token
        self.github_base_url = github_base_url

    def get_owners_team(self, org_name, team_name):
        owners_team = None
        url = '%s/orgs/%s/teams' % (self.github_base_url, org_name)
        for team in self.traverse_pagination(url):
            if team.get('name') == team_name:
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

    def get_user(self, username):
        result = self.get("%s/users/%s" % (self.github_base_url, username))
        if result.status_code == 404:
            return None
        return result.json()

    def get_key(self, username):
        result = self.get("%s/users/%s/keys" % ( self.github_base_url, username))
        if result.status_code == 404:
            raise StopIteration
        for i in result.json():
            yield i['key'], i['id']

def yield_org_keys(auth_token, github_base_url, org_name):
    client = GithubClient(auth_token, github_base_url)
    url = "%s/orgs/%s/members" % (github_base_url, org_name)
    for member in client.traverse_pagination(url):
        for key, id in client.get_key(member['login']):
            yield key, id, member['login']

def get_members(auth_token, github_base_url, org_name, team_name='Owners'):
    client = GithubClient(auth_token, github_base_url)
    url = "%s/teams/%d/members" % (
        github_base_url, client.get_owners_team(org_name, team_name).get('id'))
    return (m['login'] for m in client.traverse_pagination(url))
