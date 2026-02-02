<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { getCompany } from "@/api/companies";
import { listDepartments } from "@/api/departments";
import type { Company, Department } from "@/types/api";
import ErrorBanner from "@/components/Ui/ErrorBanner.vue";
import LoadingSpinner from "@/components/Ui/LoadingSpinner.vue";

const route = useRoute();
const id = computed(() => Number(route.params.id));

const company = ref<Company | null>(null);
const departments = ref<Department[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);

async function load() {
  loading.value = true;
  error.value = null;
  try {
    company.value = await getCompany(id.value);
    departments.value = await listDepartments(id.value);
  } catch (e: any) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
}

onMounted(load);
</script>

<template>
  <h2>Company Detail</h2>
  <ErrorBanner :error="error" />
  <LoadingSpinner v-if="loading" />

  <div v-if="company" class="card">
    <div><b>Name:</b> {{ company.name }}</div>
    <div><b>Departments:</b> {{ company.department_count }}</div>
    <div><b>Employees:</b> {{ company.employee_count }}</div>
  </div>

  <h3>Departments</h3>
  <table class="table" v-if="departments.length">
    <thead>
      <tr>
        <th>Name</th>
        <th>Employees</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="d in departments" :key="d.id">
        <td>{{ d.name }}</td>
        <td>{{ d.employee_count }}</td>
      </tr>
    </tbody>
  </table>

  <div v-else-if="!loading" class="muted">No departments.</div>
</template>

<style scoped>
.card { padding: 12px; border: 1px solid #ddd; border-radius: 10px; margin: 12px 0; }
</style>
