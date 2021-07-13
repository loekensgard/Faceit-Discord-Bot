class player_stats:
    def __init__(self, name, avatar):
        self.avatar = avatar
        self.name = name
        self.kills = 0
        self.deaths = 0
        self.hs = 0
        self.same_amount_kills = 0
        self.same_amount_deaths = 0
        self.same_amount_hs = 0