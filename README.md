# vtix

## 什么是vtix？

因为学校开学有校纪校规等考试，另外很多政治课也有机考。为了方便大家的复习，就有了 vtix。vtix 支持顺序练习、打乱题序、自定义练习、模拟考试、错题回顾，还可以导出导入做题进度。

WebSite: [https://ti.u5tc.cn](https://ti.u5tc.cn)

## 常见问答

- Q: 题目有错怎么办？
  
  A: 加QQ：1440169768反馈
  
-   Q: 我有更好的功能建议怎么办？

    A: 加QQ：1440169768反馈

-   Q: 我想贡献题库怎么办

    A: 按照 [public/data](https://github.com/yemaster/vstc/tree/master/public/data) 文件夹下的 `xxx.json` 的格式，添加新的 `json` 文件，格式是：

    ```json
    {
        "title": "题目的标题",
        "test": 20,   // 模拟测试的题目数量 number 或者 [number, number, number, number, number]，第一种是全部题目选，第二种是设定各题型的数量，题型分别是：送分题、单选题、多选题、填空题、判断题
        "score": [0, 1, 1, 1, 1]" // 每种题型的分值。
        "problems": [{   // 题库
        	"content": "题目描述",
            "type": 0,  // 0送分，1单选，2多选，3填空，4判断
            "choices": ["选项A","选项B",...], // 填空题不需要
    		"answer": 0, // 单选题，判断题是一个number，多选题是一个number[]，填空题是一个string
    	}]
    }
    ```

    

然后修改`list.json`，将新增的题库加上去。然后提交pr，通过之后会自动部署。

或者也可以加QQ：1440169768。

-   Q：我也想参与开发怎么办？

    A：加QQ：1440169768，或者阅读下面的文档。

## 技术栈

Vite+Vue3+NaiveUI

## 运行项目

### 安装必要软件

-   Nodejs，推荐v20
-   yarn

### 安装项目依赖

```sh
yarn
```

### 启动项目

```sh
yarn dev
```

## 项目结构

`/public/data` 存储题库数据

`/src/pages/TestView.vue` 存储核心答题代码

通过 `axios.js` 获取题库的json信息，然后解析之后显示。做题进度用localStorage保存在本地。

项目为纯静态网站，部署在Azure Static App上。提交到Github上自动Build并部署。