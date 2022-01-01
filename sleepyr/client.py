import logging
from typing import Dict, Optional

import requests

from . import exceptions

SLEEPER_BASE_API_URL = 'https://api.sleeper.app/v1'
SLEEPER_BASE_API_LEAGUE_URL = f'{SLEEPER_BASE_API_URL}/league'
SLEEPER_AVATAR_CDN_URL = 'https://sleepercdn.com/avatars'
# doubt this'll change soon but at least it'll be in one place
SPORT = 'nfl'

class SleeperClient(object):

    def __init__(self, init_players = True):
        # TODO: check for staleness
        if init_players:
            self._players = self._request('players/nfl')
        else:
            logging.warn('Not initializing players map, things will probably break!')
            self._players = {}

    def _request(self, path: str, league_id: Optional[str] = None, params: Optional[Dict[str, str]] = None):
        full_path = f'{SLEEPER_BASE_API_LEAGUE_URL}/{league_id}/{path}' if league_id else f'{SLEEPER_BASE_API_URL}/{path}'

        r = requests.get(full_path, params=params)

        if r.status_code == 400:
            logging.error(f'400 response: {r}')
            raise exceptions.SleeperBadRequest()
        if r.status_code != 200:
            logging.error(f'error response: {r}')
            raise exceptions.SleeperError()

        return r.json()

    # SPORT API

    def sport_state(self):
        return self._request(f'state/{SPORT}')

    # USER API

    def user(self, user_id: str):
        return self._request(f'user/{user_id}')

    # AVATARS API

    def avatar_url(self, avatar_id: str):
        return f'{SLEEPER_AVATAR_CDN_URL}/{avatar_id}'

    # LEAGUES API

    def user_leagues(self, user_id: str, season: int):
        return self._request(f'user/{user_id}/leagues/{SPORT}/{season}')

    def league(self, league_id: str):
        return self._request('', league_id=league_id)

    def league_rosters(self, league_id: str):
        return self._request('rosters', league_id=league_id)

    def league_users(self, league_id: str):
        return self._request('users', league_id=league_id)

    def league_matchups(self, league_id: str, week: str):
        return self._request(f'matchups/{week}', league_id=league_id)

    def league_winners_bracket(self, league_id: str):
        return self._request('winners_bracket', league_id=league_id)

    def league_losers_bracket(self, league_id: str):
        return self._request('losers_bracket', league_id=league_id)

    def league_transactions(self, league_id: str, round: str):
        return self._request(f'transactions/{round}', league_id=league_id)

    def league_traded_picks(self, league_id: str):
        return self._request('traded_picks', league_id=league_id)

    # DRAFTS API

    def user_drafts(self, user_id: str, season: int):
        return self._request(f'user/{user_id}/drafts/{SPORT}/{season}')

    def league_drafts(self, league_id: str):
        return self._request(f'drafts', league_id=league_id)

    def draft(self, draft_id: str):
        return self._request(f'draft/{draft_id}')

    def draft_picks(self, draft_id: str):
        return self._request(f'draft/{draft_id}/picks')

    def draft_traded_picks(self, draft_id: str):
        return self._request(f'draft/{draft_id}/traded_picks')

    # PLAYERS API

    def players(self):
        return self._players

    def trending_players(self, type: str, lookback_hours: int = 24, limit: int = 25):
        if type not in ['add', 'drop']:
            raise ValueError('trending type must be either "add" or "drop"')
        return self._request(f'players/{SPORT}/trending/{type}', params={'lookback_hours': lookback_hours, 'limit': limit})
