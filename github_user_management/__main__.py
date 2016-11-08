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


@click.group()
def main():
    """Manage members of a GitHub organization"""
    # needed to collect commands below


@main.command(help="Check GitHub usernames from LDAP")
@click.argument("gh-token", type=click.STRING)
def add_ldap_users_to_employees(gh_token):
    # Doesn't look like this actually adds
    add_ldap.check_github_usernames(gh_token)


@main.command(help="Check GitHub users in LDAP")
@click.argument("gh-token", type=click.STRING)
def check_github_users_in_ldap(gh_token):
    check_github.check_github_usernames(gh_token)


@main.command(help="Get keys for org")
@click.argument("gh-token", type=click.STRING)
def get_keys_for_org(gh_token):
    get_keys.main(gh_token)


@main.command(help="Details for given users")
@click.argument("users", type=click.Path(exists=True),
                default="users_to_remove_from_org.txt")
@click.argument("gh-token", type=click.STRING)
def github_details_for_users(users, gh_token):
    github_details.print_details_for_users(users, gh_token)


@main.command(help="Org owners without a connection in LDAP")
@click.argument("gh-token", type=click.STRING)
@click.option("--org", "-o", default="spotify", type=click.STRING)
def org_owners_without_ldap_connection(gh_token, org):
    gh_client = github_client.GithubClient(gh_token)
    gh_members = gh_client.get_members(org, "admin")
    org_owners.print_email_if_available(gh_members)


@main.command(help="Print given audit log")
@click.argument("audit-log", type=click.Path(exists=True),
                default="audit.json")
def print_audit_log(audit_log):
    print_audit.print_sorted(audit_log)
