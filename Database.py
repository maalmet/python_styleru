import json
import requests

api_key = 'db9b2583e7f3db9cdb729815cb367753'

films = []
i = 0

while len(films) < 1000:
    response = requests.get("https://api.themoviedb.org/3/movie/{id_f}?api_key={api_key}&language=en".format(api_key=api_key, id_f=i))
    if "status_code" not in response.text:
        films.append(json.loads(response.text))
    i += 1

f = open("films.json", "w")
json.dump(films, f)
f.close()
