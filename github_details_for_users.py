import sys

from github_user_management import github_client


def print_details_for_users(users_filename, token):
    gc = github_client.GithubClient(token)
    with open(users_filename) as f:
        for u in f:
            u = u.strip()
            user = gc.get_user(u)
            email = user["email"]
            if email:
                print "Email for %s is %s" % (u, email)
            else:
                print "no email for user " + u


if __name__ == '__main__':
    print_details_for_users("users_to_remove_from_org.txt", sys.argv[1])