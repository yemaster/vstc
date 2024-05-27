import json
problems = []
fileData = []
with open("a.txt", "r", encoding="utf-8") as f:
    fileData = f.read().split("\n")
problems = [i.split("\t") for i in fileData if len(i)>1]
problemInfo = {}
problemInfo["title"] = "2024中国近代史纲要机考题库"
problemInfo["test"] = [0, 12, 32, 16, 8]
problemInfo["score"] = [0, 1, 2, 1, 1]
problemInfo["problems"] = []

def getType(p):
    if "多" in p:
        return 2
    if "单" in p:
        return 1
    if "填" in p:
        return 3
    if "判" in p:
        return 4
    return 0

def getSingleAnswer(t):
    return "ABCDEFGHIJKLMN".index(t)

def getAnswer(i):
    tp =getType(i[1])
    if tp == 1 or tp == 4:
        return "ABCDEFGHIJKLMN".index(i[3])
    elif tp == 2:
        res = []
        for j in i[3]:
            res.append("ABCDEFGHIJKLMN".index(j))
        return res
    elif tp == 3:
        return i[8]


for i in problems:
    print(i)
    problemInfo["problems"].append({
        "content": f"{i[2]}\n来源:{i[0]},难度:{i[5]}",
        "choices": i[8:8+int(i[7])],
        "type": getType(i[1]),
        "answer": getAnswer(i)
    })

print(problemInfo)
with open("2024jdsgy.json", "w", encoding="utf-8") as f:
    json.dump(problemInfo, f)