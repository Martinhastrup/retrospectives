<template>
  <div class="create-users max-w-4xl mx-auto p-6">
    <h1 class="text-3xl font-bold mb-6">Manage Users</h1>
    
    <!--  Authentication Notice 
    <div v-if="!isAuthenticated" class="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded mb-4">
      <strong>Authentication Required:</strong> Please log in to create retrospectives and manage team members.
    </div> -->
    
    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
      <strong>Error:</strong> {{ error }}
    </div>

<!-- Users List -->
<div v-else-if="users.length > 0" class="space-y-4">
      <div 
        v-for="user in users" 
        :key="user.id"
        class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <p v-if="user.userfullname" class="text-gray-600 font-bold mb-3">
              {{ user.userfullname }}
            </p>
            <p v-if="user.username" class="text-gray-600 mb-3">
              {{ user.username }}
            </p>
            <p v-if="user.email" class="text-gray-600 mb-3">
              {{ user.email }}
            </p>
            <p v-if="user.role" class="text-gray-600 mb-3">
              {{ user.role }}
            </p>
          </div>
          
          <div class="flex items-center gap-2 ml-4">
            <button 
              @click="editUser(user)"
              class="bg-blue-100 text-blue-700 px-3 py-1 rounded-md hover:bg-blue-200 transition-colors text-sm"
            >
              Edit
            </button>
            <button 
              @click="deleteUser(user.id)"
              class="bg-red-100 text-red-700 px-3 py-1 rounded-md hover:bg-red-200 transition-colors text-sm"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>

     <!-- Create Users Section -->
     <div class="bg-white rounded-lg shadow-md p-6 mb-6 mt-8">
      <h2 class="text-xl font-semibold mb-4">Add new user</h2>
      <div class="space-y-4">
        <div>
          <label for="fullName" class="block text-sm font-medium text-gray-700 mb-2">
            Full Name
          </label>
          <input 
            type="text" 
            id="fullName"
            v-model="userFullName" 
            placeholder="Enter full name" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label for="userName" class="block text-sm font-medium text-gray-700 mb-2">
            User Name
          </label>
          <input 
            type="text" 
            id="userName"
            v-model="userName" 
            placeholder="Enter user name" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label for="userRole" class="block text-sm font-medium text-gray-700 mb-2">
            Role
          </label>
          <textarea 
            id="userRole"
            v-model="userRole" 
            placeholder="User Role" 
            rows="3"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          ></textarea>
        </div>
        <div>
          <label for="userEmail" class="block text-sm font-medium text-gray-700 mb-2">
            Email
          </label>
          <input 
            type="email" 
            id="userEmail"
            v-model="userEmail" 
            placeholder="User Email" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label for="userPassword" class="block text-sm font-medium text-gray-700 mb-2">
            Password
          </label>
          <input 
            type="password" 
            id="userPassword"
            v-model="userPassword" 
            placeholder="User Password" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <button 
          @click="createUser" 
          class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {{ isCreating ? 'Creating...' : 'Create User' }}
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

    <!-- Edit User Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Edit User</h3>
          <div class="space-y-4">
            <div>
              <label for="editFullName" class="block text-sm font-medium text-gray-700 mb-2">
                Full Name
              </label>
              <input 
                type="text" 
                id="editFullName"
                v-model="editingUser!.userfullname" 
                placeholder="Enter full name" 
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label for="editUserName" class="block text-sm font-medium text-gray-700 mb-2">
                Username
              </label>
              <input 
                type="text" 
                id="editUserName"
                v-model="editingUser!.username" 
                placeholder="Enter username" 
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label for="editUserRole" class="block text-sm font-medium text-gray-700 mb-2">
                Role
              </label>
              <textarea 
                id="editUserRole"
                v-model="editingUser!.role" 
                placeholder="User Role" 
                rows="3"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              ></textarea>
            </div>
            <div class="flex justify-center gap-3">
              <button 
                @click="saveUserEdit"
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
           <h3 class="text-lg font-medium text-gray-900 mb-4">Delete User</h3>
           <p class="text-sm text-gray-500 mb-6">
             Are you sure you want to delete this user? This action cannot be undone.
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
import { ref, onMounted, computed, watch } from 'vue';
import axios from 'axios';

// Reactive data
const users = ref<User[]>([])
const userName = ref('');
const userRole = ref('');
const userEmail = ref('');
const userFullName = ref('');
const userPassword = ref('');
const isCreating = ref(false);
// const isAddingMember = ref(false);
const error = ref('')
const successMessage = ref('');
const authToken = ref<string | null>(null);
const isLoading = ref(true)
const showDeleteModal = ref(false)
const userToDelete = ref<number | null>(null)
const showEditModal = ref(false)
const editingUser = ref<User | null>(null)
const isUpdating = ref(false)

// API base URL
const API_BASE_URL = '/api';

// Computed properties
const isAuthenticated = computed(() => {
  return !!authToken.value;
});



interface User {
  id: number;
  username: string;
  userfullname?: string;
  role?: string;
  email?: any;
  created_at: string;
}

