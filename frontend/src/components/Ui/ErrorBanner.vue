<script setup lang="ts">
defineProps<{ error: string | null }>();
</script>

<template>
  <div v-if="error" class="error">
    {{ error }}
  </div>
</template>

<style scoped>
.error { padding: 10px 12px; border: 1px solid #f2b8b8; background: #ffecec; color: #8b1a1a; border-radius: 6px; margin-bottom: 12px; }
</style>
