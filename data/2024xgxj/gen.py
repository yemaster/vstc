import json

with open("raw.json", encoding="utf-8") as f:
    data = json.load(f)

prob = {
    "title": data["name"],
    "test": 40,
    "score": [0, 1, 1, 1, 1]
}

problems = []

for i in data["questions"]:
    newp = {}
    newp["content"] = i["content"]

    newp["choices"] = []
    answerList = []

    for j, k in enumerate(i["options"]):
        if k["isCorrect"]:
            answerList.append(j)
        if k["content"][0] in "ABCDEFGHIJKLMNOPQ" and k["content"][1] in ".":
            newp["choices"].append(k["content"][2:])
        else:
            newp["choices"].append(k["content"])
    
    if len(answerList) == 1:
        newp["answer"] = answerList[0]
        newp["type"] = 1
    else:
        newp["answer"] = answerList
        newp["type"] = 2
    problems.append(newp)

prob["problems"] = problems

with open("2024xgxj.json", "w", encoding="utf-8") as f:
    json.dump(prob, f)