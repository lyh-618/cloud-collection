<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, RouterView } from 'vue-router'

const entered = ref(false)
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
      <RouterLink class="brand-mark" to="/"><span>JY</span> 安利收藏馆</RouterLink>
      <div class="nav-links">
        <RouterLink to="/">首页</RouterLink><RouterLink to="/film">影视</RouterLink><RouterLink to="/dance">舞蹈</RouterLink><RouterLink to="/image">图片</RouterLink><RouterLink to="/song">歌曲</RouterLink><RouterLink to="/fanwork">二创</RouterLink>
      </div>
      <button class="profile-placeholder" type="button" title="个人中心将在后续阶段开放">我的</button>
    </nav>
    <RouterView />
  </main>
</template>
