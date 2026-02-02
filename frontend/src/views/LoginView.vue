<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import ErrorBanner from "@/components/Ui/ErrorBanner.vue";

const auth = useAuthStore();
const router = useRouter();

const email = ref("");
const password = ref("");
const loading = ref(false);
const error = ref<string | null>(null);

async function submit() {
  loading.value = true;
  error.value = null;
  try {
    await auth.login(email.value, password.value);
    router.push({ name: "companies" });
  } catch (e: any) {
    error.value = e?.message ?? "Login failed";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="card">
    <h2>Login</h2>
    <ErrorBanner :error="error" />

    <form @submit.prevent="submit" class="form">
      <label>Email</label>
      <input v-model="email" type="email" required />

      <label>Password</label>
      <input v-model="password" type="password" required />

      <button class="btn" :disabled="loading" type="submit">
        {{ loading ? "Signing in..." : "Sign in" }}
      </button>
    </form>
  </div>
</template>

<style scoped>
.card { max-width: 420px; margin: 48px auto; padding: 16px; border: 1px solid #ddd; border-radius: 10px; }
.form { display: grid; gap: 10px; }
</style>
