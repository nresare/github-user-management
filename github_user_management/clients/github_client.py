import requests


class GithubClient(object):
    def __init__(self, auth_token, github_base_url='https://api.github.com'):
        self.auth_token = auth_token
        self.github_base_url = github_base_url

    def get_team_info(self, org_name, team_name):
        team_info = None
        url = '%s/orgs/%s/teams' % (self.github_base_url, org_name)
        for team in self.traverse_pagination(url):
            if team.get('name') == team_name:
                team_info = team
        if not team_info:
            raise Exception(
                'Failed to find team %s in org %s' % (team_name, org_name))
        return team_info

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
        result = self.get("%s/users/%s/keys" % (self.github_base_url,
                                                username))
        if result.status_code == 404:
            raise StopIteration
        for i in result.json():
            yield i['key'], i['id']

    def add_user_to_team(self, username, team_name):
        pass

    def get_members(self, org_name, role='all'):
        url = "%s/orgs/%s/members?role=%s" % (
            self.github_base_url, org_name, role)
        return (m['login'] for m in self.traverse_pagination(url))


def yield_org_keys(auth_token, github_base_url, org_name):
    client = GithubClient(auth_token, github_base_url)
    url = "%s/orgs/%s/members" % (github_base_url, org_name)
    for member in client.traverse_pagination(url):
        for key, id in client.get_key(member['login']):
            yield key, id, member['login']
