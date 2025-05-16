# vtix（旧版）

> [!NOTE]
> 新版仓库地址 [https://github.com/yemaster/vtix-ng](https://github.com/yemaster/vtix-ng)

## 📚 什么是 vtix？

因为学校开学有校纪校规等考试，另外很多政治课也有机考。为了方便大家的练习，就有了 vtix。

**欢迎更多小伙伴加入开发！！！**

- 🔗 WebSite：https://ti.u5tc.cn
- 题库大乱斗：未开启（仅在特定时期开放），[github](https://github.com/yemaster/vtix-scrimmage)
- blog：[https://blog.yemaster.cn](https://blog.yemaster.cn)

### ✨ Features

- 支持多种题目类型
- 丰富练习方式：顺序练习，乱序练习，自定义练习，错题练习，模拟测试
- 导入导出错题记录

### 📅 近期计划

- 长远期：代码已经成屎山，而且就糊在一个文件里，bug 特别多，所以预计打算重构代码，并且加入后端，多端同步，以及可视化编辑界面。
- 答题排行榜

## 🛠️ 贡献指南

### 📑 贡献题库

题库文件位置 `public/data`，题库格式 `json`。其中 `list.json` 存放着的是题库列表，以及推荐题库。其他的 `json` 文件就是题库内容。

您可以根据如下 TypeScript 类型定义的题库，然后编写 json 题库文件来贡献题库。如果您看不懂如下示例，也可以参考题库目录下已经有的 `json` 文件，来仿照着编写。

#### TypeScript 类型定义示例

```typescript
// ProblemListType 就是题库，最后 json 文件必须符合这个类型
type ProblemListType = {
    title: string;  // title 指的是题库的标题，如“2024年xx考试”
    test: [number, number, number, number, number] | number; // test 表示模拟考试中，如果是 5 个 number 的 array 表示每种题型的数量，5 个位置分别表示 送分题、单选题、多选题、填空题、判断题，和下面的 type 一一对应。否则就表示总题目数。
    score: [number, number, number, number, number]; // score 表示每种题目类型的分数，每个位置含义如上。
    problems: ProblemType[]; // problems 就是题库，是一个数组，关于 ProblemType，参见下面定义。
}
// 单选题类型
type SingleChooseProblemType = {
    type: 1;
    content: string; // Content 是题目的描述
    choices: string[]; // 分别是 选项A,选项B,...
    answer: number; // 表示 choices 中答案的下标，比如 0 表示 A 正确。
}
// 多选题类型
type MultiChooseProblemType = {
    type: 2;
    content: string;
    choices: string[];
    answer: number[]; // 表示 choices 中答案的下标的 array，比如 [0,2] 表示 AC 正确。
}
// 填空题类型
export type FillingProblemType = {
    type: 3;
    content: string;
    answer: string; // 表示答案，用文本
}
// 判断题类型
export type JudgementProblemType = {
    type: 4;
    content: string;
    choices: [string, string];
    answer: number;
}
type ChooseProblemType = SingleChooseProblemType | MultiChooseProblemType | JudgementProblemType;
type ProblemType = ChooseProblemType | FillingProblemType;
type ProblemShowType = {
    title: string;
    time: number;
    categories: string[];
    id?: string;
};
```

#### 题库文件示例

```json
{
    "title": "题目的标题",
    "test": 20,
    "score": [0, 1, 1, 1, 1],
    "problems": [
        {
            "content": "题目描述",
            "type": 0,
            "choices": ["选项A", "选项B", "选项C"],
            "answer": 0
        }
    ]
}
```

### 📂 贡献代码

**编程语言**: TypeScript

**前端框架**: Vue 3

**UI 库框架**: Naive UI

**核心文件**

- `public/data`: 存储题目数据
- `/src/pages/TestView.vue`: 核心答题逻辑

#### 🚀 运行项目

#####  1️⃣ 安装必要软件

- Node.js（推荐 v20）
- yarn

##### 2️⃣ 安装项目依赖

```bash
yarn
```

##### 3️⃣ 启动项目

```bash
yarn dev
```

## ❓ 常见问答

**Q: 题目有错怎么办？**
**A:** 加 QQ：**1440169768** 反馈

**Q: 我有更好的功能建议怎么办？**
**A:** 加 QQ：**1440169768** 反馈

**Q: 我也想参与开发怎么办？**
**A:** 看上面文档，也可以加 QQ：**1440169769** 咨询。
