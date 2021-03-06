[![Build and Deploy](https://github.com/loekensgard/Faceit-Discord-Bot/actions/workflows/deployment.yml/badge.svg?branch=main)](https://github.com/loekensgard/Faceit-Discord-Bot/actions/workflows/deployment.yml)

# Faceit-Discord-Bot

Discord bot for comparing faceit stats.

## Getting started

1. Create your own discord bot.
2. Create an .env file in the /Bot folder.
3. Add *DISCORD_TOKEN={Your token}* to the .env file
4. Install python and the requirements listed in requirements.txt.
5. Run the project from a terminal or your favorite IDE.

# Discord commands
```
!faceit <player1> <player2> <gameCount> 
```

This command will lookup all player1s matches and count all the matches where player2 was present, and then check which of them that had most kills for each match.

# Contributing

Pull requests are welcome, please discuss changes via Issues.
