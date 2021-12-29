from typing import Optional

import requests

import exceptions

SLEEPER_BASE_API_URL = 'https://api.sleeper.app/v1'
SLEEPER_BASE_API_LEAGUE_URL = f'{SLEEPER_BASE_API_URL}/league'


class SleeperClient(object):

    def _request(self, path: str, league_id: Optional[str]):
        full_path = f'{SLEEPER_BASE_API_LEAGUE_URL}/{league_id}/{path}' if league_id else f'{SLEEPER_BASE_API_URL}/{path}'

        r = requests.get(full_path)

        if r.status_code == 400:
            raise exceptions.SleeperBadRequest()
        if r.status_code != 200:
            raise exceptions.SleeperError()

        return r.json()
