<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import EmployeeForm from "@/components/EmployeeForm.vue";
import ErrorBanner from "@/components/Ui/ErrorBanner.vue";
import { createEmployee } from "@/api/employees";
import type { Employee } from "@/types/api";

const router = useRouter();
const loading = ref(false);
const error = ref<string | null>(null);

const model = ref<Partial<Employee>>({
  company: undefined,
  department: undefined,
  name: "",
  email: "",
  mobile_number: "",
  address: "",
  designation: "",
});

async function submit() {
  loading.value = true;
  error.value = null;
  try {
    const created = await createEmployee(model.value);
    router.push({ name: "employee-detail", params: { id: created.id } });
  } catch (e: any) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <h2>Create Employee</h2>
  <ErrorBanner :error="error" />
  <EmployeeForm v-model="model" :loading="loading" @submit="submit" />
</template>
