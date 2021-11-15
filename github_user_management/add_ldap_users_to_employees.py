# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016 Noa Resare
from clients import ldap_client
from clients import github_client


def check_github_usernames(github_token, ldap_url, ldap_base, github_url):
    gc = github_client.GithubClient(github_token, github_url)
    with ldap_client.LdapClient(ldap_url, ldap_base) as lc:
        for user, shell, github_user in lc.get_github_users():
            if shell == '/dev/null':
                # skip users with null shell, as they have quit spotify
                continue
            if not gc.get_user(github_user):
                print ("ldap user %s doesn't have a valid github user: %s"
                       % (user, github_user))
            else:
                print (github_user)