// Fetch users from API
const fetchUsers = async () => {
  try {
    isLoading.value = true
    error.value = ''
    
    console.log('Fetching users from API...')
    const response = await axios.get('/api/users/')
    console.log('API Response:', response)
    console.log('Response data:', response.data)
    
    users.value = response.data.results || response.data
    console.log('Users set to:', users.value)
  } catch (err: any) {
    console.error('Error fetching users:', err)
    console.error('Error response:', err.response)
    error.value = 'Failed to load users. Please try again.'
  } finally {
    isLoading.value = false
  }
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

// Create user function
const createUser = async () => {
  if (!userName.value.trim()) {
    error.value = 'Please enter a name for the user';
    return;
  }

  isCreating.value = true;
  error.value = '';
  successMessage.value = '';

  try {
    // TEMPORARY: Skip user creation for now to debug the issue
    console.log('🔍 Skipping team creation temporarily to debug...');
    
    // Create the user with the correct field names
    const userData = {
      username: userName.value,  // Changed from 'name' to 'username'
      userfullname: userFullName.value, // Added full_name field
      email: userEmail.value,
      role: userRole.value,      // Added role field
      password: userPassword.value   // Use password from form
    };
    
    console.log('🔍 Creating user with data:', userData);

    const userResponse = await axios.post(`${API_BASE_URL}/users/`, userData);
    const user: User = userResponse.data;

    // check if user already exists
    const existingUser = userResponse.data.results?.find((user: any) => user.email === userEmail.value);
    if (existingUser) {
      error.value = 'This user already exists';
      return;
    }

    successMessage.value = `User "${user.username}" created successfully!`;
    
    // Reset form
    userName.value = '';
    userRole.value = '';
    userEmail.value = '';
    userPassword.value = '';
    
    // Refresh the users list
    await fetchUsers();

  } catch (err: any) {
    console.error('Error creating user:', err);
    console.error('Error response:', err.response?.data);
    
    if (err.response?.status === 401) {
      error.value = 'Authentication required. Please log in.';
    } else if (err.response?.status === 500) {
      error.value = `Server error: ${err.response?.data?.detail || err.response?.data?.message || 'Internal server error'}`;
    } else {
      // Show detailed validation errors if available
      if (err.response?.data) {
        const errorData = err.response.data;
        if (typeof errorData === 'object') {
          const errorMessages = Object.entries(errorData)
            .map(([field, messages]) => `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`)
            .join('; ');
          error.value = `Validation errors: ${errorMessages}`;
        } else {
          error.value = errorData.message || errorData.error || 'Failed to create user';
        }
      } else {
        error.value = err.message || 'Failed to create user';
      }
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
watch([error, successMessage], () => {
  if (error.value || successMessage.value) {
    clearMessages();
  }
});

// Edit user function
const editUser = (user: User) => {
  editingUser.value = { ...user }
  showEditModal.value = true
}

// Save user edit
const saveUserEdit = async () => {
  if (!editingUser.value) return
  
  isUpdating.value = true
  error.value = ''
  successMessage.value = ''
  
  try {
    const response = await axios.patch(`/api/users/${editingUser.value.id}/`, {
      username: editingUser.value.username,
      userfullname: editingUser.value.userfullname,
      role: editingUser.value.role
    })
    
    // Update the user in the local list
    const index = users.value.findIndex(u => u.id === editingUser.value!.id)
    if (index !== -1) {
      users.value[index] = { ...users.value[index], ...response.data }
    }
    
    successMessage.value = 'User updated successfully!'
    showEditModal.value = false
    editingUser.value = null
    
  } catch (err: any) {
    console.error('Error updating user:', err)
    if (err.response?.data) {
      const errorData = err.response.data
      if (typeof errorData === 'object') {
        const errorMessages = Object.entries(errorData)
          .map(([field, messages]) => `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`)
          .join('; ')
        error.value = `Validation errors: ${errorMessages}`
      } else {
        error.value = errorData.message || errorData.error || 'Failed to update user'
      }
    } else {
      error.value = err.message || 'Failed to update user'
    }
  } finally {
    isUpdating.value = false
  }
}

// Cancel edit
const cancelEdit = () => {
  showEditModal.value = false
  editingUser.value = null
}

// Delete user
const deleteUser = (id: number) => {
  userToDelete.value = id
  showDeleteModal.value = true
}

// Confirm delete
const confirmDelete = async () => {
  try {
    await axios.delete(`/api/users/${userToDelete.value}/`)
    
    // Remove from local list
    users.value = users.value.filter(
      r => r.id !== userToDelete.value
    )
    
    showDeleteModal.value = false
    userToDelete.value = null
  } catch (err) {
    console.error('Error deleting user:', err)
    error.value = 'Failed to delete user. Please try again.'
  }
}

// Cancel delete
const cancelDelete = () => {
  showDeleteModal.value = false
  userToDelete.value = null
}

// Load users when component mounts
onMounted(() => {
  fetchUsers()
})
</script>


<style scoped>
.create-users {
  min-height: 100vh;
  background-color: #f9fafb;
}
</style> 