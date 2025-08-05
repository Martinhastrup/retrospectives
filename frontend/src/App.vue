<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <router-link to="/" class="flex items-center">
              <h1 class="text-xl font-bold text-primary-600">Team Retrospectives</h1>
            </router-link>
          </div>
          <div class="flex items-center space-x-4">
            <router-link to="/teams" class="text-gray-700 hover:text-primary-600">Teams</router-link>
            <router-link to="/retrospectives" class="text-gray-700 hover:text-primary-600">Retrospectives</router-link>
            <router-link to="/login" class="btn-primary">Login</router-link>
          </div>
        </div>
      </div>
    </nav>
    
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
// Component logic will be added here
</script> 