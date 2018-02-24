
import os
from teamcowpy import teamcowpy


def test_multiple_games(token=None, team=None):


    return False


def test_multiple_teams(user,token):

    teams = [t for t in user.getTeams(token=token) if not t['meta']['isHiddenByUser']]
    print teams
    for tm in teams:
        print tm['name']
    return False

if __name__ == '__main__':
    API_KEYS = {
        "public": os.getenv('tc_api_public'),
        "private": os.getenv('tc_api_private')
    }

    tc = teamcowpy.Auth(keys=API_KEYS)
    token = tc.get_user_token(data={"username": os.getenv('tc_username'), "password": os.getenv('tc_password')})

    user = teamcowpy.User(keys=API_KEYS)
    test_multiple_teams(user=user, token=token)

