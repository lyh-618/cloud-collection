<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'

type Content = { title: string; description: string; cover_url: string; external_url: string | null; author: string; tags: string[]; like_count: number; favorite_count: number; view_count: number }
const route = useRoute()
const content = ref<Content | null>(null)
const error = ref('')
onMounted(async () => {
  try { const response = await fetch(`/api/contents/${route.params.id}`); if (!response.ok) throw new Error('内容不存在'); content.value = await response.json() as Content } catch (requestError) { error.value = requestError instanceof Error ? requestError.message : '请求失败' }
})
</script>

<template><section class="detail-shell"><RouterLink class="back-link" to="/">← 返回首页</RouterLink><p v-if="error" class="empty-state">{{ error }}</p><div v-else-if="content" class="detail-card"><img :src="content.cover_url" :alt="content.title" /><div><p class="eyebrow">CONTENT DETAIL</p><h1>{{ content.title }}</h1><div class="tag-row"><span v-for="tag in content.tags" :key="tag">#{{ tag }}</span></div><p class="detail-description">{{ content.description }}</p><p class="detail-meta">作者：{{ content.author }}　{{ content.like_count }} 赞　{{ content.favorite_count }} 收藏　{{ content.view_count }} 浏览</p><button class="collect-button" type="button">加入收藏 <span>＋</span></button></div></div><p v-else class="empty-state">正在加载内容…</p></section></template>
