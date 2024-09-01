<script lang="ts">
import axios from "axios";

export default {
    data() {
        return {
            types: ["送分题", "单选题", "多选题", "填空题", "判断题"],
            chs: ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N"],
            problemInfo: {},
            nowProblems: [],
            problemState: [],
            nowAnswer: [],
            rightAnswer: [],
            wrongAnswer: [],
            answerList: [],
            errorProblems: [],
            writeAnswer: "",
            nowId: 0,
            fading: false,
            testMode: false,
            isLoading: true,
            practiceMode: 0,
            showMode: 1,
            errorMode: false,
            lastManage: 0,
            score: 0,
            viewMode: false,
            timeCount: 0,
            timeCounter: 0,
            nowTestMode: 100,
            pre: [0, 0, 0, 0, 0],
            scoreSet: [0, 0, 0, 0, 0],
            setPrac: false,
            chosenTypes: [0, 1, 2, 3, 4],
            chosenRuffle: true,
            movePos: [0, 0],
            moveEndPos: [0, 0],
            isMoving: true,
        }
    },
    watch: {
        nowId(n, o) {
            this.nowAnswer = this.answerList[n]
            this.rightAnswer = []
            this.wrongAnswer = []
            if (this.nowProblems[n].type === 3) {
                if (this.nowAnswer.length > 0)
                    this.writeAnswer = this.nowAnswer[0]
                else
                    this.writeAnswer = ""
            }
            if (this.problemState[n] > 1) {
                this.problemState[n] = -1
                this.submitAnswer()
            }
            this.showMode = 1
            this.storeInfo()
        }
    },
    computed: {
        rightRate() {
            if (this.problemState.filter(v => v >= 2).length === 0)
                return (0).toFixed(2)
            return (this.problemState.filter(v => v === 2).length / this.problemState.filter(v => v >= 2).length * 100).toFixed(2)
        }
    },
    beforeUnmount() {
        clearInterval(this.timeCounter)
    },
    async mounted() {
        const _t = this
        let pid = _t.$route.params.id
        try {
            const pinfo = await axios.get(`/data/${pid}.json`)
            _t.problemInfo = pinfo.data
            _t.isLoading = false
        }
        catch (e) {
            _t.$router.replace("/notfound")
        }
        try {
            if (localStorage.vstcSaved == _t.problemInfo.title) {
                //console.log("OK")
                _t.nowProblems = JSON.parse(localStorage.nowProblems)
                _t.problemState = JSON.parse(localStorage.problemState)
                _t.answerList = JSON.parse(localStorage.answerList)
                _t.errorProblems = JSON.parse(localStorage.errorProblems)
                _t.practiceMode = Number(localStorage.practiceMode) || 0
                _t.testMode = localStorage.testMode == 'true' ? true : false
                _t.errorMode = localStorage.errorMode == 'true' ? true : false
                _t.nowId = Number(localStorage.nowId) || 0
                //console.log(_t.problemState[_t.nowId])
                if (_t.nowProblems[_t.nowId].type === 3) {
                    if (_t.nowAnswer.length > 0)
                        _t.writeAnswer = _t.nowAnswer[0]
                    else
                        _t.writeAnswer = ""
                }
                if (_t.problemState[_t.nowId] > 1) {
                    _t.problemState[_t.nowId] = -1
                    _t.submitAnswer()
                }
            }
            else {
                _t.nowProblems = _t.problemInfo.problems
                _t.answerList = []
                _t.problemState = []
                for (let i in _t.nowProblems) {
                    _t.answerList.push([])
                    _t.problemState.push(0)
                }
                _t.errorProblems = []
                _t.nowId = 0
                _t.testMode = false
                _t.errorMode = false
            }
        }
        catch (e) {
            _t.nowProblems = _t.problemInfo.problems
            _t.answerList = []
            _t.problemState = []
            for (let i in _t.nowProblems) {
                _t.answerList.push([])
                _t.problemState.push(0)
            }
            _t.errorProblems = []
            _t.nowId = 0
            _t.testMode = false
            _t.errorMode = false
        }

        document.addEventListener("keydown", (e) => {
            const tmp = e.key.toUpperCase()
            const pos = _t.chs.indexOf(tmp)
            const qwerty = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P']
            const pos2 = qwerty.indexOf(tmp)
            //console.log(tmp)
            if (tmp == "ENTER") {
                _t.submitAnswer()
                e.preventDefault()
            }
            else if (pos2 != -1 && pos2 >= 0 && pos2 < _t.nowProblems[_t.nowId].choices.length)
                _t.choose(pos2)
            else if (pos != -1 && pos >= 0 && pos < _t.nowProblems[_t.nowId].choices.length)
                _t.choose(pos)
            else if (tmp == "ARROWLEFT" && _t.nowId > 0)
                _t.nowId -= 1
            else if (tmp == "ARROWRIGHT" && _t.nowId + 1 < _t.nowProblems.length)
                _t.nowId += 1

        })
    },
    methods: {
        hashCode(str) {
            let hash = 0
            for (var i = 0; i < str.length; i++) {
                hash = ~~(((hash << 5) - hash) + str.charCodeAt(i))
            }
            return Math.abs(hash)
        },
        choose(k) {
            if (this.problemState[this.nowId] > 1)
                return
            if (this.nowProblems[this.nowId].type === 1 || this.nowProblems[this.nowId].type === 4) {
                this.nowAnswer = [k]
                this.submitAnswer()
            }
            else {
                if (this.nowAnswer.indexOf(k) !== -1) {
                    this.nowAnswer = this.nowAnswer.filter(v => v !== k)
                }
                else
                    this.nowAnswer.push(k)
            }
        },
        nextProblem(flag = true) {
            if (this.nowId + 1 < this.nowProblems.length && flag) {
                //setTimeout(() => {
                //    this.fading = true
                //this.nowId += 1
                //}, 150)
                setTimeout(() => {
                    this.nowId += 1
                }, 150)
                //setTimeout(() => {
                //    this.fading = false
                //}, 250)
            }
        },
        checkAnswer(d = -1) {
            this.rightAnswer = []
            this.wrongAnswer = []
            let checkProblemId = d
            if (d !== -1)
                this.nowAnswer = this.answerList[d]
            if (checkProblemId === -1)
                checkProblemId = this.nowId
            if (this.problemState[checkProblemId] > 1)
                return
            let flag = true
            if (this.problemState[checkProblemId] === -1)
                flag = false
            let passed = 0
            if (this.nowProblems[checkProblemId].type === 1 || this.nowProblems[checkProblemId].type === 4) {
                for (let i in this.nowAnswer) {
                    if (this.nowAnswer[i] === this.nowProblems[checkProblemId].answer) {
                        if (passed !== 2)
                            passed = 1
                        this.rightAnswer.push(this.nowAnswer[i])
                    }
                    else {
                        this.wrongAnswer.push(this.nowAnswer[i])
                        passed = 2
                    }
                }
                if (passed !== 1)
                    this.rightAnswer.push(this.nowProblems[checkProblemId].answer)
            }
            else if (this.nowProblems[checkProblemId].type === 2) {
                for (let i in this.nowProblems[checkProblemId].answer) {
                    if (this.nowAnswer.indexOf(this.nowProblems[checkProblemId].answer[i]) === -1) {
                        this.rightAnswer.push(this.nowProblems[checkProblemId].answer[i])
                        this.wrongAnswer.push(this.nowProblems[checkProblemId].answer[i])
                        passed = 2
                    }
                }
                if (passed === 0)
                    passed = 1
                for (let i in this.nowAnswer) {
                    if (this.nowProblems[checkProblemId].answer.indexOf(this.nowAnswer[i]) === -1) {
                        this.wrongAnswer.push(this.nowAnswer[i])
                        passed = 2
                    }
                    else {
                        this.rightAnswer.push(this.nowAnswer[i])
                    }
                }
            }
            else if (this.nowProblems[checkProblemId].type === 3) {
                let p = []
                if (d != -1) {
                    if (this.nowAnswer.length > 0) {
                        this.nowAnswer[0] = this.nowAnswer[0].replace(/，/g, ",")
                        p = this.nowAnswer[0].split(",")
                    }
                }
                else {
                    this.writeAnswer = this.writeAnswer.replace(/，/g, ",")
                    p = this.writeAnswer.split(",")
                }
                p.forEach(v => {
                    v = v.trim()
                })
                passed = 1
                let q = this.nowProblems[checkProblemId].answer.split(",")
                q.forEach(v => {
                    v = v.trim()
                })
                if (p.length != q.length)
                    passed = 2
                else {
                    for (let i = 0; i < p.length; ++i) {
                        let tmp = q[i].split(";")
                        tmp.forEach(v => {
                            v = v.trim()
                        })
                        if (tmp.indexOf(p[i]) == -1) {
                            passed = 2
                            break
                        }
                    }
                    //if (this.nowAnswer[0] === this.nowProblems[checkProblemId].answer)
                    //    passed = 1
                }
                this.nowAnswer[0] = p.join(",")
            }
            this.answerList[checkProblemId] = this.nowAnswer
            if (passed === 1) {
                if (flag) {
                    this.score += this.scoreSet[this.nowProblems[checkProblemId].type]
                }
                this.problemState[checkProblemId] = 2
                if (d === -1)
                    this.nextProblem(flag)
            }
            else {
                if (flag && !this.errorMode) {
                    this.errorProblems.push(this.nowProblems[checkProblemId])
                    localStorage.errorProblems = JSON.stringify(this.errorProblems)
                }
                this.problemState[checkProblemId] = 3
            }
        },
        clearRecord() {
            this.nowAnswer = []
            this.rightAnswer = []
            this.wrongAnswer = []
            this.problemState = []
            this.answerList = []
            this.writeAnswer = ""
            this.nowId = 0
            for (let i in this.nowProblems) {
                this.problemState.push(0)
                this.answerList.push([])
            }
            this.showMode = 1
            this.storeInfo()
        },
        normalPractice() {
            this.practiceMode = 0
            this.errorMode = false
            this.testMode = false
            this.viewMode = false
            this.setPrac = false
            this.nowProblems = [...this.problemInfo.problems]
            this.clearRecord()
        },
        ruffleProblem() {
            this.practiceMode = 1
            this.errorMode = false
            this.testMode = false
            this.viewMode = false
            this.setPrac = false
            this.nowProblems = [...this.problemInfo.problems]
            this.nowProblems.sort(() => Math.random() - 0.5)
            for (let i in this.nowProblems) {
                if (this.nowProblems[i].type === 1) {
                    let ans = this.hashCode(this.nowProblems[i].choices[this.nowProblems[i].answer])
                    this.nowProblems[i].choices.sort(() => Math.random() - 0.5)
                    for (let j in this.nowProblems[i].choices)
                        if (this.hashCode(this.nowProblems[i].choices[j]) === ans) {
                            this.nowProblems[i].answer = Number(j)
                            break
                        }
                } else if (this.nowProblems[i].type === 2) {
                    let ans = []
                    for (let j in this.nowProblems[i].answer)
                        ans.push(this.hashCode(this.nowProblems[i].choices[this.nowProblems[i].answer[j]]))
                    //console.log(ans, this.nowProblems[i].answer)
                    this.nowProblems[i].answer = []
                    this.nowProblems[i].choices.sort(() => Math.random() - 0.5)
                    for (let j in this.nowProblems[i].choices) {
                        //console.log(this.nowProblems[i].choices[j], this.hashCode(this.nowProblems[i].choices[j]))
                        if (ans.indexOf(this.hashCode(this.nowProblems[i].choices[j])) !== -1)
                            this.nowProblems[i].answer.push(Number(j))
                    }
                }
            }
            this.clearRecord()
        },
        submitAnswer(d = -1) {
            let checkProblemId = d
            if (checkProblemId === -1)
                checkProblemId = this.nowId
            if (this.testMode) {
                if (this.nowProblems[checkProblemId].type === 3) {
                    this.answerList[checkProblemId] = [String(this.writeAnswer)]
                    this.writeAnswer = ""
                }
                else
                    this.answerList[checkProblemId] = this.nowAnswer
                this.problemState[checkProblemId] = 1
                this.nextProblem()
            }
            else {
                this.checkAnswer()
            }
            this.storeInfo()
        },
        storeInfo() {
            // Store Info
            if (this.testMode)
                return
            localStorage.vstcSaved = this.problemInfo.title
            localStorage.nowProblems = JSON.stringify(this.nowProblems)
            localStorage.nowId = String(this.nowId)
            localStorage.practiceMode = String(this.practiceMode)
            localStorage.testMode = String(this.testMode)
            localStorage.errorMode = String(this.errorMode)
            localStorage.problemState = JSON.stringify(this.problemState)
            localStorage.answerList = JSON.stringify(this.answerList)
        },
        submitPaper() {
            for (let i in this.nowProblems)
                this.checkAnswer(i)
            this.testMode = false
            this.errorMode = false
            this.nowAnswer = this.answerList[this.nowId]
            this.showMode = 2
            this.viewMode = true
            clearInterval(this.timeCounter)
        },
        doTest() {
            this.ruffleProblem()
            this.practiceMode = 2
            this.testMode = true
            this.errorMode = false
            this.setPrac = false
            this.nowTestMode = this.problemInfo.test
            this.scoreSet = this.problemInfo.score
            if (typeof (this.problemInfo.test) == typeof (0))
                this.nowProblems = this.nowProblems.slice(0, this.problemInfo.test)
            else {
                const nowProblemsCopy = [...this.nowProblems]
                this.nowProblems = []
                for (let i = 0; i < this.problemInfo.test.length; ++i) {
                    let tmp = this.problemInfo.test[i]
                    for (let j = 0; j < nowProblemsCopy.length; ++j)
                        if (nowProblemsCopy[j].type == i) {
                            this.nowProblems.push(nowProblemsCopy[j])
                            tmp -= 1
                            if (tmp == 0)
                                break
                        }
                }
                this.pre = [0, 0, 0, 0, 0]
                for (let i = 1; i < this.problemInfo.test.length; ++i)
                    this.pre[i] = this.pre[i - 1] + this.problemInfo.test[i - 1]
            }
            this.viewMode = false
            this.timeCount = 0
            this.score = 0
            clearInterval(this.timeCounter)
            this.timeCounter = setInterval(() => {
                this.timeCount += 1
            }, 1000)
        },
        doWrongProblems() {
            if (this.errorProblems.length == 0) {
                alert("暂无错题!")
                return
            }
            this.practiceMode = 3
            this.errorMode = true
            this.testMode = false
            this.viewMode = false
            this.setPrac = false
            this.nowProblems = [...this.errorProblems]
            this.clearRecord()
        },
        deleteThisProblem(id) {
            if ((new Date().getTime()) - this.lastManage <= 120000 || confirm("真的要移除这道题吗？")) {
                this.lastManage = new Date().getTime()
                if (id < 0 || id >= this.errorProblems.length)
                    return
                if (this.errorProblems.length == 1) {
                    this.errorProblems = []
                    alert("错题已经全部清空!")
                    this.normalPractice()
                    return
                }
                this.problemState = this.problemState.slice(0, id).concat(this.problemState.slice(id + 1))
                this.answerList = this.answerList.slice(0, id).concat(this.answerList.slice(id + 1))
                this.errorProblems = this.errorProblems.slice(0, id).concat(this.errorProblems.slice(id + 1))
                for (let i = this.answerList.length; i < this.errorProblems.length; ++i) {
                    this.problemState.push(0)
                    this.answerList.push([])
                }
                //console.log(this.errorProblems)
                this.nowProblems = [...this.errorProblems]
                if (id == this.errorProblems.length)
                    --this.nowId
                const tmp = this.nowId
                this.nowId = tmp
                this.storeInfo()
            }
        },
        clearWrongProblem() {
            if (confirm("真的要清空全部错题吗？")) {
                this.errorProblems = []
                alert("错题已经全部清空!")
                this.normalPractice()
            }
        },
        preferencePractice() {
            this.errorMode = true
            this.testMode = false
            this.viewMode = false
            this.ruffleProblem()
            this.practiceMode = 4
            this.setPrac = true
        },
        startPractice() {
            this.setPrac = false
            let nowProblemsCopy = []
            if (this.chosenRuffle)
                nowProblemsCopy = [...this.nowProblems]
            else
                nowProblemsCopy = [...this.problemInfo.problems]
            this.nowProblems = []
            for (let i = 0; i < nowProblemsCopy.length; ++i)
                if (this.chosenTypes.indexOf(nowProblemsCopy[i].type) != -1)
                    this.nowProblems.push(nowProblemsCopy[i])
            if (this.nowProblems.length == 0) {
                alert("这样子设定就没有题目可以做了呢")
                this.normalPractice()
            }
        },
        moveStart(e) {
            this.movePos = [e.targetTouches[0].pageX, e.targetTouches[0].pageY]
        },
        onMove(e) {
            this.moveEndPos = [e.targetTouches[0].pageX, e.targetTouches[0].pageY]
            const dValueX = this.movePos[0] - this.moveEndPos[0]
            const dValueY = Math.abs(this.movePos[1] - this.moveEndPos[1])
            //console.log(dValueX, dValueY)
            if (Math.abs(dValueX) > dValueY) {
                e.preventDefault()
                this.$refs.problemShow.style.transform = `translateX(${-dValueX}px)`
            }
        },
        moveEnd(e) {
            const dValueX = Math.abs(this.movePos[0] - this.moveEndPos[0])
            const dValueY = Math.abs(this.movePos[1] - this.moveEndPos[1])
            //console.log(dValueX, dValueY)
            const pa = Math.floor(document.body.offsetWidth / 2.5)
            if (dValueX > dValueY) {
                e.preventDefault()
                if (dValueX > pa) {
                    if (this.movePos[0] > this.moveEndPos[0]) {
                        if (this.nowId + 1 < this.nowProblems.length)
                            this.nowId += 1
                    } else if (dValueX > pa) {
                        if (this.nowId)
                            this.nowId -= 1
                    }
                }
            }
            this.isMoving = false
            this.movePos = [0, 0]
            this.moveEndPos = [0, 0]
            this.$refs.problemShow.style.transform = ``
        },
        timeFormat(e) {
            let res = ""
            let min = Math.floor(e / 60)
            let sec = e % 60
            if (min < 10)
                res = res + '0'
            res = res + String(min)
            res += "分"
            if (sec < 10)
                res = res + '0'
            res = res + String(sec)
            res += "秒"
            return res
        }
    }
}
</script>
<template>
    <div class="v-container"></div>
    <div class="h3 mb-3 main-title" style="color: #212223;">
        <div class="title-text"><template v-if="!isLoading">{{ problemInfo.title }} - </template>VSTC 答题自测<br>
            <span style="display: none" class="show">
                <span v-if="testMode">
                    用时：{{ timeFormat(timeCount) }}
                </span>
                <span v-else-if="viewMode">用时：{{ timeFormat(timeCount) }}，得分：{{ score }}</span>
                <span v-else>
                    <span>正确:{{ this.problemState.filter(v => v === 2).length }},已答:{{
                        this.problemState.filter(v => v > 0).length
                        }},</span>正确率: {{ rightRate }}%
                </span>
            </span>
        </div>
    </div>
    <button class="display-none show btn-icon btn btn-info btn-sm menu-btn1"
        @click="showMode == 0 ? showMode = 1 : showMode = 0">
        <i class="fal fa-x" v-if="showMode == 0"></i>
        <i class="fal fa-bars" v-else></i>
    </button>
    <button class="display-none show btn-icon btn btn-light btn-sm menu-btn2"
        @click="showMode == 2 ? showMode = 1 : showMode = 2">
        <i class="fal fa-x" v-if="showMode == 2"></i>
        <i class="fal fa-compass" v-else></i>
    </button>
    <ul class="nav" :class="{
        show: showMode === 0,
        hidden: showMode !== 0,
    }">
        <li class="nav-item">
            <router-link class="nav-link" :to="{ name: 'Index' }">
                <i class="fal fa-home"></i>返回首页
            </router-link>
        </li>
        <li class="nav-item">
            <a class="nav-link primary" :class="{ active: practiceMode == 0 }" href="javascript:;"
                @click="normalPractice()">
                <i class="fal fa-pen"></i>顺序练习
            </a>
        </li>
        <li class="nav-item">
            <a class="nav-link primary" :class="{ active: practiceMode == 1 }" href="javascript:;"
                @click="ruffleProblem()">
                <i class="fal fa-shuffle"></i>打乱题序
            </a>
        </li>
        <li class="nav-item">
            <a class="nav-link primary" :class="{ active: practiceMode == 4 }" href="javascript:;"
                @click="preferencePractice()">
                <i class="fal fa-cog"></i>自定义练习
            </a>
        </li>
        <li class="nav-item">
            <a class="nav-link red" :class="{ active: practiceMode == 2 }" href="javascript:;" @click="doTest()">
                <i class="fal fa-scroll"></i>模拟测试
            </a>
        </li>
        <li class="nav-item">
            <a class="nav-link orange" :class="{ active: practiceMode == 3 }" href="javascript:;"
                @click="doWrongProblems()">
                <i class="fal fa-x"></i>错题回顾
            </a>
        </li>
        <li class="nav-item">
            <a class="nav-link show" style="display: none" :class="{ active: practiceMode == 3 }"
                href="javascript:alert('请加qq 1440169768!')">
                <i class="fal fa-comments"></i>意见反馈
            </a>
        </li>
    </ul>
    <div class="loader d-flex justify-content-center" v-if="isLoading">
        <div class="spinner-border text-primary" style="margin: auto"></div>
    </div>
    <template v-else>
        <div class="row">
            <div class="col-md-9 col-sm-12" style="height: 100%;" :class="{
                show: showMode === 1,
                hidden: showMode !== 1
            }">
                <!--div class="height-100" @touchstart="moveStart" @touchmove="onMove" @touchend="moveEnd"
                    :class="{ fade: fading }" style="transition: all .2s"-->
                <div class="height-100" :class="{ fade: fading }" style="transition: all .2s">
                    <div class="problem-show" ref="problemShow">
                        <template v-if="setPrac">
                            <h4>设定练习题库</h4>
                            <div class="field">
                                <label for="pracType">练习题型</label><br>
                                <div class="row">
                                    <div class="col" v-for="(z, i) in types">
                                        {{ z }}<br>
                                        <label class="custom-toggle">
                                            <input type="checkbox" name="pracType" v-model="chosenTypes" :value="i">
                                            <span class="custom-toggle-slider rounded-circle"></span>
                                        </label>
                                    </div>
                                </div>
                            </div>
                            <div class="field">
                                <div class="custom-control custom-checkbox mb-3">
                                    <input class="custom-control-input" id="chosenRuffle" type="checkbox"
                                        v-model="chosenRuffle">
                                    <label class="custom-control-label" for="chosenRuffle">
                                        <span>打乱题序</span>
                                    </label>
                                </div>
                            </div>
                            <div class="field">
                                <button class="btn btn-light btn-sm" @click="startPractice()">开始练习!</button>
                            </div>
                        </template>
                        <template v-else>
                            <div class="problem-content mb-4">
                                <span class="badge badge-primary mr-2">{{ types[nowProblems[nowId].type] }}</span>{{
                                    nowId +
                                    1
                                }}/{{
                                nowProblems.length
                                }}.
                                <span v-text="nowProblems[nowId].content"></span>
                            </div>
                            <div class="answer-area mb-4">
                                <template v-if="nowProblems[nowId].type === 3">
                                    <div class="form-group">
                                        <input class="form-control form-control-alternative" :class="{
                                            'input-success': problemState[nowId] === 2,
                                            'input-error': problemState[nowId] === 3,
                                        }" v-model="writeAnswer" placeholder="多个答案之间用逗号隔开！">
                                    </div>
                                    <div v-if="problemState[nowId] === 3" class="form-group">
                                        <input class="form-control form-control-alternative input-success readonly"
                                            readonly :value="nowProblems[nowId].answer">
                                    </div>
                                </template>
                                <template v-else>
                                    <span class="choose-box" :class="{
                                        chosen: nowAnswer.indexOf(i) !== -1,
                                        wrong: wrongAnswer.indexOf(i) !== -1,
                                        right: rightAnswer.indexOf(i) !== -1
                                    }" v-for="(c, i) in nowProblems[nowId].choices" @click="choose(i)">
                                        {{ chs[i] }}. {{ c }}</span>
                                </template>
                            </div>
                        </template>
                    </div>
                    <div class="manage-area" v-if="!setPrac">
                        <button class="btn btn-icon btn-primary btn-sm" type="button"
                            v-if="(problemState[nowId] <= 1) && (nowProblems[nowId].type !== 1) && (nowProblems[nowId].type !== 4)"
                            @click="submitAnswer()">
                            <span class="btn-inner--icon">
                                <i class="fal fa-check"></i></span>
                            <span class="btn-inner--text">确定</span>
                        </button>
                        <button class="btn btn-icon btn-light btn-sm" type="button" v-if="this.nowId > 0"
                            @click="this.nowId -= 1">
                            <span class="btn-inner--icon">
                                <i class="far fa-chevron-left"></i></span>
                            <span class="btn-inner--text">上一题</span>
                        </button>
                        <button class="btn btn-icon btn-light btn-sm" type="button"
                            v-if="this.nowId + 1 < this.nowProblems.length" @click="this.nowId += 1">
                            <span class="btn-inner--text">下一题</span><span class="btn-inner--icon">
                                <i class="far fa-chevron-right"></i></span>
                        </button>
                        <button class="btn btn-icon btn-outline-danger btn-sm" type="button" v-if="this.errorMode"
                            @click="deleteThisProblem(this.nowId)">
                            <span class="btn-inner--icon">
                                <i class="far fa-x"></i></span>
                            <span class="btn-inner--text">移出错题</span>
                        </button>
                        <button class="btn btn-icon btn-outline-light btn-sm" type="button" v-if="this.errorMode"
                            @click="clearWrongProblem()">
                            <span class="btn-inner--icon">
                                <i class="far fa-trash"></i></span>
                        </button>
                        <button class="btn btn-icon btn-info btn-sm" type="button" v-if="testMode" @click="submitPaper">
                            <span class="btn-inner--icon">
                                <i class="fal fa-paper-plane"></i></span>
                            <span class="btn-inner--text">交卷</span>
                        </button>
                    </div>
                </div>
            </div>
            <div class="col-md-3 col-sm-12" :class="{
                show: showMode === 2,
                hidden: showMode !== 2
            }">
                <div class="hidden">
                    <span v-if="testMode">
                        用时：{{ timeFormat(timeCount) }}
                    </span>
                    <span v-else-if="viewMode">用时：{{ timeFormat(timeCount) }}，得分：{{ score }}</span>
                    <span v-else>
                        <span>正确:{{ this.problemState.filter(v => v === 2).length }},已答:{{
                            this.problemState.filter(v => v > 0).length
                            }},</span>正确率: {{ rightRate }}%
                    </span>
                </div>
                <div class="choice-buttons">
                    <div style="height: 1px; width:100%; background-color: #eee;margin: 5px 0;"></div>
                    <template v-if="(testMode || viewMode) && typeof (nowTestMode) != typeof (0)">
                        <template v-for="(zs, k) in nowTestMode">
                            <template v-if="zs > 0">
                                <b>{{ types[k] }}({{ scoreSet[k] * zs }}分)</b><br>
                                <button class="btn btn-sm" :class="{
                                    'btn-outline-light': (problemState[g + pre[k] - 1] === 0),
                                    'btn-outline-primary': problemState[g + pre[k] - 1] === 1,
                                    'btn-outline-success': problemState[g + pre[k] - 1] === 2,
                                    'btn-outline-danger': problemState[g + pre[k] - 1] === 3,
                                }" style="margin: 5px" v-for="g in zs" @click="nowId = g + pre[k] - 1">{{ g + pre[k]
                                    }}</button><br>
                            </template>
                        </template>
                    </template>
                    <button v-else class="btn btn-sm" :class="{
                        'btn-outline-light': (problemState[k - 1] === 0),
                        'btn-outline-primary': problemState[k - 1] === 1,
                        'btn-outline-success': problemState[k - 1] === 2,
                        'btn-outline-danger': problemState[k - 1] === 3,
                    }" style="margin: 5px" v-for="k in nowProblems.length" @click="nowId = k - 1">{{ k }}</button>
                </div>
            </div>
            <div class="divider hidden"></div>
            <a href="javascript:alert('请加qq 1440169768!')">意见反馈</a>&nbsp; | By&nbsp;<a
                href="https://github.com/yemaster/vstc">yemaster</a>.
        </div>
    </template>
</template>