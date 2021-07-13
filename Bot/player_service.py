def get_players(teamOne, teamTwo, playerOne, playerTwo):
    playersTeamOne = teamOne.get('players', [])
    playersTeamTwo = teamTwo.get('players', [])

    outPlayerOne = next((p for p in playersTeamOne if p.get('nickname') == playerOne), None)
    if(outPlayerOne == None):
        outPlayerOne = next((p for p in playersTeamTwo if p.get('nickname') == playerOne), None)

    outPlayerTwo = next((p for p in playersTeamOne if p.get('nickname') == playerTwo), None)
    if(outPlayerTwo == None):
        outPlayerTwo = next((p for p in playersTeamTwo if p.get('nickname') == playerTwo), None)

    return outPlayerOne,outPlayerTwo

def get_player_stats(property, player):
    player_one_count = 0
    player_two_count = 0
    same_amount = 0

    playerOneTotalKills = player[0].get('player_stats').get(property)
    playerTwoTotalKills = player[1].get('player_stats').get(property)

    if playerOneTotalKills > playerTwoTotalKills:
        player_one_count += 1
    elif playerTwoTotalKills > playerOneTotalKills:
        player_two_count += 1
    else:
        same_amount += 1
    return player_one_count,player_two_count,same_amount