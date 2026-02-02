<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { getDepartment } from "@/api/departments";
import type { Department } from "@/types/api";
import ErrorBanner from "@/components/Ui/ErrorBanner.vue";
import LoadingSpinner from "@/components/Ui/LoadingSpinner.vue";

const route = useRoute();
const id = computed(() => Number(route.params.id));

const item = ref<Department | null>(null);
const loading = ref(false);
const error = ref<string | null>(null);

async function load() {
  loading.value = true;
  error.value = null;
  try {
    item.value = await getDepartment(id.value);
  } catch (e: any) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
}

onMounted(load);
</script>

<template>
  <div class="header">
    <h2>Department Detail</h2>
    <RouterLink class="btn" to="/departments">Back to List</RouterLink>
  </div>

  <ErrorBanner :error="error" />
  <LoadingSpinner v-if="loading" />

  <div v-if="item" class="card">
    <div><b>ID:</b> {{ item.id }}</div>
    <div><b>Name:</b> {{ item.name }}</div>
    <div><b>Company ID:</b> {{ item.company }}</div>
    <div><b>Total Employees:</b> {{ item.employee_count }}</div>
  </div>
</template>

<style scoped>
.header { display: flex; justify-content: space-between; align-items: center; }
.card { padding: 16px; border: 1px solid #ddd; border-radius: 8px; margin-top: 12px; line-height: 2; }
</style>