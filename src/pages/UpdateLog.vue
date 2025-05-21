<script setup lang="ts">
import { useRouter } from "vue-router";

import { NIcon, NA } from "naive-ui";
import { ChevronBackSharp } from "@vicons/ionicons5";

const router = useRouter();

function backToHome() {
    router.push('/');
}
</script>

<template>
    <div class="v-container">
        <div class="v-ti-subheader link" @click="backToHome"><n-icon :component="ChevronBackSharp"></n-icon> <span>vtix
                答题自测</span></div>
        <h2 class="v-ti-header">更新日志</h2>
    </div>
    <div class="v-divider"></div>
    <div class="v-container">
        <h3>2025-5-21 更新</h3>
        <ul>
            <li>新增 2025 近代史纲要</li>
            <li>新增题目解析</li>
        </ul>
        <h3>2024-12-23 更新</h3>
        <ul>
            <li>修复了导入存档无效的问题</li>
            <li>修复了存档删除后没用的问题</li>
        </ul>
        <h3>2024-12-19 更新</h3>
        <ul>
            <li>(<n-a href="https://github.com/yemaster/vstc/commits?author=Zhehan-Z" target="_blank">@Zhehan-Z</n-a>) 增加了存档的频率，放置存档丢失 Commit <n-a href="https://github.com/yemaster/vstc/commit/3a30aafc30b7d777f075683ea1614ce5e72ed3fe" target="_blank">3a30aaf</n-a></li>
        </ul>
        <h3>2024-06-18 更新</h3>
        <ul>
            <li>不同答题练习的存档分开储存，方便错题练习后重新回到相应答题中</li>
            <li>优化了部分界面</li>
        </ul>
        <h3>2024-06-17 更新</h3>
        <ul>
            <li>错题支持导出和导入json文件</li>
            <li>优化了性能</li>
            <li>优化了部分界面</li>
        </ul>
        <h3>2023-5-21 更新</h3>
        <ul>
            <li>全新界面，采用Vue 3和Naive UI</li>
        </ul>
        <h3>2023-12-28 更新</h3>
        <ul>
            <li>我也不知道更新了什么</li>
        </ul>
        <h3>2023-12-26 更新</h3>
        <ul>
            <li>我也不知道更新了什么</li>
        </ul>
        <h3>2023-12-21</h3>
        <ul>
            <li>上线</li>
        </ul>
    </div>
</template>