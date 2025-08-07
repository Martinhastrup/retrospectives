<template>
  <div class="retrospective-detail">
    <h1>Retrospective Detail</h1>
    <p>Retrospective detail page - coming soon</p>
    <p>ID: {{ $route.params.id }}</p>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()
</script>

<style scoped>
.retrospective-detail {
  padding: 20px;
}
</style> 