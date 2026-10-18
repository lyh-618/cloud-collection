import { ref } from 'vue'

export const token = ref(localStorage.getItem('cc_token') || '')
export const currentUser = ref<{ id: number; username: string; is_admin: boolean } | null>(null)

export async function apiFetch(input: RequestInfo | URL, init: RequestInit = {}) {
  const headers = new Headers(init.headers)
  if (token.value) headers.set('Authorization', `Bearer ${token.value}`)
  if (init.body && !headers.has('Content-Type')) headers.set('Content-Type', 'application/json')
  return fetch(input, { ...init, headers })
}

export async function login(username: string, password: string) {
  const response = await fetch('/api/auth/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ username, password }) })
  const data = await response.json()
  if (!response.ok) throw new Error(data.detail || '登录失败')
  token.value = data.token; currentUser.value = data.user; localStorage.setItem('cc_token', data.token)
}

export async function register(username: string, password: string, confirm_password: string) {
  const response = await fetch('/api/auth/register', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ username, password, confirm_password }) })
  const data = await response.json()
  if (!response.ok) throw new Error(data.detail || '注册失败')
  token.value = data.token; currentUser.value = data.user; localStorage.setItem('cc_token', data.token)
}

export function logout() { token.value = ''; currentUser.value = null; localStorage.removeItem('cc_token') }
