<script setup lang="ts">
import { onMounted, ref } from "vue";
import { listCompanies } from "@/api/companies";
import { listDepartments } from "@/api/departments";
import type { Company, Department } from "@/types/api";
import ErrorBanner from "@/components/Ui/ErrorBanner.vue";
import LoadingSpinner from "@/components/Ui/LoadingSpinner.vue";

const companies = ref<Company[]>([]);
const departments = ref<Department[]>([]);
const companyId = ref<number | null>(null);

const loading = ref(false);
const error = ref<string | null>(null);

async function loadCompanies() {
  companies.value = await listCompanies();
}

async function loadDepartments() {
  loading.value = true;
  error.value = null;
  try {
    departments.value = await listDepartments(companyId.value ?? undefined);
  } catch (e: any) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
}

onMounted(async () => {
  await loadCompanies();
  await loadDepartments();
});
</script>

<template>
  <h2>Departments</h2>
  <ErrorBanner :error="error" />

  <div class="row">
    <label>Company</label>
    <select v-model="companyId" @change="loadDepartments">
      <option :value="null">All</option>
      <option v-for="c in companies" :key="c.id" :value="c.id">
        {{ c.name }}
      </option>
    </select>
  </div>

  <LoadingSpinner v-if="loading" />

  <table class="table" v-if="departments.length">
    <thead>
      <tr>
        <th>Company</th>
        <th>Department</th>
        <th>Employees</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="d in departments" :key="d.id">
        <td>{{ companies.find(c => c.id === d.company)?.name ?? d.company }}</td>
        <td>{{ d.name }}</td>
        <td>{{ d.employee_count }}</td>
      </tr>
    </tbody>
  </table>

  <div v-else-if="!loading" class="muted">No departments.</div>
</template>

<style scoped>
.row { display:flex; gap:10px; align-items:center; margin: 12px 0; }
</style>
