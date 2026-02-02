<script setup lang="ts">
import { computed } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useRouter, useRoute } from "vue-router";

const auth = useAuthStore();
const router = useRouter();
const route = useRoute();

const showNav = computed(() => auth.isAuthed && route.name !== "login");

function logout() {
  auth.clear();
  router.push({ name: "login" });
}
</script>

<template>
  <div class="shell">
    <header class="topbar">
      <div class="brand">EMS</div>
      <nav v-if="showNav" class="nav">
        <RouterLink to="/dashboard">Dashboard</RouterLink>
        <RouterLink to="/companies">Companies</RouterLink>
        <RouterLink to="/departments">Departments</RouterLink>
        <RouterLink to="/employees">Employees</RouterLink>
        <RouterLink to="/reports/employees">Hired Report</RouterLink>
      </nav>

      <div class="right">
        <span v-if="auth.email" class="muted">{{ auth.email }} ({{ auth.role }})</span>
        <button v-if="showNav" class="btn" @click="logout">Logout</button>
      </div>
    </header>

    <main class="content">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.shell { min-height: 100vh; display: flex; flex-direction: column; }
.topbar { display:flex; gap:16px; align-items:center; padding:12px 16px; border-bottom:1px solid #ddd; }
.brand { font-weight:700; }
.nav { display:flex; gap:12px; }
.nav a.router-link-active { font-weight:600; text-decoration: underline; }
.right { margin-left:auto; display:flex; gap:12px; align-items:center; }
.content { padding: 16px; }
</style>
