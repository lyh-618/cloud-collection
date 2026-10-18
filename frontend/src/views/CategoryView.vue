<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'

type Content = { id: number; type: string; title: string; description: string; cover_url: string; external_url: string | null; author: string; tags: string[]; like_count: number; favorite_count: number; view_count: number }
const route = useRoute()
const category = computed(() => ({
  film: { name: '影视', label: 'SCREEN STORIES', text: '收藏角色、作品与值得反复回看的片段。' },
  dance: { name: '舞蹈', label: 'STAGE MOMENTS', text: '记录舞台上的动作、音乐和闪光瞬间。' },
  image: { name: '图片', label: 'VISUAL NOTES', text: '把喜欢的画面整理成一册专属视觉手记。' },
  song: { name: '歌曲', label: 'MUSIC CORNER', text: '从旋律开始，收藏每一首想单曲循环的歌。' },
  fanwork: { name: '二创', label: 'FAN CREATIONS', text: '发现并分享来自粉丝的想象与表达。' },
}[route.params.category as string] ?? { name: '分类', label: 'COMING SOON', text: '这个分类正在准备中。' }))
const contents = ref<Content[]>([])
const keyword = ref('')
const sort = ref('latest')
const loading = ref(true)
const error = ref('')

async function loadContents() {
  loading.value = true
  try {
    const params = new URLSearchParams({ type: String(route.params.category), sort: sort.value })
    if (keyword.value.trim()) params.set('keyword', keyword.value.trim())
    const response = await fetch(`/api/contents?${params}`)
    if (!response.ok) throw new Error('内容加载失败')
    contents.value = await response.json() as Content[]
    error.value = ''
  } catch (requestError) {
    error.value = requestError instanceof Error ? requestError.message : '请求失败'
  } finally { loading.value = false }
}

onMounted(loadContents)
</script>

<template>
  <section class="category-shell">
    <p class="eyebrow">{{ category.label }}</p>
    <h1>{{ category.name }}</h1>
    <p>{{ category.text }}</p>
    <div class="content-toolbar"><input v-model="keyword" placeholder="搜索标题或标签" @keyup.enter="loadContents" /><select v-model="sort" @change="loadContents"><option value="latest">最新发布</option><option value="popular">最多点赞</option></select><button type="button" @click="loadContents">搜索</button></div>
    <p v-if="loading" class="empty-state">正在加载内容…</p>
    <p v-else-if="error" class="empty-state">{{ error }}</p>
    <p v-else-if="!contents.length" class="empty-state">还没有匹配的内容。</p>
    <div v-else class="content-grid"><article v-for="item in contents" :key="item.id" class="content-card"><img :src="item.cover_url" :alt="item.title" /><div class="content-card-body"><div class="tag-row"><span v-for="tag in item.tags" :key="tag">#{{ tag }}</span></div><h3>{{ item.title }}</h3><p>{{ item.description }}</p><small>{{ item.author }} · {{ item.like_count }} 赞 · {{ item.view_count }} 次浏览</small><RouterLink class="detail-link" :to="`/content/${item.id}`">查看详情 →</RouterLink></div></article></div>
  </section>
</template>
