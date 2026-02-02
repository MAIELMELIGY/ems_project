<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { getEmployee, transitionEmployee } from "@/api/employees";
import type { Employee } from "@/types/api";
import { useAuthStore } from "@/stores/auth";
import ErrorBanner from "@/components/Ui/ErrorBanner.vue";
import LoadingSpinner from "@/components/Ui/LoadingSpinner.vue";

const auth = useAuthStore();
const route = useRoute();
const router = useRouter();
const id = computed(() => Number(route.params.id));

const item = ref<Employee | null>(null);
const loading = ref(false);
const error = ref<string | null>(null);

async function load() {
  loading.value = true;
  error.value = null;
  try {
    item.value = await getEmployee(id.value);
  } catch (e: any) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
}

async function act(targetStatus: "interview_scheduled" | "not_accepted" | "hired") {
  if (!item.value) return;
  loading.value = true;
  error.value = null;
  
  try {
    const payload: any = { status: targetStatus }; 
    
    if (targetStatus === "hired") {
      const date = prompt("Hired on (YYYY-MM-DD) leave empty for today:", "");
      if (date?.trim()) payload.hired_on = date.trim();
    }
    
    item.value = await transitionEmployee(item.value.id, payload);
  } catch (e: any) {
    error.value = e.response?.data?.error || e.message;
  } finally {
    loading.value = false;
  }
}

const canSchedule = computed(() => item.value?.status === "application_received");
const canHireOrRejectFromInterview = computed(() => item.value?.status === "interview_scheduled");
const canRejectFromApplication = computed(() => item.value?.status === "application_received");

onMounted(load);
</script>

<template>
  <div class="row space">
    <h2>Employee Detail</h2>
    <div class="row">
      <RouterLink class="btn" to="/employees">Back</RouterLink>
      <RouterLink v-if="auth.canWrite && item" class="btn" :to="`/employees/${item.id}/edit`">Edit</RouterLink>
    </div>
  </div>

  <ErrorBanner :error="error" />
  <LoadingSpinner v-if="loading" />

  <div v-if="item" class="card">
    <div><b>Name:</b> {{ item.name }}</div>
    <div><b>Email:</b> {{ item.email }}</div>
    <div><b>mobile_number:</b> {{ item.mobile_number }}</div>
    <div><b>Designation:</b> {{ item.designation }}</div>
    <div><b>Status:</b> {{ item.status }}</div>
    <div><b>Hired on:</b> {{ item.hired_on ?? "-" }}</div>
    <div><b>Days employed:</b> {{ item.days_employed ?? "-" }}</div>
    <div><b>Address:</b> {{ item.address || "-" }}</div>
    <div><b>status:</b> {{ item.status || "-" }}</div>

  </div>

<div v-if="item && auth.canWrite" class="actions">
  <h3>Workflow</h3>
  <div class="row">
    <button class="btn" :disabled="!canSchedule || loading" 
            @click="act('interview_scheduled')">
      Schedule Interview
    </button>
    
    <button class="btn" :disabled="!(canRejectFromApplication || canHireOrRejectFromInterview) || loading" 
            @click="act('not_accepted')">
      Reject
    </button>
    
    <button class="btn" :disabled="!canHireOrRejectFromInterview || loading" 
            @click="act('hired')">
      Hire
    </button>
  </div>
</div>
</template>

<style scoped>
.card { padding: 12px; border: 1px solid #ddd; border-radius: 10px; margin: 12px 0; display:grid; gap:6px; }
.row { display:flex; gap:10px; align-items:center; }
.space { justify-content: space-between; }
.actions { margin-top: 16px; }
</style>
