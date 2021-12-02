import requests

def get_random_quote():
    response = requests.get("http://api.quotable.io/random")
    json_data = response.json()
    data = json_data

    quote = (data['content']) + " - " + (data['author'])
    print(quote)
    return quote

