<template>
  <div class="create-users max-w-4xl mx-auto p-6">
    <h1 class="text-3xl font-bold mb-6">Manage Teams</h1>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
      <strong>Error:</strong> {{ error }}
    </div>

    <!-- Success Message -->
    <div v-if="successMessage" class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-6">
      {{ successMessage }}
    </div>

    <!-- Teams List -->
    <div v-if="teams.length > 0" class="space-y-4">
      <div 
        v-for="team in teams" 
        :key="team.id"
        class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <h3 class="text-xl font-semibold text-gray-900 mb-2">{{ team.name }}</h3>
            <p v-if="team.description" class="text-gray-600 mb-3">
              {{ team.description }}
            </p>
            
            <!-- Team Members Display -->
            <div class="mb-3">
              <h4 class="text-sm font-medium text-gray-700 mb-2">Team Members:</h4>
              <div v-if="team.members && team.members.length > 0" class="flex flex-wrap gap-2">
                <span 
                  v-for="member in team.members" 
                  :key="member.id"
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                >
                  {{ member.username }}
                </span>
              </div>
              <p v-else class="text-sm text-gray-500 italic">No members yet</p>
            </div>
            
            <p class="text-xs text-gray-400">
              Created: {{ new Date(team.created_at).toLocaleDateString() }}
            </p>
          </div>
          
          <div class="flex items-center gap-2 ml-4">
            <button 
              @click="editTeam(team)"
              class="bg-blue-100 text-blue-700 px-3 py-1 rounded-md hover:bg-blue-200 transition-colors text-sm"
            >
              Edit
            </button>
            <button 
              @click="deleteTeam(team.id)"
              class="bg-red-100 text-red-700 px-3 py-1 rounded-md hover:bg-red-200 transition-colors text-sm"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- No Teams Message -->
    <div v-if="!isLoading && teams.length === 0" class="text-center py-12 text-gray-500">
      <p class="text-lg">No teams created yet.</p>
      <p class="text-sm">Create your first team below!</p>
    </div>

    <!-- Create Teams Section -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6 mt-8">
      <h2 class="text-xl font-semibold mb-4">Add new team</h2>
      <div class="space-y-4">
        <div>
          <label for="teamName" class="block text-sm font-medium text-gray-700 mb-2">
            Team Name
          </label>
          <input 
            type="text" 
            id="teamName"
            v-model="teamName" 
            placeholder="Enter team name" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label for="teamDescription" class="block text-sm font-medium text-gray-700 mb-2">
            Team Description
          </label>
          <textarea 
            id="teamDescription"
            v-model="teamDescription" 
            placeholder="Enter team description" 
            rows="3"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          ></textarea>
        </div>

        <!-- Team Members Selection -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Team Members
          </label>
          <div class="max-h-48 overflow-y-auto border border-gray-300 rounded-md p-3 bg-gray-50">
            <div 
              v-for="user in availableUsers" 
              :key="user.id" 
              class="flex items-center space-x-3 py-2 hover:bg-white hover:rounded px-2 transition-colors"
            >
              <input 
                type="checkbox"
                :id="`user-${user.id}`"
                :value="Number(user.id)"
                v-model="selectedMembers"
                @change="() => console.log('Checkbox changed for user', user.id, 'Selected members:', selectedMembers)"
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label 
                :for="`user-${user.id}`"
                class="text-sm text-gray-700 cursor-pointer flex-1"
              >
                {{ user.username }}
              </label>
            </div>
          </div>
        </div>

        <button 
          @click="createTeam" 
          :disabled="isCreating || !teamName.trim()"
          class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {{ isCreating ? 'Creating...' : 'Create Team' }}
        </button>

      </div>
    </div>

    <!-- Edit Team Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-[500px] shadow-lg rounded-md bg-white max-h-[90vh] overflow-y-auto">
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
                placeholder="Enter team name" 
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label for="editTeamDescription" class="block text-sm font-medium text-gray-700 mb-2">
                Team Description
              </label>
              <textarea 
                id="editTeamDescription"
                v-model="editingTeam!.description" 
                placeholder="Enter team description" 
                rows="3"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              ></textarea>
            </div>

            <!-- Edit Team Members -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Team Members
              </label>
              
              <!-- Current Members -->
              <div v-if="editingTeam!.members && editingTeam!.members.length > 0" class="mb-3">
                <h4 class="text-sm font-medium text-gray-600 mb-2">Current Members:</h4>
                <div class="space-y-2">
                  <div 
                    v-for="member in editingTeam!.members" 
                    :key="member.id"
                    class="flex items-center justify-between bg-gray-50 px-3 py-2 rounded-md"
                  >
                    <span class="text-sm">{{ member.username }}</span>
                    <button 
                      @click="removeMember(member.id)"
                      class="text-red-600 hover:text-red-800 text-sm font-medium"
                    >
                      Remove
                    </button>
                  </div>
                </div>
              </div>

              <!-- Add New Members -->
              <div>
                <label class="block text-sm font-medium text-gray-600 mb-2">
                  Add New Members:
                </label>
                <div class="max-h-32 overflow-y-auto border border-gray-300 rounded-md p-2 bg-gray-50">
                  <div 
                    v-for="user in availableUsersForEdit" 
                    :key="user.id" 
                    class="flex items-center space-x-3 py-1 hover:bg-white hover:rounded px-2 transition-colors"
                  >
                    <input 
                      type="checkbox"
                      :id="`edit-user-${user.id}`"
                      :value="user.id"
                      v-model="newMembersToAdd"
                      class="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                    />
                    <label 
                      :for="`edit-user-${user.id}`"
                      class="text-sm text-gray-700 cursor-pointer flex-1"
                    >
                      {{ user.username }}
                    </label>
                  </div>
                </div>
                <button 
                  @click="addMembers"
                  :disabled="newMembersToAdd.length === 0"
                  class="mt-2 bg-green-600 text-white px-3 py-1 rounded-md hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-sm"
                >
                  Add {{ newMembersToAdd.length }} Member(s)
                </button>
              </div>
            </div>

            <div class="flex justify-center gap-3 pt-4">
              <button 
                @click="saveTeamEdit"
                :disabled="isUpdating"
                class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {{ isUpdating ? 'Saving...' : 'Save Changes' }}
              </button>
              <button 
                @click="cancelEdit"
                class="bg-gray-300 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-400 transition-colors"
              >
                Cancel
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
          <h3 class="text-lg font-medium text-gray-900 mb-4">Delete Team</h3>
          <p class="text-sm text-gray-500 mb-6">
            Are you sure you want to delete this team? This action cannot be undone.
          </p>
          
          <!-- Warning about associated data -->
          <div class="bg-yellow-50 border border-yellow-200 rounded-md p-3 mb-4 text-left">
            <p class="text-sm text-yellow-800">
              <strong>Note:</strong> Teams with associated retrospectives or other data may not be deletable.
            </p>
          </div>
          
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
import { ref, onMounted, computed, watch } from 'vue';
import axios from 'axios';

