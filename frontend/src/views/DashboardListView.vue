<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { listCompanies } from '@/api/companies';
import { listEmployees } from '@/api/employees';
import LoadingSpinner from "@/components/Ui/LoadingSpinner.vue";

const stats = ref({ companies: 0, employees: 0 });
const loading = ref(true);

onMounted(async () => {
  try {
    const [cos, emps] = await Promise.all([listCompanies(), listEmployees()]);
    stats.value = { 
      companies: cos.length, 
      employees: emps.length 
    };
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div class="container">
    <h2>Organization Overview</h2>
    <LoadingSpinner v-if="loading" />
    <div v-else class="stats-grid">
      <div class="stat-card">
        <div class="icon">🏢</div>
        <h3>Companies</h3>
        <p class="count">{{ stats.companies }}</p>
      </div>
      <div class="stat-card">
        <div class="icon">👥</div>
        <h3>Employees</h3>
        <p class="count">{{ stats.employees }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 20px; margin-top: 20px; }
.stat-card { background: white; padding: 30px; border-radius: 12px; border: 1px solid #eee; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
.count { font-size: 3rem; font-weight: 800; color: #42b883; margin: 10px 0 0; }
.icon { font-size: 2rem; }
</style>