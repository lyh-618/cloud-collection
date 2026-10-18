<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login, register } from '../auth'
const router = useRouter(); const mode = ref<'login' | 'register'>('login'); const username = ref(''); const password = ref(''); const confirm = ref(''); const error = ref(''); const busy = ref(false)
async function submit() { error.value = ''; busy.value = true; try { if (mode.value === 'login') await login(username.value, password.value); else await register(username.value, password.value, confirm.value); await router.push('/') } catch (e) { error.value = e instanceof Error ? e.message : '操作失败' } finally { busy.value = false } }
</script>
<template><section class="auth-shell"><p class="eyebrow">MEMBER SPACE</p><h1>{{ mode === 'login' ? '欢迎回来' : '加入收藏馆' }}</h1><p>登录后可以点赞、收藏和发布安利内容。</p><form class="auth-form" @submit.prevent="submit"><input v-model="username" minlength="3" maxlength="20" placeholder="用户名" required /><input v-model="password" type="password" minlength="8" placeholder="密码（至少 8 位）" required /><input v-if="mode === 'register'" v-model="confirm" type="password" minlength="8" placeholder="确认密码" required /><p v-if="error" class="form-error">{{ error }}</p><button type="submit" :disabled="busy">{{ busy ? '处理中…' : mode === 'login' ? '登录' : '注册' }}</button></form><button class="text-button" type="button" @click="mode = mode === 'login' ? 'register' : 'login'">{{ mode === 'login' ? '还没有账号？立即注册' : '已有账号？返回登录' }}</button></section></template>
