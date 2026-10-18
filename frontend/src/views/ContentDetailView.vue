<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { apiFetch, token } from '../auth'

type Content = { id: number; title: string; description: string; cover_url: string; external_url: string | null; author: string; tags: string[]; like_count: number; favorite_count: number; view_count: number; liked?: boolean; favorited?: boolean }
type Comment = { id: number; username: string; body: string; created_at: string }
const route = useRoute()
const content = ref<Content | null>(null)
const error = ref('')
const comments = ref<Comment[]>([]); const commentBody = ref('')
onMounted(async () => {
  try { const response = await apiFetch(`/api/contents/${route.params.id}`); if (!response.ok) throw new Error('内容不存在'); content.value = await response.json() as Content; const commentsResponse = await fetch(`/api/contents/${route.params.id}/comments`); if (commentsResponse.ok) comments.value = await commentsResponse.json() as Comment[] } catch (requestError) { error.value = requestError instanceof Error ? requestError.message : '请求失败' }
})
async function toggle(action: 'like' | 'favorite') { if (!token.value) { window.alert('请先登录后再互动'); return } const response = await apiFetch(`/api/contents/${route.params.id}/${action}`, { method: 'POST' }); if (!response.ok || !content.value) return; const data = await response.json(); if (action === 'like') { content.value.like_count = data.like_count; content.value.liked = data.liked } else { content.value.favorite_count = data.favorite_count; content.value.favorited = data.favorited } }
async function addComment() { if (!commentBody.value.trim()) return; if (!token.value) { window.alert('请先登录后发表评论'); return } const response = await apiFetch(`/api/contents/${route.params.id}/comments`, { method: 'POST', body: JSON.stringify({ body: commentBody.value }) }); if (!response.ok) return; comments.value.push(await response.json() as Comment); commentBody.value = '' }
</script>

<template><section class="detail-shell"><RouterLink class="back-link" to="/">← 返回首页</RouterLink><p v-if="error" class="empty-state">{{ error }}</p><div v-else-if="content" class="detail-card"><img :src="content.cover_url" :alt="content.title" /><div><p class="eyebrow">CONTENT DETAIL</p><h1>{{ content.title }}</h1><div class="tag-row"><span v-for="tag in content.tags" :key="tag">#{{ tag }}</span></div><p class="detail-description">{{ content.description }}</p><p class="detail-meta">作者：{{ content.author }}　{{ content.like_count }} 赞　{{ content.favorite_count }} 收藏　{{ content.view_count }} 浏览</p><div class="detail-actions"><button class="collect-button" type="button" @click="toggle('like')">♥ {{ content.like_count }}</button><button class="collect-button" type="button" @click="toggle('favorite')">☆ {{ content.favorite_count }}</button><a v-if="content.external_url" class="collect-button" :href="content.external_url" target="_blank" rel="noreferrer">打开原链接 ↗</a></div><div class="comments"><h2>评论</h2><form @submit.prevent="addComment"><input v-model="commentBody" placeholder="写下你的想法" /><button type="submit">发送</button></form><p v-if="!comments.length" class="empty-state">还没有评论，来留下第一条吧。</p><div v-for="comment in comments" :key="comment.id" class="comment"><strong>{{ comment.username }}</strong><span>{{ comment.body }}</span></div></div></div></div><p v-else class="empty-state">正在加载内容…</p></section></template>
