<script setup lang="ts">
import { onMounted, ref } from 'vue'

type HealthResponse = { status: string; service: string }
type Recommendation = {
  id: number
  category: string
  title: string
  subtitle: string
  description: string
  accent: string
}

const health = ref<HealthResponse | null>(null)
const error = ref('')
const recommendations = ref<Recommendation[]>([])
const loadingRecommendations = ref(true)
const entered = ref(false)

onMounted(async () => {
  try {
    const [healthResponse, recommendationsResponse] = await Promise.all([
      fetch('/api/health'),
      fetch('/api/recommendations'),
    ])
    if (!healthResponse.ok || !recommendationsResponse.ok) throw new Error('API 请求失败')
    health.value = await healthResponse.json() as HealthResponse
    recommendations.value = await recommendationsResponse.json() as Recommendation[]
  } catch (requestError) {
    error.value = requestError instanceof Error ? requestError.message : '请求失败'
  } finally {
    loadingRecommendations.value = false
  }
})
</script>

<template>
  <main v-if="!entered" class="cover-page">
    <div class="cover-backdrop" />
    <div class="cover-overlay" />
    <section class="cover-content">
      <p class="eyebrow">JINGYI FAN COLLECTION</p>
      <h1>鞠婧祎<br /><span>安利收藏馆</span></h1>
      <p>收藏舞台、作品和每一个值得回看的瞬间。</p>
      <button type="button" class="enter-button" @click="entered = true">进入收藏馆 <span>→</span></button>
    </section>
    <p class="cover-credit">A SMALL FAN-MADE ARCHIVE · 2026</p>
  </main>
  <main v-else class="page-shell">
    <nav class="top-nav">
      <div class="brand-mark"><span>JY</span> 安利收藏馆</div>
      <div class="nav-links"><a href="#home">首页</a><a href="#film">影视</a><a href="#dance">舞蹈</a><a href="#image">图片</a><a href="#song">歌曲</a><a href="#fanwork">二创</a></div>
    </nav>
    <section class="hero-card" id="home">
      <div class="hero-copy">
        <p class="eyebrow">JINGYI FAN COLLECTION · 01</p>
        <h1>把喜欢的光<br /><span>好好收藏</span></h1>
        <p class="intro">这是一个关于鞠婧祎的安利空间，收集作品、舞台和那些让人心动的瞬间。</p>
        <div class="status" :class="{ online: health, offline: error }">
          <span class="dot" />
          <span v-if="health">后端已连接</span>
          <span v-else-if="error">后端连接失败：{{ error }}</span>
          <span v-else>正在检查后端连接…</span>
        </div>
      </div>
      <img class="hero-portrait" src="/assets/portrait-film.jpg" alt="蓝色胶片风格人物照片" />
    </section>

    <section class="catalogue-section" id="guide">
      <div class="section-heading">
        <div>
          <p class="eyebrow">START HERE</p>
          <h2>三条入坑路线</h2>
        </div>
        <span class="count-badge">{{ recommendations.length }} 个推荐</span>
      </div>
      <p v-if="loadingRecommendations" class="empty-state">正在加载安利内容…</p>
      <p v-else-if="error" class="empty-state">暂时无法加载内容，请确认后端已启动。</p>
      <div v-else class="recommendation-grid">
        <article v-for="item in recommendations" :key="item.id" class="recommendation-card">
          <div class="card-number">{{ item.accent }}</div>
          <div class="card-content">
            <p class="card-category">{{ item.category }}</p>
            <h3>{{ item.title }}</h3>
            <p class="card-subtitle">{{ item.subtitle }}</p>
            <p class="card-description">{{ item.description }}</p>
            <button type="button" class="collect-button">查看推荐 <span>↗</span></button>
          </div>
        </article>
      </div>
    </section>
    <section class="feature-strip" id="film">
      <div class="feature-copy"><p class="eyebrow">FEATURED STORY</p><h2>从一帧画面开始认识她</h2><p>把喜欢的作品、舞台和图片放在同一个有温度的空间里，慢慢搭建属于你的安利档案。</p></div>
      <img src="/assets/illustration.png" alt="彩色插画风格人物头像" />
    </section>
    <div class="anchor-note" id="dance">舞蹈 · <span id="image">图片</span> · <span id="song">歌曲</span> · <span id="fanwork">二创</span> 页面将在下一阶段逐步展开。</div>
    <section class="notes-section" id="notes">
      <p class="eyebrow">A SMALL NOTE</p>
      <p>喜欢不需要标准答案。这里先放下第一张小小的推荐卡，之后一起把它变成更完整的作品档案和收藏手记。</p>
    </section>
  </main>
</template>
