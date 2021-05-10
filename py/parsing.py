import requests


class Parsing:
    def __init__(self, repo_url: str):
        req = requests.get(repo_url)
        self.__write_to_file(req.text)

    def __write_to_file(self, value: str):
        with open('src/sentences.txt', 'w') as code_file:
            code_file.write(value)