// Reactive data
const isLoading = ref(true);
const error = ref('');
const teams = ref<Team[]>([]);
const availableUsers = ref<User[]>([]);
const teamName = ref('');
const teamDescription = ref('');
const selectedMembers = ref<number[]>([]);
const isCreating = ref(false);  
const successMessage = ref('');
const showEditModal = ref(false);
const editingTeam = ref<Team | null>(null);
const isUpdating = ref(false);
const showDeleteModal = ref(false);
const teamToDelete = ref<number | null>(null);
const newMembersToAdd = ref<number[]>([]);

// API base URL
const API_BASE_URL = '/api';

interface User {
  id: number;
  username: string;
  email: string;
  userfullname?: string;
  role?: string;
}

interface Team {
  id: number;
  name: string;
  description: string;
  members?: User[];
  created_at: string;
}

// Computed property for available users in edit mode (excluding current members)
const availableUsersForEdit = computed(() => {
  if (!editingTeam.value?.members) return availableUsers.value;
  
  const currentMemberIds = editingTeam.value.members.map(m => m.id);
  return availableUsers.value.filter(user => !currentMemberIds.includes(user.id));
});

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

// Fetch available users from API
const fetchUsers = async () => {
  try {
    console.log('Fetching users from API...');
    const response = await axios.get('/api/users/');
    console.log('Users API Response:', response);
    
    availableUsers.value = response.data.results || response.data;
    console.log('Available users set to:', availableUsers.value);
  } catch (err: any) {
    console.error('Error fetching users:', err);
    error.value = 'Failed to load users. Please try again.';
  }
};

