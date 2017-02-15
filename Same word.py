import json

word = input("Enter word: ")
with open('films.json', encoding='utf-8') as data_file:
    data = json.load(data_file)

for film in data:
    if word.lower() in film["original_title"].lower():
        print(film["original_title"])
