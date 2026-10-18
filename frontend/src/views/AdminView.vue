<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { apiFetch } from '../auth'
type Content = { id: number; title: string; description: string; author: string; type: string }
const items = ref<Content[]>([]); const error = ref('')
async function load() { const response = await apiFetch('/api/admin/pending'); const data = await response.json(); if (!response.ok) { error.value = data.detail || '无权限'; return } items.value = data }
async function review(id: number, approved: boolean) { await apiFetch(`/api/admin/contents/${id}/review?approved=${approved}${approved ? '' : '&reason=请补充清晰的作品来源'}`, { method: 'POST' }); await load() }
onMounted(load)
</script>
<template><section class="admin-shell"><p class="eyebrow">EDITORIAL DESK</p><h1>待审核内容</h1><p v-if="error" class="form-error">{{ error }}</p><p v-else-if="!items.length" class="empty-state">当前没有待审核内容。</p><div v-else class="admin-list"><article v-for="item in items" :key="item.id"><div><small>{{ item.type }} · {{ item.author }}</small><h3>{{ item.title }}</h3><p>{{ item.description }}</p></div><div><button type="button" @click="review(item.id, true)">通过</button><button type="button" class="reject-button" @click="review(item.id, false)">退回</button></div></article></div></section></template>