// Create team function
const createTeam = async () => {
  if (!teamName.value.trim()) {
    error.value = 'Please enter a name for the team';
    return;
  }

  console.log('Creating team with selected members:', selectedMembers.value);
  console.log('Available users:', availableUsers.value);

  isCreating.value = true;
  error.value = '';
  successMessage.value = '';

  try {
    const teamData = {
      name: teamName.value,
      description: teamDescription.value,
    };
    
    console.log('Creating team with data:', teamData);
    const teamResponse = await axios.post(`${API_BASE_URL}/teams/`, teamData);
    const team: Team = teamResponse.data;
    
    console.log('Team created successfully:', team);
    console.log('Team ID:', team.id, 'Type:', typeof team.id);

    // If team ID is missing, try to fetch the team details
    let teamToUse = team;
    if (!team.id && teamResponse.status === 201) {
      console.log('Team ID missing from response, trying to fetch team details...');
      try {
        // Try to get the team by name since we just created it
        const teamsResponse = await axios.get(`${API_BASE_URL}/teams/`);
        const allTeams = teamsResponse.data.results || teamsResponse.data;
        const createdTeam = allTeams.find((t: Team) => t.name === team.name);
        if (createdTeam) {
          teamToUse = createdTeam;
          console.log('Found created team:', createdTeam);
        }
      } catch (fetchErr: any) {
        console.error('Error fetching team details:', fetchErr);
      }
    }

    // Add team members if any were selected
    console.log('Selected members before adding:', selectedMembers.value);
    if (selectedMembers.value.length > 0 && teamToUse.id) {
      console.log(`Adding ${selectedMembers.value.length} members to team ${teamToUse.id}`);
      for (const userId of selectedMembers.value) {
        try {
          const numericUserId = Number(userId);
          console.log(`Adding member ${numericUserId} (type: ${typeof numericUserId}) to team ${teamToUse.id}`);
          const memberResponse = await axios.post(`${API_BASE_URL}/teams/${teamToUse.id}/add_member/`, {
            user_id: numericUserId
          });
          console.log(`Member ${numericUserId} added successfully:`, memberResponse.data);
        } catch (memberErr: any) {
          console.error(`Error adding member ${userId}:`, memberErr);
          console.error('Member error response:', memberErr.response?.data);
        }
      }
    } else if (selectedMembers.value.length > 0 && !teamToUse.id) {
      console.error('Cannot add members: team ID is still undefined!');
      console.error('Team response:', team);
      console.error('Team to use:', teamToUse);
    } else {
      console.log('No members selected to add');
    }

    successMessage.value = `Team "${team.name}" created successfully!`;
    
    // Reset form
    teamName.value = '';
    teamDescription.value = '';
    selectedMembers.value = [];

    // Refresh the teams list
    await fetchTeams(false);

  } catch (err: any) {
    console.error('Error creating team:', err);
    console.error('Error response:', err.response?.data);
    
    if (err.response?.status === 401) {
      error.value = 'Authentication required. Please log in.';
    } else if (err.response?.status === 500) {
      error.value = `Server error: ${err.response?.data?.detail || err.response?.data?.message || 'Internal server error'}`;
    } else {
      if (err.response?.data) {
        const errorData = err.response.data;
        if (typeof errorData === 'object') {
          const errorMessages = Object.entries(errorData)
            .map(([field, messages]) => `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`)
            .join('; ');
          error.value = `Validation errors: ${errorMessages}`;
        } else {
          error.value = errorData.message || errorData.error || 'Failed to create team';
        }
      } else {
        error.value = err.message || 'Failed to create team';
      }
    }
  } finally {
    isCreating.value = false;
  }
};

// Edit team function
const editTeam = (team: Team) => {
  editingTeam.value = { ...team };
  showEditModal.value = true;
};

// Add members to team
const addMembers = async () => {
  if (newMembersToAdd.value.length === 0 || !editingTeam.value) return;
  
  try {
    // Add all selected members
    for (const userId of newMembersToAdd.value) {
      await axios.post(`${API_BASE_URL}/teams/${editingTeam.value.id}/add_member/`, {
        user_id: userId
      });
    }
    
    // Refresh the team data
    const response = await axios.get(`${API_BASE_URL}/teams/${editingTeam.value.id}/`);
    editingTeam.value = response.data;
    
    const memberCount = newMembersToAdd.value.length;
    
    // Reset the selection
    newMembersToAdd.value = [];
    
    successMessage.value = `${memberCount} member(s) added successfully!`;
    setTimeout(() => { successMessage.value = ''; }, 3000);
    
  } catch (err: any) {
    console.error('Error adding members:', err);
    error.value = 'Failed to add members. Please try again.';
  }
};

