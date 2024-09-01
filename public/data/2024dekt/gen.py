import json

with open("ektk.md", "r", encoding="utf-8") as f:
    data = f.read()

def parse_questions(questions_text):
    questions = []
    current_question = {}
    
    lines = questions_text.strip().split("\n")
    for line in lines:
        if line.strip() == "":
            continue
            
        if line[0].isdigit():
            # 解析题目内容
            content_end = line.rindex("（")
            answer_start = line.rindex("（") + 1
            answer_end = line.rindex("）")
            
            content = line[2:content_end].strip() + "（）"
            answers = line[answer_start:answer_end]
            
            current_question = {
                "content": content,
                "choices": [],
                "answer": []
            }
            
            # 判断题目类型
            if len(answers) > 1:
                current_question["type"] = 2
            else:
                current_question["type"] = 1
            
            # 将答案转换为索引
            for answer in answers:
                current_question["answer"].append(ord(answer) - ord('A'))
        
        else:
            # 解析选项
            if line[0] in ["A", "B", "C", "D"]:
                current_question["choices"].append(line[2:].strip())
                
        # 将当前题目加入到列表中
        if len(current_question.get("choices", [])) == 4:
            if current_question["type"] == 1:
                current_question["answer"] = current_question["answer"][0]
            questions.append(current_question)
            current_question = {}
    
    return questions

# 生成JSON
questions = parse_questions(data)

prob = {
    "title": "2024第二课堂知识测试题库",
    "test": 20,
    "score": [0, 1, 1, 1, 1]
}

prob["problems"] = questions

with open("2024dekt.json", "w", encoding="utf-8") as f:
    json.dump(prob, f)