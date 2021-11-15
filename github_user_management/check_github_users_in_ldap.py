# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016 Noa Resare
import collections

from clients import ldap_client
from clients import github_client


def print_dict_keys_per_value(d, exclude, check_existence_for_these):
    by_value = collections.defaultdict(list)
    for k in d:
        by_value[d[k]].append(k)
    printed_categories = []
    for v in sorted(by_value.keys()):
        if v in exclude:
            continue
        print("%s (%i)" % (v, len(by_value[v])))
        printed_categories.append(v)
        for k in sorted(by_value[v]):
            print(" " + k)
    for cat in check_existence_for_these:
        if cat not in printed_categories:
            print("Good news, category %s is empty!" % cat)


def check_github_usernames(github_token, ldap_url, ldap_base, github_url, org, remove_nonemployee, remove_nonmatching):
    gc = github_client.GithubClient(github_token, github_url)

    members = dict(
        map(lambda x: (x.lower(), "only_in_github"), gc.get_members(org))
    )

    with ldap_client.LdapClient(ldap_url, ldap_base) as lc:
        for user, shell, github_user in lc.get_github_users():
            github_user = github_user.lower().decode('UTF-8')
            if shell.decode('UTF-8') == '/dev/null':
                if github_user in members and members[github_user] == 'only_in_github':
                    members[github_user] = 'github_user_that_quit'
                    if remove_nonemployee:
                        gc.remove_member(org, github_user)
                continue
            if github_user not in members:
                members[github_user] = 'to_add_to_github'
            else:
                members[github_user] = 'matching'
                # print "matching %s@spotify.com" % user

        if remove_nonmatching:
            for non_matching_member in [m for m in members if members[m] == 'only_in_github']:
                gc.remove_member(org, non_matching_member)

    print_dict_keys_per_value(
        members, ("matching", "to_add_to_github"),
        ("only_in_github", "github_user_that_quit")
    )
