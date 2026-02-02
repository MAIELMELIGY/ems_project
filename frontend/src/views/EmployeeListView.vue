<script setup lang="ts">
import { onMounted, ref } from "vue";
import { listEmployees, deleteEmployee } from "@/api/employees";
import { listCompanies } from "@/api/companies";
import { listDepartments } from "@/api/departments";
import type { Company, Department, Employee, EmployeeStatus } from "@/types/api";
import { useAuthStore } from "@/stores/auth";
import ErrorBanner from "@/components/Ui/ErrorBanner.vue";
import LoadingSpinner from "@/components/Ui/LoadingSpinner.vue";

const auth = useAuthStore();

const employees = ref<Employee[]>([]);
const companies = ref<Company[]>([]);
const departments = ref<Department[]>([]);

const filterCompany = ref<number | null>(null);
const filterDepartment = ref<number | null>(null);
const filterStatus = ref<EmployeeStatus | "">("");

const loading = ref(false);
const error = ref<string | null>(null);

async function loadMeta() {
  companies.value = await listCompanies();
}

async function loadDepartmentsForCompany() {
  filterDepartment.value = null;
  if (!filterCompany.value) {
    departments.value = [];
    return;
  }
  departments.value = await listDepartments(filterCompany.value);
}

async function load() {
  loading.value = true;
  error.value = null;
  try {
    employees.value = await listEmployees({
      company: filterCompany.value ?? undefined,
      department: filterDepartment.value ?? undefined,
      status: filterStatus.value || undefined,
    });
  } catch (e: any) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
}

async function remove(id: number) {
  if (!confirm("Delete this employee?")) return;
  loading.value = true;
  error.value = null;
  try {
    await deleteEmployee(id);
    await load();
  } catch (e: any) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
}

function companyName(id: number) {
  return companies.value.find((c) => c.id === id)?.name ?? String(id);
}
function deptName(id: number) {
  return departments.value.find((d) => d.id === id)?.name ?? String(id);
}

onMounted(async () => {
  await loadMeta();
  await load();
});
</script>

<template>
  <div class="row space">
    <h2>Employees</h2>
    <RouterLink v-if="auth.canWrite" class="btn" to="/employees/new">+ New</RouterLink>
  </div>

  <ErrorBanner :error="error" />

  <div class="filters">
    <div>
      <label>Company</label>
      <select v-model="filterCompany" @change="loadDepartmentsForCompany(); load()">
        <option :value="null">All</option>
        <option v-for="c in companies" :key="c.id" :value="c.id">{{ c.name }}</option>
      </select>
    </div>

    <div>
      <label>Department</label>
      <select v-model="filterDepartment" @change="load" :disabled="!filterCompany">
        <option :value="null">All</option>
        <option v-for="d in departments" :key="d.id" :value="d.id">{{ d.name }}</option>
      </select>
    </div>

    <div>
      <label>Status</label>
      <select v-model="filterStatus" @change="load">
        <option value="">All</option>
        <option value="application_received">Application Received</option>
        <option value="interview_scheduled">Interview Scheduled</option>
        <option value="hired">Hired</option>
        <option value="not_accepted">Not Accepted</option>
      </select>
    </div>
  </div>

  <LoadingSpinner v-if="loading" />

  <table class="table" v-if="employees.length">
    <thead>
      <tr>
        <th>Name</th>
        <th>Company</th>
        <th>Department</th>
        <th>Status</th>
        <th>Days employed</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="e in employees" :key="e.id">
        <td><RouterLink :to="`/employees/${e.id}`">{{ e.name }}</RouterLink></td>
        <td>{{ companyName(e.company) }}</td>
        <td>{{ filterCompany ? deptName(e.department) : e.department }}</td>
        <td>{{ e.status }}</td>
        <td>{{ e.days_employed ?? "-" }}</td>
        <td class="right">
          <RouterLink class="btn" :to="`/employees/${e.id}`">View</RouterLink>
          <RouterLink v-if="auth.canWrite" class="btn" :to="`/employees/${e.id}/edit`">Edit</RouterLink>
          <button v-if="auth.canWrite" class="btn danger" @click="remove(e.id)">Delete</button>
        </td>
      </tr>
    </tbody>
  </table>

  <div v-else-if="!loading" class="muted">No employees.</div>
</template>

<style scoped>
.row { display:flex; align-items:center; gap:12px; }
.space { justify-content: space-between; }
.filters { display:flex; gap:12px; flex-wrap:wrap; margin: 12px 0; }
.filters > div { display:grid; gap:6px; }
.right { text-align:right; white-space:nowrap; }
</style>
