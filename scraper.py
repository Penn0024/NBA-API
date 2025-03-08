import requests
from bs4 import BeautifulSoup

def fetch_html(url):
    """
    Fetch HTML content from the given URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"error": f"Other error occurred: {err}"}

def parse_nba_scores(html_content):
    """
    Parse the HTML content to extract NBA scores.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    games = soup.find_all("div", class_="game_summary expanded nohover")
    nba_scores = []

    for game in games:
        teams = game.find_all("a")
        scores = game.find_all("td", class_="right")

        if teams and scores and len(teams) > 2 and len(scores) > 1:
            team1 = teams[0].text
            team2 = teams[2].text
            score1 = scores[0].text.strip()
            score2 = scores[1].text.strip()

            # Ensure that the score is a number and not the word "Final"
            if score2 == "Final":
                score2 = scores[2].text.strip() if len(scores) > 2 else "N/A"

            nba_scores.append({
                "team1": team1,
                "score1": score1,
                "team2": team2,
                "score2": score2
            })

    return nba_scores

def get_nba_scores():
    """
    Main function to get NBA scores.
    """
    url = "https://www.basketball-reference.com/boxscores/"
    html_content = fetch_html(url)
    
    if isinstance(html_content, dict) and "error" in html_content:
        return html_content
    
    nba_scores = parse_nba_scores(html_content)
    return nba_scores

if __name__ == "__main__":
    print(get_nba_scores())