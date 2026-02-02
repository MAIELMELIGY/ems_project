<script setup lang="ts">
import { onMounted, ref, computed } from "vue";
import { getHiredReport } from "@/api/employees";
import { listCompanies } from "@/api/companies";
import { listDepartments } from "@/api/departments";
import type { Employee, Company, Department } from "@/types/api";
import LoadingSpinner from "@/components/Ui/LoadingSpinner.vue";
import ErrorBanner from "@/components/Ui/ErrorBanner.vue";

const employees = ref<Employee[]>([]);
const companies = ref<Company[]>([]);
const departments = ref<Department[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);

async function loadData() {
  loading.value = true;
  try {
    const [empData, coData, depData] = await Promise.all([
      getHiredReport('hired'),
      listCompanies(),
      listDepartments()
    ]);
    employees.value = empData;
    companies.value = coData;
    departments.value = depData;
  } catch (e: any) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
}


const getCompanyName = (id: number) => companies.value.find(c => c.id === id)?.name || 'N/A';
const getDeptName = (id: number) => departments.value.find(d => d.id === id)?.name || 'N/A';

onMounted(loadData);
</script>

<template>
  <div class="container">
    <div class="header-row">
      <h2>Hired Employees Report</h2>
      <button class="btn" @click="loadData">Refresh Report</button>
    </div>

    <ErrorBanner :error="error" />
    <LoadingSpinner v-if="loading" />

    <div v-if="!loading && employees.length" class="table-container">
      <table class="table report-table">
        <thead>
          <tr>
            <th>Employee Name</th>
            <th>Email</th>
            <th>Mobile</th>
            <th>Position</th>
            <th>Hired On</th>
            <th>Days Employed</th>
            <th>Company</th>
            <th>Department</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="emp in employees" :key="emp.id">
            <td><strong>{{ emp.name }}</strong></td>
            <td>{{ emp.email }}</td>
            <td>{{ emp.mobile_number }}</td>
            <td>{{ emp.designation }}</td>
            <td>{{ emp.hired_on || '-' }}</td>
            <td><span class="badge">{{ emp.days_employed }} days</span></td>
            <td>{{ getCompanyName(emp.company) }}</td>
            <td>{{ getDeptName(emp.department) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else-if="!loading" class="muted">
      No hired employees found to generate report.
    </div>
  </div>
</template>

<style scoped>
.report-table { width: 100%; border-collapse: collapse; margin-top: 20px; }
.report-table th { background: #f8f9fa; text-align: left; padding: 12px; border-bottom: 2px solid #dee2e6; }
.report-table td { padding: 12px; border-bottom: 1px solid #eee; }
.badge { background: #e8f5e9; color: #2e7d32; padding: 2px 8px; border-radius: 12px; font-size: 0.85rem; }
.header-row { display: flex; justify-content: space-between; align-items: center; }
.table-container { overflow-x: auto; }
</style>