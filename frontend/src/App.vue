<script setup lang="ts">
import { onMounted, ref } from 'vue'

type HealthResponse = { status: string; service: string }
type Pet = {
  id: number
  name: string
  attribute: string
  rarity: string
  description: string
  emoji: string
}

const health = ref<HealthResponse | null>(null)
const error = ref('')
const pets = ref<Pet[]>([])
const loadingPets = ref(true)

onMounted(async () => {
  try {
    const [healthResponse, petsResponse] = await Promise.all([
      fetch('/api/health'),
      fetch('/api/pets'),
    ])
    if (!healthResponse.ok || !petsResponse.ok) throw new Error('API 请求失败')
    health.value = await healthResponse.json() as HealthResponse
    pets.value = await petsResponse.json() as Pet[]
  } catch (requestError) {
    error.value = requestError instanceof Error ? requestError.message : '请求失败'
  } finally {
    loadingPets.value = false
  }
})
</script>

<template>
  <main class="page-shell">
    <section class="hero-card">
      <div class="hero-copy">
        <p class="eyebrow">CLOUD COLLECTION · POKEDEX</p>
        <h1>洛克王国<br /><span>宠物图鉴</span></h1>
        <p class="intro">收集每一次相遇，记录属于你的宠物故事。</p>
        <div class="status" :class="{ online: health, offline: error }">
          <span class="dot" />
          <span v-if="health">后端已连接</span>
          <span v-else-if="error">后端连接失败：{{ error }}</span>
          <span v-else>正在检查后端连接…</span>
        </div>
      </div>
      <div class="hero-orb">✦</div>
    </section>

    <section class="catalogue-section">
      <div class="section-heading">
        <div>
          <p class="eyebrow">MY CATALOGUE</p>
          <h2>宠物收藏</h2>
        </div>
        <span class="count-badge">{{ pets.length }} 只宠物</span>
      </div>
      <p v-if="loadingPets" class="empty-state">正在加载图鉴…</p>
      <p v-else-if="error" class="empty-state">暂时无法加载图鉴，请确认后端已启动。</p>
      <div v-else class="pet-grid">
        <article v-for="pet in pets" :key="pet.id" class="pet-card">
          <div class="pet-emoji">{{ pet.emoji }}</div>
          <div class="pet-card-body">
            <div class="pet-meta"><span>{{ pet.attribute }}</span><span>{{ pet.rarity }}</span></div>
            <h3>{{ pet.name }}</h3>
            <p>{{ pet.description }}</p>
            <button type="button" class="collect-button">加入收藏 <span>＋</span></button>
          </div>
        </article>
      </div>
    </section>
  </main>
</template>
