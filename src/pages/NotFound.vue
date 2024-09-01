<script setup lang="ts">
import { NButton } from "naive-ui";
import { useRouter } from "vue-router";

const router = useRouter();

function gotoHome() {
    router.push("/");
}
</script>

<template>
    <div class="v-container">
        <h2 class="v-header">vtix 答题自测</h2>
        <div class="v-divider"></div>
        <h1 class="text-center">
            404 Not Found
        </h1>
        <n-button @click="gotoHome" type="primary">回首页</n-button>
    </div>
</template>