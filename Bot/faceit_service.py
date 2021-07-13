import aiohttp
from player_service import get_players, get_player_stats
from config import settings

from error_extensions import NeverInSameLobbyError
from player_stats_class import player_stats

async def get_player_id(nickname):
    headers = { 'Authorization': f'Bearer {settings.API_KEY}' }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f'https://open.faceit.com/data/v4/players?nickname={nickname}') as response:
            if response.status == 400:
                raise ValueError(f'Found no user with nickname: {nickname}')
            elif response.status != 200:
                raise ValueError('Response code is not 200')
            response_json = await response.json()
            return response_json['player_id'], response_json['avatar']

async def get_stats(player1, player2, xGames):
    in_same_lobby = 0

    try:
        user_id, avatar = await get_player_id(player1)
    except:
        raise

    result_player1 = player_stats(player1, avatar)
    result_player2 = player_stats(player2, None)

    if(user_id == None):
        raise ValueError(f'Found no user with nickname: {player1}')

    headers = { 'Authorization': f'Bearer {settings.API_KEY}' }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f'https://open.faceit.com/data/v4/players/{user_id}/history?game=csgo&offset=0&limit={xGames}&from=1468420255') as matches_response:
            if matches_response.status != 200:
                raise ValueError('Could not get matches from the faceit api')
            else:
                json_response_matches = await matches_response.json()
                matches = json_response_matches.get('items')
                for match in matches:
                    match_id = match.get('match_id')

                    async with session.get(f'https://open.faceit.com/data/v4/matches/{match_id}/stats') as stats_response:
                        if stats_response.status != 200:
                            raise ValueError(f'Could not get stats for matchid: {match_id}')
                        else:
                            json_response_stats = await stats_response.json()
                            teams = json_response_stats.get('rounds')[0].get('teams')

                            player_info = get_players(teams[0], teams[1], player1, player2)

                            if player_info[0] != None and player_info[1] != None:
                                in_same_lobby += 1
                                kills = get_player_stats('Kills', player_info)
                                deaths = get_player_stats('Deaths', player_info)
                                hs = get_player_stats('Headshots %', player_info)

                                result_player1.kills += kills[0]
                                result_player2.kills += kills[1]
                                result_player1.same_amount_kills += kills[2]

                                result_player1.deaths += deaths[0]
                                result_player2.deaths += deaths[1]
                                result_player1.same_amount_deaths += deaths[2]

                                result_player1.hs += hs[0]
                                result_player2.hs += hs[1]
                                result_player1.same_amount_hs += hs[2]
            if in_same_lobby == 0:
                raise NeverInSameLobbyError()
            else:       
                return in_same_lobby, result_player1, result_player2