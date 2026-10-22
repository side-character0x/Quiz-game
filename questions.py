import requests
import html
class Question:
    def fetch(self,amount,difficulty):
        response=requests.get(f"https://opentdb.com/api.php?amount={amount}&type=multiple&difficulty={difficulty}")
        if response.status_code==200:
            response=response.json()
            results=response["results"]
            data=[]
            for i in results:
                question=html.unescape(i["question"])
                correct=i["correct_answer"]
                choices=i["incorrect_answers"]+[correct]
                data.append([question,choices,correct])
            return data

