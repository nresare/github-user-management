#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2016 Lynn Root

import click

from clients import github_client
import add_ldap_users_to_employees as add_ldap
import check_github_users_in_ldap as check_github
import get_keys_for_org as get_keys
import github_details_for_users as github_details
import org_owners_without_ldap_connection as org_owners
import print_audit_log as print_audit


#####
# Argument Parameters
#####
gh_token = click.argument("gh-token", type=click.STRING)
gh_audit_log = click.argument("gh-audit-log", type=click.Path(exists=True),
                              default="audit.json")
gh_user_list = click.argument("users", type=click.Path(exists=True),
                              default="users_to_remove_from_org.txt")

#####
# Option Parameters
#####

gh_url = click.option("--gh-url", "-g", type=click.STRING,
                      default="https://api.github.com")
gh_org = click.option("--gh-org", "-o", default="spotify", type=click.STRING)
ldap_url = click.option("--ldap-url", "-l", type=click.STRING,
                        default="ldap://ldap-lon.spotify.net")
ldap_base = click.option("--ldap-base", "-b", type=click.STRING,
                         default=("cn=users,dc=carmen,dc=int,dc=sto,"
                                  "dc=spotify,dc=net"))
domain = click.option("--domain", "-d", type=click.STRING,
                      default="spotify.com")
remove_nonemployee = click.option("--remove-nonemployee", "-r", type=click.BOOL,
                                  default=False, is_flag=True)
remove_nonmatching = click.option("--remove-nonmatching", "-r", type=click.BOOL,
                                  default=False, is_flag=True)



def apply_params(click_objects):
    def wrapper(func):
        for obj in click_objects:
            obj(func)
        return func
    return wrapper


@click.group()
def main():
    """Manage members of a GitHub organization"""
    # needed to collect commands below


@main.command(help="Check GitHub usernames from LDAP")
@apply_params([gh_token, ldap_url, ldap_base, gh_url])
def add_ldap_users_to_employees(gh_token, ldap_url, ldap_base, gh_url):
    # Doesn't look like this actually adds
    add_ldap.check_github_usernames(gh_token, ldap_url, ldap_base, gh_url)


@main.command(help="Check GitHub users in LDAP")
@apply_params([gh_token, ldap_url, ldap_base, gh_url, gh_org, remove_nonemployee, remove_nonmatching])
def check_github_users_in_ldap(gh_token, ldap_url, ldap_base, gh_url, gh_org, remove_nonemployee, remove_nonmatching):
    check_github.check_github_usernames(
        gh_token, ldap_url, ldap_base, gh_url, gh_org, remove_nonemployee, remove_nonmatching
    )


@main.command(help="Get keys for org")
@apply_params([gh_token, gh_url, gh_org])
def get_keys_for_org(gh_token, gh_url, gh_org):
    get_keys.main(gh_token, gh_url, gh_org)


@main.command(help="Details for given users")
@apply_params([gh_user_list, gh_token, gh_url])
def github_details_for_users(users, gh_token, gh_url):
    github_details.print_details_for_users(users, gh_token, gh_url)


@main.command(help="Org owners without a connection in LDAP")
@apply_params([gh_token, gh_org, ldap_url, ldap_base, domain])
def org_owners_without_ldap_connection(gh_token, gh_org, ldap_url, ldap_base,
                                       domain):
    gh_client = github_client.GithubClient(gh_token)
    gh_members = gh_client.get_members(gh_org, "admin")
    org_owners.print_email_if_available(
        gh_members, ldap_url, ldap_base, domain
    )


@main.command(help="Print given audit log")
@apply_params([gh_audit_log])
def print_audit_log(gh_audit_log):
    print_audit.print_sorted(gh_audit_log)
