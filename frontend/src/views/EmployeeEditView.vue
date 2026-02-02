<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import EmployeeForm from "@/components/EmployeeForm.vue";
import ErrorBanner from "@/components/Ui/ErrorBanner.vue";
import LoadingSpinner from "@/components/Ui/LoadingSpinner.vue";
import { getEmployee, updateEmployee } from "@/api/employees";
import type { Employee } from "@/types/api";

const route = useRoute();
const router = useRouter();
const id = computed(() => Number(route.params.id));

const loading = ref(false);
const fetching = ref(false);
const error = ref<string | null>(null);

const model = ref<Partial<Employee>>({});

onMounted(async () => {
  fetching.value = true;
  try {
    model.value = await getEmployee(id.value);
  } catch (e: any) {
    error.value = e.message;
  } finally {
    fetching.value = false;
  }
});

async function submit() {
  loading.value = true;
  error.value = null;
  try {
    const updated = await updateEmployee(id.value, model.value);
    router.push({ name: "employee-detail", params: { id: updated.id } });
  } catch (e: any) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <h2>Edit Employee</h2>
  <ErrorBanner :error="error" />
  <LoadingSpinner v-if="fetching" />
  <EmployeeForm v-else v-model="model" :loading="loading" @submit="submit" />
</template>
