import requests


def load_fixture_data():
    url = 'https://www.football-data.co.uk/englandm.php'
    response = requests.get(url)
    pass
