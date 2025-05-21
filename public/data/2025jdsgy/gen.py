import csv
import json
problems = []
fileData = ""
with open("a.txt", "r", encoding="utf-8") as f:
    fileData = f.read() + "\n"

nowCell = ""
nowLine = []
inQuote = False

for i in fileData:
    if inQuote:
        if i == '"':
            inQuote = False
        else:
            nowCell += i
    else:
        if i == '"':
            inQuote = True
        elif i == "\t":
            if len(nowCell.strip()):
                nowLine.append(nowCell.strip())
            nowCell = ""
        elif i == "\n":
            if len(nowLine) > 5:
                nowLine.append(nowCell)
                problems.append(nowLine)
            nowLine = []
            nowCell = ""
        else:
            nowCell += i

problemInfo = {}
problemInfo["title"] = "2025中国近代史纲要-2025复核后版本 Sheet1"
problemInfo["test"] = [0, 25, 30, 0, 15]
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

cnt = 0
for i in problems:
    if (i[4]).isdigit():
        problemInfo["problems"].append({
            "content": f"{i[2]}\n来源:{i[0]}",
            "choices": i[5:5+int(i[4])],
            "type": getType(i[1]),
            "answer": getAnswer(i)
        })
    elif (i[5]).isdigit():
        problemInfo["problems"].append({
            "content": f"{i[2]}\n来源:{i[0]},难度:{i[4]}",
            "choices": i[6:6+int(i[5])],
            "type": getType(i[1]),
            "answer": getAnswer(i)
        })
    else:        
        problemInfo["problems"].append({
            "content": f"{i[2]}\n来源:{i[0]},难度:{i[5]}",
            "choices": i[7:7+int(i[6])],
            "type": getType(i[1]),
            "answer": getAnswer(i),
            "hint": i[4]
        })
    print(len(problemInfo["problems"]), i[3], problemInfo["problems"][-1]["answer"])

#print(problemInfo)
with open("2025jdsgy.json", "w", encoding="utf-8") as f:
    json.dump(problemInfo, f)