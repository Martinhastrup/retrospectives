<template>
  <div class="create-retrospectives max-w-4xl mx-auto p-6">
    <h1 class="text-3xl font-bold mb-6">New Retrospective</h1>
    
    <!--  Authentication Notice 
    <div v-if="!isAuthenticated" class="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded mb-4">
      <strong>Authentication Required:</strong> Please log in to create retrospectives and manage team members.
    </div> -->
    
    <!-- Create Retrospective Section -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 class="text-xl font-semibold mb-4">Create New Retrospective</h2>
      <div class="space-y-4">
        <div>
          <label for="retrospectiveName" class="block text-sm font-medium text-gray-700 mb-2">
            Retrospective Name
          </label>
          <input 
            type="text" 
            id="retrospectiveName"
            v-model="retrospectiveName" 
            placeholder="Enter retrospective name" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label for="retrospectiveDescription" class="block text-sm font-medium text-gray-700 mb-2">
            Description (Optional)
          </label>
          <textarea 
            id="retrospectiveDescription"
            v-model="retrospectiveDescription" 
            placeholder="Enter description" 
            rows="3"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          ></textarea>
        </div>
        <!-- Team Selection -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Team
          </label>
          <div class="max-h-48 overflow-y-auto border border-gray-300 rounded-md p-3 bg-gray-50">
            <div 
              v-for="team in teams" 
              :key="team.id" 
              class="flex items-center space-x-3 py-2 hover:bg-white hover:rounded px-2 transition-colors"
            >
              <input 
                type="checkbox"
                :id="`team-${team.id}`"
                :value="Number(team.id)"
                v-model="selectedTeam"
                @change="() => console.log('Checkbox changed for team', team.id, 'Selected members:', selectedTeam)"
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label 
                :for="`team-${team.id}`"
                class="text-sm text-gray-700 cursor-pointer flex-1"
              >
                {{ team.name }}
              </label>
            </div>
          </div>
        </div>
        <button 
          @click="createRetrospective" 
          class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {{ isCreating ? 'Creating...' : 'Create Retrospective' }}
        </button>
      </div>
    </div>

    <!-- Error Messages -->
    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      {{ error }}
    </div>

    <!-- Success Messages -->
    <div v-if="successMessage" class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
      {{ successMessage }}
    </div>
    
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

// Reactive data
const retrospectiveName = ref('');
const retrospectiveDescription = ref('');
const teamMemberEmail = ref('');
const teamMembers = ref<any[]>([]);
const isCreating = ref(false);
const error = ref('');
const successMessage = ref('');
const authToken = ref<string | null>(null);
const teams = ref<Team[]>([]);
const selectedTeam = ref<number[]>([]);
const isLoading = ref(true);

// API base URL
const API_BASE_URL = '/api';

// Computed properties
const isAuthenticated = computed(() => {
  return !!authToken.value;
});

// Types
interface Team {
  id: number;
  name: string;
  description: string;
  members?: User[];
  created_at: string;
}

interface User {
  id: number;
  email: string;
  full_name?: string;
  username?: string;
}

interface Retrospective {
  id: number;
  title: string;
  description?: string;
  team?: any;
  status: string;
  created_at: string;
}

// Axios interceptor to add authentication headers
axios.interceptors.request.use(
  (config) => {
    if (authToken.value) {
      config.headers.Authorization = `Bearer ${authToken.value}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Axios interceptor to handle authentication errors
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized error
      error.value = 'Authentication required. Please log in.';
      authToken.value = null;
    }
    return Promise.reject(error);
  }
);

// Fetch teams from API
const fetchTeams = async (showLoading = false) => {
  try {
    if (showLoading) {
      isLoading.value = true;
    }
    error.value = '';
    
    console.log('Fetching teams from API...');
    const response = await axios.get('/api/teams/');
    console.log('API Response:', response);
    console.log('Response data:', response.data);
    
    teams.value = response.data.results || response.data;
    console.log('Teams set to:', teams.value);
  } catch (err: any) {
    console.error('Error fetching teams:', err);
    console.error('Error response:', err.response);
    error.value = 'Failed to load teams. Please try again.';
  } finally {
    if (showLoading) {
      isLoading.value = false;
    }
  }
};

// Create retrospective function
const createRetrospective = async () => {
  if (!retrospectiveName.value.trim()) {
    error.value = 'Please enter a retrospective name';
    return;
  }

  // if (!isAuthenticated.value) {
  // error.value = 'Please log in to create a retrospective';
  // return;
  // }

  isCreating.value = true;
  error.value = '';
  successMessage.value = '';

  try {
    // Create the retrospective
    const retrospectiveData = {
      title: retrospectiveName.value,
      description: retrospectiveDescription.value,
      team: selectedTeam.value.length > 0 ? selectedTeam.value[0] : null
    };
    
    console.log('🔍 Creating retrospective with data:', retrospectiveData);

    const retrospectiveResponse = await axios.post(`${API_BASE_URL}/retrospectives/`, retrospectiveData);
    const retrospective: Retrospective = retrospectiveResponse.data;

    successMessage.value = `Retrospective "${retrospective.title}" created successfully!`;
    
    // Reset form
    retrospectiveName.value = '';
    retrospectiveDescription.value = '';
    selectedTeam.value = [];
    teamMembers.value = [];
    teamMemberEmail.value = '';

  } catch (err: any) {
    console.error('Error creating retrospective:', err);
    console.error('Error response:', err.response?.data);
    
    if (err.response?.status === 401) {
      error.value = 'Authentication required. Please log in.';
    } else if (err.response?.status === 500) {
      error.value = `Server error: ${err.response?.data?.detail || err.response?.data?.message || 'Internal server error'}`;
    } else {
      error.value = err.response?.data?.message || err.response?.data?.error || err.message || 'Failed to create retrospective';
    }
  } finally {
    isCreating.value = false;
  }
};


// Clear messages after a delay
const clearMessages = () => {
  setTimeout(() => {
    error.value = '';
    successMessage.value = '';
  }, 5000);
};

// Watch for messages to auto-clear
import { watch } from 'vue';
watch([error, successMessage], () => {
  if (error.value || successMessage.value) {
    clearMessages();
  }
});

onMounted(async () => {
  await Promise.all([fetchTeams(true)]);
});
</script>

<style scoped>
.create-retrospectives {
  min-height: 100vh;
  background-color: #f9fafb;
}
</style> 