<script setup lang="ts">
import { computed, ref, type ComputedRef, type Ref } from 'vue';
import { NInput, NIcon, NSkeleton, NTag, NEmpty } from 'naive-ui';
import { Search } from '@vicons/ionicons5';

import axios from 'axios';
import { useRouter } from 'vue-router';
import type { ProblemShowType } from '@/base/ProblemTypes';
const router = useRouter();

const categories = ref([]);
const recommended: Ref<ProblemShowType[]> = ref([]);
const problems: Ref<{ [key: string]: ProblemShowType }> = ref({});

const searchPattern = ref("");
const tagPattern = ref("");

const loading = ref(true);

function updateSearchPattern(v: string) {
    searchPattern.value = v;
}

function updateTagPattern(v: string) {
    tagPattern.value = v;
    const toTop = setInterval(() => {
        if (document.documentElement.scrollTop < 10) {
            document.documentElement.scrollTop = 0;
            clearInterval(toTop);
        }
        else
            document.documentElement.scrollTop -= 10;
    }, 10);
}

function gotoTest(id: string) {
    router.push({ name: 'Test', params: { id } })
}

const showList: ComputedRef<any[]> = computed(() => {
    // 如果没有搜索，就直接返回推荐项目
    if (tagPattern.value.length === 0 && searchPattern.value.length === 0)
        return recommended.value;
    else {
        let res = Object.values(problems.value);
        if (tagPattern.value === "recommended")
            res = recommended.value;
        if (tagPattern.value.length > 0 && tagPattern.value !== "all" && tagPattern.value !== "recommended") {
            res = res.filter(v => v.categories.indexOf(tagPattern.value) !== -1);
        }
        if (searchPattern.value.length > 0) {
            res = res.filter(v => v.title.indexOf(searchPattern.value) !== -1);
        }
        return res;
    }
});

const tagText = computed(() => {
    if (searchPattern.value && tagPattern.value.length === 0)
        return "全部";
    else if (tagPattern.value === "all")
        return "全部";
    else if (tagPattern.value === "recommended")
        return "推荐";
    else
        return tagPattern.value;
})

axios.get("/data/list.json").then(res => {
    loading.value = false;

    categories.value = res.data.categories;
    problems.value = res.data.problems;
    for (let i in problems.value) {
        problems.value[i].id = i;
    }
    // 计算出recommended的内容
    recommended.value = []
    for (let i of res.data.recommended) {
        recommended.value.push(problems.value[i]);
    }
});
</script>

<template>
    <div class="v-container">
        <h2 class="v-header">vtix 答题自测</h2>
        <n-input placeholder="搜索" :on-input="updateSearchPattern" size="large" clearable>
            <template #prefix>
                <n-icon :component="Search" />
            </template>
        </n-input>
        <template v-if="searchPattern.length === 0 && tagPattern.length === 0">
            <h3 class="v-subheader">推荐</h3>
        </template>
        <template v-else>
            <h3 class="v-subheader"><template v-if="tagText">{{ tagText }}类别</template><template
                    v-if="searchPattern">搜索：{{ searchPattern }}</template></h3>
        </template>
        <div class="v-card-list">
            <template v-if="loading">
                <div class="v-card">
                    <n-skeleton text size="medium" />
                    <n-skeleton text :repeat="2" />
                </div>
            </template>
            <template v-else>
                <template v-if="showList.length > 0">
                    <div class="v-card v-card-link main-item" v-for="(r, i) in showList" @click="gotoTest(r.id)"
                        v-bind:key="i">
                        <span class="v-card-title-small">{{ r.title }}</span>
                        <div class="v-card-append">时间：{{ r.time }} &nbsp; 分类：<span class="v-tag v-tag-success"
                                v-for="(t, j) in r.categories" v-bind:key="j">{{ t }}</span></div>
                    </div>
                </template>
                <div class="v-card" v-else>
                    <n-empty description="找不到符合要求的练习题库">
                    </n-empty>
                </div>
            </template>
        </div>
        <h3 class="v-subheader">分类</h3>
        <div class="v-row">
            <template v-if="loading">
                <div class="v-column" v-for="t of 4" v-bind:key="t">
                    <div class="v-card">
                        <n-skeleton text size="medium" />
                        <n-skeleton text :repeat="1" />
                    </div>
                </div>
            </template>
            <template v-else>
                <div class="v-column">
                    <div class="v-card v-card-link" @click="updateTagPattern('all')">
                        <span class="v-card-title-small">全部</span>
                    </div>
                </div>
                <div class="v-column">
                    <div class="v-card v-card-link" @click="updateTagPattern('recommended')">
                        <span class="v-card-title-small">推荐</span>
                    </div>
                </div>
                <div class="v-column" v-for="(c, i) in categories" v-bind:key="i">
                    <div class="v-card v-card-link" @click="updateTagPattern(c)">
                        <span class="v-card-title-small">{{ c }}</span>
                    </div>
                </div>
            </template>
        </div>
    </div>
</template>
