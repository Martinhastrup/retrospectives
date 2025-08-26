<template>
  <div class="manage-retrospectives max-w-6xl mx-auto p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">Manage Retrospectives</h1>
      <router-link 
        to="/create-retrospectives" 
        class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
      >
        Create New Retrospective
      </router-link>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
      <strong>Error:</strong> {{ error }}
    </div>

    <!-- Success Messages -->
    <div v-if="successMessage" class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-6">
      {{ successMessage }}
    </div>

    <!-- Retrospectives List -->
    <div v-else-if="retrospectives.length > 0" class="space-y-4">
      <div 
        v-for="retrospective in retrospectives" 
        :key="retrospective.id"
        class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <h3 class="text-xl font-semibold text-gray-900 mb-2">
              {{ retrospective.title }}
            </h3>
            <p v-if="retrospective.description" class="text-gray-600 mb-3">
              {{ retrospective.description }}
            </p>
            <p v-if="retrospective.team && retrospective.team.name" class="text-gray-600 mb-3">
              <span 
                @click="editTeam(retrospective.team)"
                class="text-blue-600 hover:text-blue-800 cursor-pointer underline decoration-dotted hover:decoration-solid transition-all"
                title="Click to edit team"
              >
                {{ retrospective.team.name }}
              </span>
            </p>
            <div class="flex items-center gap-6 text-sm text-gray-500">
              <span class="flex items-center">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                </svg>
                {{ formatDate(retrospective.created_at) }}
              </span>
              <span class="flex items-center">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                {{ retrospective.status }}
              </span>
              <span v-if="retrospective.created_by" class="flex items-center">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
                {{ retrospective.created_by.username }}
              </span>
            </div>
          </div>
          
          <div class="flex items-center gap-2 ml-4">
            <button 
              @click="runRetrospective(retrospective)"
              class="bg-green-100 text-green-700 px-3 py-1 rounded-md hover:bg-green-200 transition-colors text-sm"
            >
              {{ getButtonText(retrospective.id) }}
            </button>
            <button 
              @click="editRetrospective(retrospective)"
              class="bg-blue-100 text-blue-700 px-3 py-1 rounded-md hover:bg-blue-200 transition-colors text-sm"
            >
              Edit
            </button>
            <button 
              @click="deleteRetrospective(retrospective.id)"
              class="bg-red-100 text-red-700 px-3 py-1 rounded-md hover:bg-red-200 transition-colors text-sm"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-12">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
      </svg>
      <h3 class="mt-2 text-sm font-medium text-gray-900">No retrospectives</h3>
      <p class="mt-1 text-sm text-gray-500">Get started by creating your first retrospective.</p>
      <div class="mt-6">
        <router-link 
          to="/create-retrospectives" 
          class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
        >
          Create Retrospective
        </router-link>
      </div>
    </div>

    <!-- Edit Retrospective Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Edit Retrospective</h3>
          <div class="space-y-4">
            <div>
              <label for="editRetrospectiveTitle" class="block text-sm font-medium text-gray-700 mb-2">
                Title
              </label>
              <input 
                type="text" 
                id="editRetrospectiveTitle"
                v-model="editingRetrospective!.title" 
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label for="editRetrospectiveDescription" class="block text-sm font-medium text-gray-700 mb-2">
                Description
              </label>
              <textarea 
                id="editRetrospectiveDescription"
                v-model="editingRetrospective!.description" 
                rows="3"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              ></textarea>
            </div>
            <div class="flex justify-end gap-3">
              <button 
                @click="cancelRetrospectiveEdit"
                class="bg-gray-300 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-400 transition-colors"
              >
                Cancel
              </button>
              <button 
                @click="saveRetrospectiveEdit"
                :disabled="isUpdating"
                class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {{ isUpdating ? 'Saving...' : 'Save Changes' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Team Modal -->
    <div v-if="showTeamModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Edit Team</h3>
          <div class="space-y-4">
            <div>
              <label for="editTeamName" class="block text-sm font-medium text-gray-700 mb-2">
                Team Name
              </label>
              <input 
                type="text" 
                id="editTeamName"
                v-model="editingTeam!.name" 
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label for="editTeamDescription" class="block text-sm font-medium text-gray-700 mb-2">
                Description
              </label>
              <textarea 
                id="editTeamDescription"
                v-model="editingTeam!.description" 
                rows="3"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              ></textarea>
            </div>
            <div class="flex justify-end gap-3">
              <button 
                @click="cancelTeamEdit"
                class="bg-gray-300 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-400 transition-colors"
              >
                Cancel
              </button>
              <button 
                @click="saveTeamEdit"
                :disabled="isUpdatingTeam"
                class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {{ isUpdatingTeam ? 'Saving...' : 'Save Changes' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3 text-center">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Delete Retrospective</h3>
          <p class="text-sm text-gray-500 mb-6">
            Are you sure you want to delete this retrospective? This action cannot be undone.
          </p>
          <div class="flex justify-center gap-3">
            <button 
              @click="confirmDelete"
              class="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 transition-colors"
            >
              Delete
            </button>
            <button 
              @click="cancelDelete"
              class="bg-gray-300 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-400 transition-colors"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

// Reactive data
const retrospectives = ref<Retrospective[]>([]);
const isLoading = ref(true);
const error = ref('');
const showDeleteModal = ref(false);
const retrospectiveToDelete = ref<number | null>(null);
const showEditModal = ref(false);
const isUpdating = ref(false);
const successMessage = ref('');
const editingRetrospective = ref<Retrospective | null>(null);
const showTeamModal = ref(false);
const isUpdatingTeam = ref(false);
const editingTeam = ref<any>(null);

interface Retrospective {
  id: number;
  title: string;
  description?: string;
  team?: any;
  status: string;
  created_at: string;
  created_by: User;
}

interface User {
  id: number;
  email: string;
  full_name?: string;
  username?: string;
}

// Fetch retrospectives from API
const fetchRetrospectives = async () => {
  try {
    isLoading.value = true
    error.value = '';
    
    console.log('Fetching retrospectives from API...')
    const response = await axios.get('/api/retrospectives/')
    console.log('API Response:', response)
    console.log('Response data:', response.data)
    
    retrospectives.value = response.data.results || response.data
    console.log('Retrospectives set to:', retrospectives.value)
  } catch (err: any) {
    console.error('Error fetching retrospectives:', err)
    console.error('Error response:', err.response)
    error.value = 'Failed to load retrospectives. Please try again.'
  } finally {
    isLoading.value = false
  }
}

// Format date for display
const formatDate = (dateString: string) => {
  if (!dateString) return 'Unknown date'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Get button text based on whether retrospective has been started
const getButtonText = (retrospectiveId: number) => {
  const hasBeenStarted = localStorage.getItem(`retrospective_${retrospectiveId}_started`)
  return hasBeenStarted ? 'Continue' : 'Run'
}

// Run Retrospective function
const runRetrospective = async (retrospective: Retrospective) => {
  console.log('🔍 runRetrospective called with retrospective:', retrospective)
  
  // Check if this retrospective has been started before (using localStorage)
  const hasBeenStarted = localStorage.getItem(`retrospective_${retrospective.id}_started`)
  
  if (!hasBeenStarted) {
    // Mark this retrospective as started
    localStorage.setItem(`retrospective_${retrospective.id}_started`, 'true')
    console.log('✅ Retrospective marked as started')
  }
  
  router.push(`/run-retrospective/${retrospective.id}`)
}

// Edit Retrospective function
const editRetrospective = (retrospective: Retrospective) => {
  editingRetrospective.value = { ...retrospective }
  showEditModal.value = true
}

// Save Retrospective edit
const saveRetrospectiveEdit = async () => {
  if (!editingRetrospective.value) return
  
  isUpdating.value = true
  error.value = ''
  successMessage.value = ''
  
  try {
    const response = await axios.patch(`/api/retrospectives/${editingRetrospective.value.id}/`, {
      title: editingRetrospective.value.title,
      description: editingRetrospective.value.description,
    })
    
    // Update the retrospectives in the local list
    const index = retrospectives.value.findIndex(r => r.id === editingRetrospective.value!.id)
    if (index !== -1) {
      retrospectives.value[index] = { ...retrospectives.value[index], ...response.data }
    }
    
    successMessage.value = 'Retrospective updated successfully!'
    showEditModal.value = false
    editingRetrospective.value = null
    
  } catch (err: any) {
    console.error('Error updating retrospective:', err)
    if (err.response?.data) {
      const errorData = err.response.data
      if (typeof errorData === 'object') {
        const errorMessages = Object.entries(errorData)
          .map(([field, messages]) => `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`)
          .join('; ')
        error.value = `Validation errors: ${errorMessages}`
      } else {
        error.value = errorData.message || errorData.error || 'Failed to update retrospective'
      }
    } else {
      error.value = err.message || 'Failed to update retrospective'
    }
  } finally {
    isUpdating.value = false
  }
}

// Cancel edit
const cancelRetrospectiveEdit = () => {
  showEditModal.value = false
  editingRetrospective.value = null
}

// Edit Team function
const editTeam = (team: any) => {
  console.log('🔍 editTeam called with team:', team)
  editingTeam.value = { ...team }
  showTeamModal.value = true
  console.log('🔍 showTeamModal set to:', showTeamModal.value)
  console.log('🔍 editingTeam set to:', editingTeam.value)
}

// Save Team edit
const saveTeamEdit = async () => {
  if (!editingTeam.value) return
  
  isUpdatingTeam.value = true
  error.value = ''
  successMessage.value = ''
  
  try {
    const response = await axios.patch(`/api/teams/${editingTeam.value.id}/`, {
      name: editingTeam.value.name,
      description: editingTeam.value.description,
    })
    
    // Update the team in retrospectives that use it
    retrospectives.value.forEach(retrospective => {
      if (retrospective.team && retrospective.team.id === editingTeam.value.id) {
        retrospective.team = { ...retrospective.team, ...response.data }
      }
    })
    
    successMessage.value = 'Team updated successfully!'
    showTeamModal.value = false
    editingTeam.value = null
    
  } catch (err: any) {
    console.error('Error updating team:', err)
    if (err.response?.data) {
      const errorData = err.response.data
      if (typeof errorData === 'object') {
        const errorMessages = Object.entries(errorData)
          .map(([field, messages]) => `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`)
          .join('; ')
        error.value = `Validation errors: ${errorMessages}`
      } else {
        error.value = errorData.message || errorData.error || 'Failed to update team'
      }
    } else {
      error.value = err.message || 'Failed to update team'
    }
  } finally {
    isUpdatingTeam.value = false
  }
}

// Cancel team edit
const cancelTeamEdit = () => {
  showTeamModal.value = false
  editingTeam.value = null
}

// Delete retrospective
const deleteRetrospective = (id: number) => {
  retrospectiveToDelete.value = id
  showDeleteModal.value = true
}

// Confirm delete
const confirmDelete = async () => {
  try {
    await axios.delete(`/api/retrospectives/${retrospectiveToDelete.value}/`)
    
    // Remove from local list
    retrospectives.value = retrospectives.value.filter(
      r => r.id !== retrospectiveToDelete.value
    )
    
    showDeleteModal.value = false
    retrospectiveToDelete.value = null
  } catch (err: any) {
    console.error('Error deleting retrospective:', err)
    error.value = 'Failed to delete retrospective. Please try again.'
  }
}

// Cancel delete
const cancelDelete = () => {
  showDeleteModal.value = false
  retrospectiveToDelete.value = null
}

// Load retrospectives when component mounts
onMounted(() => {
  fetchRetrospectives()
})
</script>

<style scoped>
.manage-retrospectives {
  min-height: 100vh;
  background-color: #f9fafb;
}

/* Smooth transitions */
.transition-colors {
  transition: all 0.2s ease-in-out;
}

.transition-shadow {
  transition: box-shadow 0.2s ease-in-out;
}

/* Hover effects */
.hover\:shadow-lg:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* Loading animation */
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>
