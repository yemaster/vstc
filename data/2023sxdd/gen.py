import json
problems = []
fileData = []
with open("a.txt", "r", encoding="utf-8") as f:
    fileData = f.read().split("\n")
problems = [i.split("\t") for i in fileData if len(i)>1]
problemInfo = {}
problemInfo["title"] = "2023思想道德与法治无纸化考试题库"
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
        return i[6]


for i in problems:
    problemInfo["problems"].append({
        "content": f"{i[2]}\n来源:{i[0]},难度:{i[4]}",
        "choices": i[6:6+int(i[5])],
        "type": getType(i[1]),
        "answer": getAnswer(i)
    })

print(problemInfo)
with open("2023sxdd.json", "w", encoding="utf-8") as f:
    json.dump(problemInfo, f)