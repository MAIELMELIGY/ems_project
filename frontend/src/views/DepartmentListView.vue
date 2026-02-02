<script setup lang="ts">
import { onMounted, ref } from "vue";
import { listCompanies } from "@/api/companies";
import { listDepartments, createDepartment, deleteDepartment } from "@/api/departments";
import type { Company, Department } from "@/types/api";
import { useAuthStore } from "@/stores/auth";
import ErrorBanner from "@/components/Ui/ErrorBanner.vue";
import LoadingSpinner from "@/components/Ui/LoadingSpinner.vue";

const auth = useAuthStore();

const companies = ref<Company[]>([]);
const departments = ref<Department[]>([]);
const companyId = ref<number | null>(null);

const loading = ref(false);
const error = ref<string | null>(null);

// Form state for adding a new department
const newName = ref("");
const selectedCompanyForNew = ref<number | null>(null);

async function loadCompanies() {
  try {
    companies.value = await listCompanies();
  } catch (e: any) {
    error.value = e.message;
  }
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

async function add() {
  if (!newName.value.trim() || !selectedCompanyForNew.value) return;
  loading.value = true;
  error.value = null;
  try {
    await createDepartment({ 
      name: newName.value.trim(), 
      company: selectedCompanyForNew.value 
    });
    newName.value = "";
    await loadDepartments();
  } catch (e: any) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
}

async function remove(id: number) {
  if (!confirm("Delete this department?")) return;
  loading.value = true;
  error.value = null;
  try {
    await deleteDepartment(id);
    await loadDepartments();
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
  <div class="row space">
    <h2>Departments</h2>
  </div>

  <ErrorBanner :error="error" />

  <div v-if="auth.canWrite" class="add-section card">
    <h3>Add New Department</h3>
    <div class="row">
      <select v-model="selectedCompanyForNew">
        <option :value="null" disabled>Select Company</option>
        <option v-for="c in companies" :key="c.id" :value="c.id">{{ c.name }}</option>
      </select>
      <input v-model="newName" placeholder="Department name" />
      <button class="btn" @click="add" :disabled="!newName || !selectedCompanyForNew">Add</button>
    </div>
  </div>

  <div class="row filter-section">
    <label>Filter by Company:</label>
    <select v-model="companyId" @change="loadDepartments">
      <option :value="null">All Companies</option>
      <option v-for="c in companies" :key="c.id" :value="c.id">{{ c.name }}</option>
    </select>
  </div>

  <LoadingSpinner v-if="loading" />

  <table class="table" v-if="departments.length">
    <thead>
      <tr>
        <th>Company</th>
        <th>Department</th>
        <th>Employees</th>
        <th v-if="auth.canWrite"></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="d in departments" :key="d.id">
        <td>{{ companies.find(c => c.id === d.company)?.name ?? d.company }}</td>
        <td>
          <RouterLink :to="`/departments/${d.id}`">{{ d.name }}</RouterLink>
        </td>
        <td>{{ d.employee_count }}</td>
        <td v-if="auth.canWrite" class="right">
          <button class="btn danger" @click="remove(d.id)">Delete</button>
        </td>
      </tr>
    </tbody>
  </table>

  <div v-else-if="!loading" class="muted">No departments found.</div>
</template>

<style scoped>
.row { display: flex; gap: 10px; align-items: center; margin: 12px 0; }
.space { justify-content: space-between; }
.add-section { margin-bottom: 24px; padding: 15px; background: #f4f4f4; border-radius: 8px; }
.filter-section { border-top: 1px solid #eee; padding-top: 12px; }
.right { text-align: right; }
.card { border: 1px solid #ddd; }
</style>