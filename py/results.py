# report system
from datetime import datetime
import json


class Statistic:
    @staticmethod
    def save_results(acc, cpm, wpm):
        res_file = 'typing-speed-test.results.json'
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        results = [{
            date: {
                "acc": str(acc),
                "cpm": str(cpm),
                "wpm": str(wpm)
            }
        }]
        with open(res_file, 'a+'):
            json.dump(res_file, results)

    @staticmethod
    def get_results():
        res_file = 'typing-speed-test.results.json'
        res: any
        with open(res_file, 'r') as sfile:
            res = json.load(sfile)
        return res
