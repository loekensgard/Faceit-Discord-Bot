def getPlayers(teamOne, teamTwo, playerOne, playerTwo):
    playersTeamOne = teamOne.get('players', [])
    playersTeamTwo = teamTwo.get('players', [])

    outPlayerOne = next((p for p in playersTeamOne if p.get('nickname') == playerOne), None)
    if(outPlayerOne == None):
        outPlayerOne = next((p for p in playersTeamTwo if p.get('nickname') == playerOne), None)

    outPlayerTwo = next((p for p in playersTeamOne if p.get('nickname') == playerTwo), None)
    if(outPlayerTwo == None):
        outPlayerTwo = next((p for p in playersTeamTwo if p.get('nickname') == playerTwo), None)

    return outPlayerOne,outPlayerTwo