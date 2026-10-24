# Sports Tournament Ranking System

def create_team():
    return {
        "played": 0,
        "won": 0,
        "drawn": 0,
        "lost": 0,
        "goals_for": 0,
        "goals_against": 0,
        "points": 0
    }


def record_match(teams, team1, team2, score1, score2):
    # Update matches played and goals
    teams[team1]["played"] += 1
    teams[team2]["played"] += 1

    teams[team1]["goals_for"] += score1
    teams[team1]["goals_against"] += score2

    teams[team2]["goals_for"] += score2
    teams[team2]["goals_against"] += score1

    # Determine match result and award points
    if score1 > score2:
        teams[team1]["won"] += 1
        teams[team2]["lost"] += 1
        teams[team1]["points"] += 3

    elif score2 > score1:
        teams[team2]["won"] += 1
        teams[team1]["lost"] += 1
        teams[team2]["points"] += 3

    else:
        teams[team1]["drawn"] += 1
        teams[team2]["drawn"] += 1
        teams[team1]["points"] += 1
        teams[team2]["points"] += 1


def goal_difference(team):
    return team["goals_for"] - team["goals_against"]


def display_rankings(teams):
    # Sort by points, goal difference, goals scored,
    # then alphabetical order as the final tie-breaker.
    rankings = sorted(
        teams.items(),
        key=lambda item: (
            -item[1]["points"],
            -goal_difference(item[1]),
            -item[1]["goals_for"],
            item[0].lower()
        )
    )

    print("\n" + "=" * 94)
    print("                    FINAL TOURNAMENT RANKINGS")
    print("=" * 94)

    print(
        f"{'Rank':<6}{'Team':<18}{'P':>5}{'W':>5}"
        f"{'D':>5}{'L':>5}{'GF':>6}{'GA':>6}"
        f"{'GD':>7}{'Points':>9}"
    )
    print("-" * 94)

    for rank, (name, stats) in enumerate(rankings, start=1):
        gd = goal_difference(stats)

        print(
            f"{rank:<6}{name:<18}{stats['played']:>5}"
            f"{stats['won']:>5}{stats['drawn']:>5}"
            f"{stats['lost']:>5}{stats['goals_for']:>6}"
            f"{stats['goals_against']:>6}{gd:>7}"
            f"{stats['points']:>9}"
        )

    print("=" * 94)

    print("\nCompetition Policy:")
    print("Win = 3 points | Draw = 1 point | Loss = 0 points")
    print("Tie-breakers: Points > Goal Difference > Goals Scored")
    print("Final tie-breaker: Alphabetical order")


def main():
    print("=" * 60)
    print("       SPORTS TOURNAMENT RANKING SYSTEM")
    print("=" * 60)

    try:
        number_of_teams = int(input("Enter number of teams: "))

        if number_of_teams < 2:
            print("At least two teams are required.")
            return

        teams = {}

        # Register teams
        for i in range(number_of_teams):
            name = input(f"Enter team {i + 1} name: ").strip()

            if not name:
                print("Team name cannot be empty.")
                return

            if name.lower() in (team.lower() for team in teams):
                print("Duplicate team names are not allowed.")
                return

            teams[name] = create_team()

        number_of_matches = int(input("Enter number of matches: "))

        if number_of_matches < 0:
            print("Number of matches cannot be negative.")
            return

        matches = set()

        # Enter match results
        for i in range(number_of_matches):
            print(f"\nMatch {i + 1}")
            team1 = input("Enter first team: ").strip()
            team2 = input("Enter second team: ").strip()

            # Match names are matched without case sensitivity
            team_lookup = {name.lower(): name for name in teams}

            if team1.lower() not in team_lookup or team2.lower() not in team_lookup:
                print("Error: Both teams must be registered.")
                return

            team1 = team_lookup[team1.lower()]
            team2 = team_lookup[team2.lower()]

            if team1 == team2:
                print("A team cannot play against itself.")
                return

            # Prevent duplicate matches in this example league
            match_key = frozenset((team1, team2))
            if match_key in matches:
                print("This match has already been entered.")
                return

            score1 = int(input(f"Goals scored by {team1}: "))
            score2 = int(input(f"Goals scored by {team2}: "))

            if score1 < 0 or score2 < 0:
                print("Scores cannot be negative.")
                return

            matches.add(match_key)
            record_match(teams, team1, team2, score1, score2)

        display_rankings(teams)

    except ValueError:
        print("Invalid input. Enter valid numbers for matches and scores.")


if __name__ == "__main__":
    main()
