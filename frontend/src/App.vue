<script setup lang="ts">
import { onMounted, ref } from 'vue'

type HealthResponse = { status: string; service: string }

const health = ref<HealthResponse | null>(null)
const error = ref('')

onMounted(async () => {
  try {
    const response = await fetch('/api/health')
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    health.value = await response.json() as HealthResponse
  } catch (requestError) {
    error.value = requestError instanceof Error ? requestError.message : '请求失败'
  }
})
</script>

<template>
  <main class="page-shell">
    <section class="hero-card">
      <p class="eyebrow">CLOUD COLLECTION · PHASE 1</p>
      <h1>云端收藏馆</h1>
      <p class="intro">从洛克王国宠物图鉴开始，构建属于自己的兴趣收藏空间。</p>
      <div class="status" :class="{ online: health, offline: error }">
        <span class="dot" />
        <span v-if="health">后端已连接：{{ health.service }}</span>
        <span v-else-if="error">后端连接失败：{{ error }}</span>
        <span v-else>正在检查后端连接…</span>
      </div>
    </section>
  </main>
</template>
