<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const category = computed(() => ({
  film: { name: '影视', label: 'SCREEN STORIES', text: '收藏角色、作品与值得反复回看的片段。' },
  dance: { name: '舞蹈', label: 'STAGE MOMENTS', text: '记录舞台上的动作、音乐和闪光瞬间。' },
  image: { name: '图片', label: 'VISUAL NOTES', text: '把喜欢的画面整理成一册专属视觉手记。' },
  song: { name: '歌曲', label: 'MUSIC CORNER', text: '从旋律开始，收藏每一首想单曲循环的歌。' },
  fanwork: { name: '二创', label: 'FAN CREATIONS', text: '发现并分享来自粉丝的想象与表达。' },
}[route.params.category as string] ?? { name: '分类', label: 'COMING SOON', text: '这个分类正在准备中。' }))
</script>

<template><section class="category-shell"><p class="eyebrow">{{ category.label }}</p><h1>{{ category.name }}</h1><p>{{ category.text }}</p><div class="category-placeholder"><span>✦</span><strong>内容展区即将开放</strong><small>阶段 1 先完成页面骨架，下一阶段接入内容列表和详情。</small></div></section></template>
