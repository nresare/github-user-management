A set of scripts to manage members of a github organisation.

noa@resare.com

## Installation

In a [virtualenv](https://virtualenv.pypa.io/en/stable/):

```sh
(env) $ pip install git+https://github.com/nresare/github-user-management.git
```

## Usage

You will first need to create a [GitHub token](https://github.com/settings/tokens) with "read" permissions under "admin:org".

```sh
(env) $ export GITHUB_TOKEN=YOUR_TOKEN
```

Then to start using the utility:

```sh
(env) $ ghmanage --help
Usage: ghmanage [OPTIONS] COMMAND [ARGS]...

  Manage members of a GitHub organization

Options:
  --help  Show this message and exit.

Commands:
  add_ldap_users_to_employees     Check GitHub usernames from LDAP
  check_github_users_in_ldap      Check GitHub users in LDAP
  get_keys_for_org                Get keys for org
  github_details_for_users        Details for given users
  org_owners_without_ldap_connection
                                  Org owners without a connection in LDAP
  print_audit_log                 Print given audit log
```

```sh
# for example, to find org owners without an LDAP mapping
(env) $ ghmanage org_owners_without_ldap_connection $GITHUB_TOKEN
```
