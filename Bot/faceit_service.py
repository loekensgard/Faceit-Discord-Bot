import aiohttp
from player_exists import getPlayers
from config import settings

async def getPlayerId(nickname):
    headers = { 'Authorization': f'Bearer {settings.API_KEY}' }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f'https://open.faceit.com/data/v4/players?nickname={nickname}') as response:
            if response.status == 400:
                raise ValueError(f'Found no user with nickname: {nickname}')
            elif response.status != 200:
                raise ValueError('Response code is not 200')
            response_json = await response.json()
            return response_json['player_id']

async def getWins(player1, player2, xGames, property):
    if not property: raise ValueError(f'property is null')

    inSameLobby = 0
    playerOneCount = 0
    playerTwoCount = 0
    sameAmount = 0

    try:
        user_id = await getPlayerId(player1)
    except:
        raise

    if(user_id == None):
        raise ValueError(f'Found no user with nickname: {player1}')

    headers = { 'Authorization': f'Bearer {settings.API_KEY}' }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f'https://open.faceit.com/data/v4/players/{user_id}/history?game=csgo&offset=0&limit={xGames}') as matches_response:
            if matches_response.status != 200:
                raise ValueError('Could not get matches from the faceit api')
            else:
                json_response_matches = await matches_response.json()

                for match in json_response_matches.get('items'):
                    match_id = match.get('match_id')

                    async with session.get(f'https://open.faceit.com/data/v4/matches/{match_id}/stats') as stats_response:
                        if stats_response.status != 200:
                            raise ValueError(f'Could not get stats for matchid: {match_id}')
                        else:
                            json_response_stats = await stats_response.json()
                            teams = json_response_stats.get('rounds')[0].get('teams')

                            player = getPlayers(teams[0], teams[1], player1, player2)

                            if player[0] != None and player[1] != None:
                                inSameLobby += 1
                                playerOneTotalKills = player[0].get('player_stats').get(property)
                                playerTwoTotalKills = player[1].get('player_stats').get(property)

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