// Remove member from team
const removeMember = async (userId: number) => {
  if (!editingTeam.value) return;
  
  try {
    await axios.post(`${API_BASE_URL}/teams/${editingTeam.value.id}/remove_member/`, {
      user_id: userId
    });
    
    // Refresh the team data
    const response = await axios.get(`${API_BASE_URL}/teams/${editingTeam.value.id}/`);
    editingTeam.value = response.data;
    
    successMessage.value = 'Member removed successfully!';
    setTimeout(() => { successMessage.value = ''; }, 3000);
    
  } catch (err: any) {
    console.error('Error removing member:', err);
    error.value = 'Failed to remove member. Please try again.';
  }
};

// Save team edit
const saveTeamEdit = async () => {
  if (!editingTeam.value) return;
  
  isUpdating.value = true;
  error.value = '';
  successMessage.value = '';
  
  try {
    const response = await axios.patch(`/api/teams/${editingTeam.value.id}/`, {
      name: editingTeam.value.name,
      description: editingTeam.value.description
    });
    
    // Update the team in the local list
    const index = teams.value.findIndex(t => t.id === editingTeam.value!.id);
    if (index !== -1) {
      teams.value[index] = { ...teams.value[index], ...response.data };
    }
    
    successMessage.value = 'Team updated successfully!';
    showEditModal.value = false;
    editingTeam.value = null;
    
  } catch (err: any) {
    console.error('Error updating team:', err);
    if (err.response?.data) {
      const errorData = err.response.data;
      if (typeof errorData === 'object') {
        const errorMessages = Object.entries(errorData)
          .map(([field, messages]) => `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`)
          .join('; ');
        error.value = `Validation errors: ${errorMessages}`;
      } else {
        error.value = errorData.message || errorData.error || 'Failed to update team';
      }
    } else {
      error.value = err.message || 'Failed to update team';
    }
  } finally {
    isUpdating.value = false;
  }
};

// Cancel edit
const cancelEdit = () => {
  showEditModal.value = false;
  editingTeam.value = null;
  newMembersToAdd.value = [];
};

// Delete team
const deleteTeam = (id: number) => {
  teamToDelete.value = id;
  showDeleteModal.value = true;
};

// Confirm delete
const confirmDelete = async () => {
  try {
    console.log('Attempting to delete team:', teamToDelete.value);
    const response = await axios.delete(`/api/teams/${teamToDelete.value}/`);
    console.log('Delete response:', response);
    
    // Remove from local list
    teams.value = teams.value.filter(
      r => r.id !== teamToDelete.value
    );
    
    showDeleteModal.value = false;
    teamToDelete.value = null;
    successMessage.value = 'Team deleted successfully!';
    setTimeout(() => { successMessage.value = ''; }, 3000);
  } catch (err: any) {
    console.error('Error deleting team:', err);
    console.error('Error response:', err.response?.data);
    
    if (err.response?.status === 500) {
      error.value = 'Server error: Team may have associated data that cannot be deleted. Please check if the team has any retrospectives or other related items.';
    } else if (err.response?.status === 404) {
      error.value = 'Team not found. It may have already been deleted.';
    } else if (err.response?.status === 403) {
      error.value = 'Permission denied. You may not have the right to delete this team.';
    } else {
      error.value = `Failed to delete team: ${err.response?.data?.detail || err.response?.data?.message || err.message}`;
    }
    
    // Keep the delete modal open so user can see the error
    setTimeout(() => { error.value = ''; }, 5000);
  }
};

// Cancel delete
const cancelDelete = () => {
  showDeleteModal.value = false;
  teamToDelete.value = null;
};

// Clear success message after 5 seconds
watch(successMessage, (newValue) => {
  if (newValue) {
    setTimeout(() => {
      successMessage.value = '';
    }, 5000);
  }
});

// Load data when component mounts
onMounted(async () => {
  await Promise.all([fetchTeams(true), fetchUsers()]);
});
</script>

<style scoped>
.teams {
  padding: 20px;
}

/* Custom scrollbar for the members selection */
.overflow-y-auto::-webkit-scrollbar {
  width: 8px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style> 