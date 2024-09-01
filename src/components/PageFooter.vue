<script setup lang="ts">
import { NA, useMessage } from "naive-ui";

const message = useMessage();

function feedback() {
    message.info("请加QQ: 1440169768!");
}
</script>

<template>
    <div class="v-container" :class="{ 'hidden': $route.name === 'Test' }">
        <div class="v-divider"></div>
        <div class="v-footer">
            <n-a href="https://github.com/yemaster/vstc" target="_blank">Github</n-a>
            |
            <router-link :to="{ name: 'Update Logs' }" #="{ navigate, href }" custom>
                <n-a :href="href" @click="navigate">
                    更新日志
                </n-a>
            </router-link>
            |
            <n-a href="javascript:;" @click="feedback">意见反馈</n-a>
            |
            Made by <n-a href="https://github.com/yemaster" target="_blank">yemaster</n-a>.
        </div>
    </div>
</template>
