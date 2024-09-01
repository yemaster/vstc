<script setup lang="ts">
import { NMessageProvider, NNotificationProvider } from "naive-ui";
import PageFooter from "@/components/PageFooter.vue";
</script>

<template>
    <n-notification-provider>
        <n-message-provider>
            <router-view></router-view>
            <PageFooter />
        </n-message-provider>
    </n-notification-provider>
</template>