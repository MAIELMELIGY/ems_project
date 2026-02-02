<script setup lang="ts">
import { onMounted, ref } from "vue";
import { listCompanies, createCompany, deleteCompany } from "@/api/companies";
import type { Company } from "@/types/api";
import { useAuthStore } from "@/stores/auth";
import ErrorBanner from "@/components/Ui/ErrorBanner.vue";
import LoadingSpinner from "@/components/Ui/LoadingSpinner.vue";

const auth = useAuthStore();

const items = ref<Company[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);

const newName = ref("");

async function load() {
  loading.value = true;
  error.value = null;
  try {
    items.value = await listCompanies();
  } catch (e: any) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
}

async function add() {
  if (!newName.value.trim()) return;
  loading.value = true;
  error.value = null;
  try {
    await createCompany({ name: newName.value.trim() });
    newName.value = "";
    await load();
  } catch (e: any) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
}

async function remove(id: number) {
  if (!confirm("Delete this company?")) return;
  loading.value = true;
  error.value = null;
  try {
    await deleteCompany(id);
    await load();
  } catch (e: any) {
    error.value = e.message; // will show PROTECT errors too
  } finally {
    loading.value = false;
  }
}

onMounted(load);
</script>

<template>
  <h2>Companies</h2>
  <ErrorBanner :error="error" />
  <LoadingSpinner v-if="loading" />

  <div v-if="auth.canWrite" class="row">
    <input v-model="newName" placeholder="New company name" />
    <button class="btn" @click="add">Add</button>
  </div>

  <table class="table" v-if="items.length">
    <thead>
      <tr>
        <th>Name</th>
        <th>Departments</th>
        <th>Employees</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="c in items" :key="c.id">
        <td>
          <RouterLink :to="`/companies/${c.id}`">{{ c.name }}</RouterLink>
        </td>
        <td>{{ c.department_count }}</td>
        <td>{{ c.employee_count }}</td>
        <td class="right">
          <button v-if="auth.canWrite" class="btn danger" @click="remove(c.id)">Delete</button>
        </td>
      </tr>
    </tbody>
  </table>

  <div v-else-if="!loading" class="muted">No companies.</div>
</template>

<style scoped>
.row { display:flex; gap:10px; margin: 12px 0; }
.right { text-align: right; }
</style>
