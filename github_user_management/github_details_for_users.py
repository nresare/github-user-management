# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016 Noa Resare
from clients import github_client


def print_details_for_users(users_filename, token, github_url):
    gc = github_client.GithubClient(token, github_url)
    with open(users_filename) as f:
        for u in f:
            u = u.strip()
            user = gc.get_user(u)
            email = user["email"]
            if email:
                print ("Email for %s is %s" % (u, email))
            else:
                print ("no email for user " + u)
