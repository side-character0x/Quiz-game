import requests
import html
import time
class Question:
    def fetch(self,amount,difficulty,category=False):
        if category:
            data=[]
            response=requests.get(f"https://opentdb.com/api.php?amount={amount}&type=multiple&difficulty={difficulty}&category={category}")
            if response.status_code==200:
                response=response.json()
                if response.get("response_code") != 0:
                    return False
                results=response["results"]
                data=[]
                for i in results:
                        question=html.unescape(i["question"])
                        correct=i["correct_answer"]
                        choices=i["incorrect_answers"]+[correct]
                        categories=i["category"]
                        data.append([question,choices,correct,categories])
                return data
            else:
                return False
            ##  Made the approach as a backup for multi-category fetch ,but currently facing some problems!!

            # if amount/len(category)>=2:
            #     base=amount//len(category)
            #     remainder=amount%len(category)
            #     question_division=[]
            #     for i in category:
            #         if remainder != 0:
            #             question_division.append(base+remainder)
            #             remainder=0
            #         else:
            #             question_division.append(base)
            #     for index,value in enumerate(question_division):
            #         response=requests.get(f"https://opentdb.com/api.php?amount={value}&type=multiple&difficulty={difficulty}&category={category[index]}")
            #         if response.status_code==200:
            #             response=response.json()
            #             results=response["results"]
            #         for i in results:
            #             question=html.unescape(i["question"])
            #             correct=i["correct_answer"]
            #             choices=i["incorrect_answers"]+[correct]
            #             categories=i["category"]
            #             data.append([question,choices,correct,categories])
            #             if len(data)==amount:
            #                 return data
            #         time.sleep(5)
            # else:
            #     while True:
            #         response=requests.get(f"https://opentdb.com/api.php?amount=50&type=multiple&difficulty={difficulty}")
            #         if response.status_code==200:
            #             response=response.json()
            #             results=response["results"]
            #             for i in results:
            #                 if i["category"] in category:
            #                     question=html.unescape(i["question"])
            #                     correct=i["correct_answer"]
            #                     choices=i["incorrect_answers"]+[correct]
            #                     categories=i["category"]
            #                     data.append([question,choices,correct,categories])
            #                     if len(data)==amount:
            #                         return data
            #             time.sleep(5)


        else:
            response=requests.get(f"https://opentdb.com/api.php?amount={amount}&type=multiple&difficulty={difficulty}")
            if response.status_code==200:
                response=response.json()
                if response.get("response_code") != 0:
                    return False
                results=response["results"]
                data=[]
                for i in results:
                    question=html.unescape(i["question"])
                    correct=i["correct_answer"]
                    choices=i["incorrect_answers"]+[correct]
                    categories=i["category"]
                    data.append([question,choices,correct,categories])
                return data
            else:
                return False
    def get_categories(self):
        url = "https://opentdb.com/api_category.php"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            category_names = [[cat["name"],cat["id"]] for cat in data["trivia_categories"]]
            return category_names
        else:
            return []


