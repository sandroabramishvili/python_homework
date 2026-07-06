# Football Team Managmenet System

# შექმენით კლასი FootballTeam შემდეგი ატრიბუტებით:
# team_name (string) - კლუბის სახელი
# coach (string) - მწვრთნელი
# players - მოთამაშეების სია(შექმნისას ცარიელი უნდა იყოს)

# კლასს უნდა გააჩნდეს შემდეგი მეთოდები:
# 1. მოთამაშის დამატება - მოთამაშის სახელი, პოზიცია, სათამაშო ნომერი, 
#    ასაკი და ეროვნება(დიქტის სახით უნდა დაემატოს მოთამაშეების სიაში)

# 2. მოთამაშის წაშლა - მოთამაშე უნდა წაიშალოს სიიდან სათამაშო ნომრის მიხედვით

# 3. მოთამაშის ინფორმაციის განახლება - მოთამაშე უნდა მონახოთ სათამაშო ნომრის მიხედვით
#    და უნდა დაუსეტოთ ისეთი ინფორმაცია, რომელსაც გადასცემთ ამ მეთოდს, მაგ: "goal": 1 
#    ანუ key და value უნდა იყოს გადაცემული ამავე მეთოდის გამოძახებისას!

# 4. კლუბის ინფორმაციის ჩვენება - გამოიტანეთ კლუბის სახელი, მწვრთნელის სახელი და მოთამაშეების სია

# 5. მოთამაშის ინფორმაციის ჩვენება - უნდა გამოიტანოთ ინფორმაცია მოთამაშის ნომრის მიხედვით

class FootballTeam:

    def __init__(self, team_name, coach):
        self.team_name: str = team_name
        self.coach: str = coach
        self.players: list[dict] = []

    def add_player(self, name, position, number, age, nationality):
        player = {
            "name": name,
            "position": position,
            "number": number,
            "age": age,
            "nationality": nationality
        }
        self.players.append(player)

    def remove_player(self, number):
        self.players = [player for player in self.players if player["number"] != number]

    def update_player_info(self, number, key, value):
        for player in self.players:
            if player["number"] == number:
                player[key] = value
                break
    
    def show_team_info(self):
        print(f"Team Name: {self.team_name}")
        print(f"Coach: {self.coach}")
        print("Players:")
        for player in self.players:
            print(player)

    def show_player_info(self, number):
        for player in self.players:
            if player["number"] == number:
                print(f"Player Information: {player}")
                break


football_team = FootballTeam("Real Madrid", "Jose Mourinho")
football_team.add_player("Jude Bellingham", "Midfielder", 5, 21, "England")
football_team.add_player("Vinicius Junior", "Forward", 7, 25, "Brazil")
football_team.add_player("Kylian Mbappe", "Forward", 10, 27, "France")
football_team.update_player_info(5, "age", 22)
football_team.show_team_info()
football_team.show_player_info(7)