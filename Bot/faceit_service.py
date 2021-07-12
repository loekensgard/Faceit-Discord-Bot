import aiohttp
from aiohttp import ClientResponse

import gzip
import json

from player_exists import getPlayers

async def getPlayerId(nickname):
    async with aiohttp.ClientSession(auto_decompress=False) as session:
        async with session.get(f'https://api.faceit.com/core/v1/nicknames/{nickname}') as response:
            response: ClientResponse
            if response.status != 200:
                raise ValueError('Response code is not 200')

            if response.headers.get('x-faceit-cache') != 'true':
                # If the data is NOT cached, it's NOT compressed, just return json decode
                response_json = await response.json()
                return response_json['payload']['guid']

            decoded = gzip.decompress(await response.read())
            response_json = json.loads(decoded)
            return response_json['payload']['guid']

async def getWins(player1, player2, xGames):
    inSameLobby = 0
    playerOneCount = 0
    playerTwoCount = 0
    sameAmount = 0

    #Could probably be handeled different
    try:
        user_id = await getPlayerId(player1)
    except:
        raise

    if(user_id == None):
        raise ValueError(f'Found no user with nickname: {player1}')

    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.faceit.com/stats/v1/stats/time/users/{user_id}/games/csgo?page=0&size={xGames}') as matches_response:
            if matches_response.status != 200:
                raise ValueError('Could not get matches from the faceit api')
            else:
                json_response_matches = await matches_response.json()

                for match in json_response_matches:
                    match_id = match.get('matchId')

                    async with session.get(f'https://api.faceit.com/stats/v1/stats/matches/{match_id}') as stats_response:
                        if stats_response.status != 200:
                            raise ValueError(f'Could not get stats for matchid: {match_id}')
                        else:
                            json_response_stats = await stats_response.json()
                            stats = next(iter(json_response_stats or []), None)

                            if stats == None:
                                raise ValueError(f'Found no stats for matchid: {match_id}')

                            teams = stats.get('teams')
                            teamOne = teams[0]
                            teamTwo = teams[1]

                            player = getPlayers(teamOne, teamTwo, player1, player2)

                            if player[0] != None and player[1] != None:
                                inSameLobby += 1
                                playerOneTotalKills = player[0].get('i6')
                                playerTwoTotalKills = player[1].get('i6')

                                if playerOneTotalKills > playerTwoTotalKills:
                                    playerOneCount += 1
                                elif playerTwoTotalKills > playerOneTotalKills:
                                    playerTwoCount += 1
                                else:
                                    sameAmount += 1
            
            if inSameLobby == 0:
                return None 
            else:       
                result = dict()
                result['inSameLobby'] = inSameLobby
                result['playerOneCount'] = playerOneCount
                result['playerTwoCount'] = playerTwoCount
                result['sameAmount'] = sameAmount
                return result

# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass

class CacheError(Error):
    """Raised when faceit cache is not present"""
    pass