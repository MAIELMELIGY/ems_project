<script setup lang="ts">
import { ref, watch, onMounted } from "vue";
import { listCompanies } from "@/api/companies";
import { listDepartments } from "@/api/departments";
import type { Company, Department, Employee } from "@/types/api";

const props = defineProps<{
  modelValue: Partial<Employee>;
  loading?: boolean;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", v: Partial<Employee>): void;
  (e: "submit"): void;
}>();

const companies = ref<Company[]>([]);
const departments = ref<Department[]>([]);
const form = ref<Partial<Employee>>({ ...props.modelValue });

watch(
  () => props.modelValue,
  (v) => (form.value = { ...v })
);

function update() {
  emit("update:modelValue", { ...form.value });
}

watch(
  () => form.value.company,
  async (companyId) => {
    form.value.department = undefined;
    update();
    if (!companyId) {
      departments.value = [];
      return;
    }
    departments.value = await listDepartments(Number(companyId));
  }
);

onMounted(async () => {
  companies.value = await listCompanies();
  if (form.value.company) {
    departments.value = await listDepartments(Number(form.value.company));
  }
});
</script>

<template>
  <form @submit.prevent="emit('submit')" class="form">
    <label>Company</label>
    <select v-model="form.company" @change="update" required>
      <option :value="undefined">Select...</option>
      <option v-for="c in companies" :key="c.id" :value="c.id">{{ c.name }}</option>
    </select>

    <label>Department</label>
    <select v-model="form.department" @change="update" required :disabled="!form.company">
      <option :value="undefined">Select...</option>
      <option v-for="d in departments" :key="d.id" :value="d.id">{{ d.name }}</option>
    </select>

    <label>Name</label>
    <input v-model="form.name" @input="update" required />

    <label>Email</label>
    <input v-model="form.email" @input="update" type="email" required />

    <label>Mobile</label>
    <input v-model="form.mobile" @input="update" required placeholder="+123456789" />

    <label>Designation</label>
    <input v-model="form.designation" @input="update" required />

    <label>Address</label>
    <textarea v-model="form.address" @input="update" rows="3"></textarea>

    <button class="btn" :disabled="loading" type="submit">
      {{ loading ? "Saving..." : "Save" }}
    </button>
  </form>
</template>

<style scoped>
.form { display:grid; gap:10px; max-width: 520px; }
</style>
