import aiohttp
import requests
import brotli
from player_exists import getPlayers

#TODO: Change this method to async and use aiohttp
def getPlayerId(nickname):
    session = requests.session()
    headers = { 'Accept-Encoding': 'br, gzip, deflate' }

    response = session.get(f'https://api.faceit.com/core/v1/nicknames/{nickname}', headers = headers)
    if response.status_code != 200:
        return None

    if response.headers.get('Content-Encoding') == 'br':
        response_json = response.json()
        return response_json['payload']['guid']

    response_json = response.json()    
    return response_json['payload']['guid']

    # async with aiohttp.ClientSession() as session:
    #     headers = {'Accept-Encodig': 'gzip, deflate, br'}
    #     async with session.get(f'https://api.faceit.com/core/v1/nicknames/Thorshi', headers=headers, compress = False) as response:
    #         if response.status != 200:
    #            return None
    #         if response.headers['Content-Encoding'] == 'gzip' or response.headers['Content-Encoding'] == 'br':
    #             try:
    #                 return await response.content.read()
    #             except:
    #                 print("Failed to read")
    #             try:
    #                 return await response.read()
    #             except:
    #                 print("Failed to read again")
    #             try:
    #                 return await response.json()
    #             except:
    #                 print("Failed json")

    #             return "test"

async def getWins(player1, player2, xGames):
    inSameLobby = 0
    playerOneCount = 0
    playerTwoCount = 0

    user_id = getPlayerId(player1)

    if(user_id == None):
        return f'Found no user with nickname: {player1}'

    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.faceit.com/stats/v1/stats/time/users/{user_id}/games/csgo?page=0&size={xGames}') as matches_response:
            if matches_response.status != 200:
                return "Could not fetch matches"
            else:
                json_response_matches = await matches_response.json()

                for match in json_response_matches:
                    match_id = match.get('matchId')

                    async with session.get(f'https://api.faceit.com/stats/v1/stats/matches/{match_id}') as stats_response:
                        if stats_response.status != 200:
                            return "Could not fetch stats"
                        else:
                            json_response_stats = await stats_response.json()
                            stats = next(iter(json_response_stats or []), None)

                            if stats == None:
                                return "Found no stats"

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

            if inSameLobby == 0:
                return f'You have played together {inSameLobby} time(s) in your {xGames} latest games.' 
            else:       
                return f'You have played together {inSameLobby} time(s) in your {xGames} latest games.\n{player1} had most kills in {playerOneCount} matches\n{player2} had most kills in {playerTwoCount} matches'