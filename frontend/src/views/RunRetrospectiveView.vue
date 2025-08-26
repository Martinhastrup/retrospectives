<template>
  <div class="run-retrospective max-w-4xl mx-auto p-6">
    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
      <strong>Error:</strong> {{ error }}
    </div>

    <!-- Retrospective Content -->
    <div v-else-if="retrospective" class="space-y-6">
      <!-- Header -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex items-center justify-between mb-4">
          <h1 class="text-3xl font-bold text-gray-900">{{ retrospective.title }}</h1>
          <router-link 
            to="/manage-retrospectives" 
            class="bg-gray-100 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-200 transition-colors"
          >
            ← Back to Retrospectives
          </router-link>
        </div>
        
        <div v-if="retrospective.description" class="text-gray-600 text-lg leading-relaxed">
          {{ retrospective.description }}
        </div>
        
        <div class="mt-4 flex items-center gap-6 text-sm text-gray-500">
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
          <span v-if="retrospective.team && retrospective.team.name" class="flex items-center">
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
            </svg>
            {{ retrospective.team.name }}
          </span>
        </div>
      </div>

      <!-- Retrospective Steps -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold text-gray-900 mb-6 text-center">Retrospective</h2>
        
        <!-- Retrospective Grid -->
        <div class="retrospective-grid" :class="{ 'expanded': expandedSquare }" @click="handleGridClick">
          <!-- Good Square -->
          <div 
            class="retrospective-square good-square" 
            :class="{ 'expanded': expandedSquare === 'good' }"
            @click.stop="expandSquare('good')"
          >
            <div class="square-header">
              <div class="square-icon">😊</div>
              <h3 class="square-title">Good</h3>
              <p class="square-description">What went well?</p>
            </div>
            <div 
              class="square-content"
              @dragover="handleDragOver"
              @dragleave="handleDragLeave"
              @drop="handleDrop($event, 'good')"
            >
              <div class="square-items-container">
                <div 
                  v-for="(item, index) in squareItems.good" 
                  :key="item.id"
                  class="square-item draggable-postit"
                  :style="{ left: item.x + 'px', top: item.y + 'px' }"
                  @mousedown="startDrag($event, 'good', index)"
                  @click.stop
                >
                  <button 
                    class="delete-postit-btn"
                    @click.stop="deletePostIt('good', index)"
                    title="Delete post-it"
                  >
                    ×
                  </button>
                  {{ item.text }}
                </div>
              </div>
            </div>
          </div>

          <!-- Bad Square -->
          <div 
            class="retrospective-square bad-square" 
            :class="{ 'expanded': expandedSquare === 'bad' }"
            @click.stop="expandSquare('bad')"
          >
            <div class="square-header">
              <div class="square-icon">😞</div>
              <h3 class="square-title">Bad</h3>
              <p class="square-description">What didn't go well?</p>
            </div>
            <div 
              class="square-content"
              @dragover="handleDragOver"
              @dragleave="handleDragLeave"
              @drop="handleDrop($event, 'bad')"
            >
              <div class="square-items-container">
                <div 
                  v-for="(item, index) in squareItems.bad" 
                  :key="item.id"
                  class="square-item draggable-postit"
                  :style="{ left: item.x + 'px', top: item.y + 'px' }"
                  @mousedown="startDrag($event, 'bad', index)"
                  @click.stop
                >
                  <button 
                    class="delete-postit-btn"
                    @click.stop="deletePostIt('bad', index)"
                    title="Delete post-it"
                  >
                    ×
                  </button>
                  {{ item.text }}
                </div>
              </div>
            </div>
          </div>

          <!-- Start Square -->
          <div 
            class="retrospective-square start-square" 
            :class="{ 'expanded': expandedSquare === 'start' }"
            @click.stop="expandSquare('start')"
          >
            <div class="square-header">
              <div class="square-icon">🚀</div>
              <h3 class="square-title">Start</h3>
              <p class="square-description">What should we start doing?</p>
            </div>
            <div 
              class="square-content"
              @dragover="handleDragOver"
              @dragleave="handleDragLeave"
              @drop="handleDrop($event, 'start')"
            >
              <div class="square-items-container">
                <div 
                  v-for="(item, index) in squareItems.start" 
                  :key="item.id"
                  class="square-item draggable-postit"
                  :style="{ left: item.x + 'px', top: item.y + 'px' }"
                  @mousedown="startDrag($event, 'start', index)"
                  @click.stop
                >
                  <button 
                    class="delete-postit-btn"
                    @click.stop="deletePostIt('start', index)"
                    title="Delete post-it"
                  >
                    ×
                  </button>
                  {{ item.text }}
                </div>
              </div>
            </div>
          </div>

          <!-- Stop Square -->
          <div 
            class="retrospective-square stop-square" 
            :class="{ 'expanded': expandedSquare === 'stop' }"
            @click.stop="expandSquare('stop')"
          >
            <div class="square-header">
              <div class="square-icon">🛑</div>
              <h3 class="square-title">Stop</h3>
              <p class="square-description">What should we stop doing?</p>
            </div>
            <div 
              class="square-content"
              @dragover="handleDragOver"
              @dragleave="handleDragLeave"
              @drop="handleDrop($event, 'stop')"
            >
              <div class="square-items-container">
                <div 
                  v-for="(item, index) in squareItems.stop" 
                  :key="item.id"
                  class="square-item draggable-postit"
                  :style="{ left: item.x + 'px', top: item.y + 'px' }"
                  @mousedown="startDrag($event, 'stop', index)"
                  @click.stop
                >
                  <button 
                    class="delete-postit-btn"
                    @click.stop="deletePostIt('stop', index)"
                    title="Delete post-it"
                  >
                    ×
                  </button>
                  {{ item.text }}
                </div>
              </div>
            </div>
          </div>

          <!-- Actions Square -->
          <div 
            class="retrospective-square actions-square" 
            :class="{ 'expanded': expandedSquare === 'actions' }"
            @click.stop="expandSquare('actions')"
          >
            <div class="square-header">
              <div class="square-icon">✅</div>
              <h3 class="square-title">Actions</h3>
              <p class="square-description">What actions will we take?</p>
            </div>
            <div 
              class="square-content"
              @dragover="handleDragOver"
              @dragleave="handleDragLeave"
              @drop="handleDrop($event, 'actions')"
            >
              <div class="square-items-container">
                <div 
                  v-for="(item, index) in squareItems.actions" 
                  :key="item.id"
                  class="square-item draggable-postit"
                  :style="{ left: item.x + 'px', top: item.y + 'px' }"
                  @mousedown="startDrag($event, 'actions', index)"
                  @click.stop
                >
                  <button 
                    class="delete-postit-btn"
                    @click.stop="deletePostIt('actions', index)"
                    title="Delete post-it"
                  >
                    ×
                  </button>
                  {{ item.text }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Post-it Notes Section -->
      <div class="post-it-section">
        <h3 class="text-lg font-semibold text-gray-900 mb-4 text-center">Add Items</h3>
        <div class="post-it-container">
          <div 
            v-for="(postIt, index) in availablePostIts" 
            :key="index"
            class="post-it-note"
            :draggable="true"
            @dragstart="handleDragStart($event, index)"
            @dragend="handleDragEnd"
          >
            <div class="post-it-content">
              <input 
                v-model="postIt.text"
                placeholder="Enter text..."
                class="post-it-input"
                @click.stop
              />
            </div>
          </div>
          <button 
            @click="addNewPostIt"
            class="add-post-it-btn"
          >
            + Add Post-it
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()

// Reactive data
const retrospective = ref<Retrospective | null>(null)
const isLoading = ref(true)
const error = ref('')
const expandedSquare = ref<string | null>(null)
const availablePostIts = ref<PostIt[]>([])
const squareItems = ref<SquareItems>({
  good: [],
  bad: [],
  start: [],
  stop: [],
  actions: []
})
const draggedPostItIndex = ref<number | null>(null)
const isDraggingPostIt = ref(false)
const hasMovedPostIt = ref(false)
const draggedItem = ref<{ squareType: keyof SquareItems, index: number } | null>(null)
const dragOffset = ref({ x: 0, y: 0 })

interface Retrospective {
  id: number
  title: string
  description?: string
  team?: any
  status: string
  created_at: string
  created_by: User
}

interface User {
  id: number
  email: string
  full_name?: string
  username?: string
}

interface PostIt {
  text: string
  id: string
  x?: number
  y?: number
}

interface SquareItems {
  good: PostIt[]
  bad: PostIt[]
  start: PostIt[]
  stop: PostIt[]
  actions: PostIt[]
}

// Fetch retrospective from API
const fetchRetrospective = async () => {
  try {
    isLoading.value = true
    error.value = ''
    
    const retrospectiveId = route.params.id
    console.log('Fetching retrospective with ID:', retrospectiveId)
    
    const response = await axios.get(`/api/retrospectives/${retrospectiveId}/`)
    console.log('API Response:', response)
    
    retrospective.value = response.data
    console.log('Retrospective set to:', retrospective.value)
  } catch (err: any) {
    console.error('Error fetching retrospective:', err)
    console.error('Error response:', err.response)
    error.value = 'Failed to load retrospective. Please try again.'
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

// Expand square functionality
const expandSquare = (squareType: string) => {
  // Don't expand if we're currently dragging a post-it
  if (isDraggingPostIt.value) {
    return
  }
  
  if (expandedSquare.value === squareType) {
    expandedSquare.value = null
  } else {
    expandedSquare.value = squareType
  }
}

// Handle grid click (click outside to collapse)
const handleGridClick = () => {
  expandedSquare.value = null
}

// Post-it functionality
const addNewPostIt = () => {
  const newPostIt: PostIt = {
    text: '',
    id: Date.now().toString()
  }
  availablePostIts.value.push(newPostIt)
  savePostItData()
}

// Storage key for this retrospective
const getStorageKey = () => {
  const retrospectiveId = route.params.id
  return `retrospective_${retrospectiveId}_postits`
}

// Save post-it data to localStorage
const savePostItData = () => {
  const data = {
    availablePostIts: availablePostIts.value,
    squareItems: squareItems.value
  }
  localStorage.setItem(getStorageKey(), JSON.stringify(data))
}

// Load post-it data from localStorage
const loadPostItData = () => {
  try {
    const savedData = localStorage.getItem(getStorageKey())
    if (savedData) {
      const data = JSON.parse(savedData)
      availablePostIts.value = data.availablePostIts || []
      squareItems.value = data.squareItems || {
        good: [],
        bad: [],
        start: [],
        stop: [],
        actions: []
      }
    }
  } catch (error) {
    console.error('Error loading post-it data:', error)
  }
}

// Drag and drop functionality
const handleDragStart = (event: DragEvent, index: number) => {
  draggedPostItIndex.value = index
  if (event.dataTransfer) {
    event.dataTransfer.effectAllowed = 'move'
    event.dataTransfer.setData('text/plain', index.toString())
  }
}

const handleDragEnd = () => {
  draggedPostItIndex.value = null
}

const handleDragOver = (event: DragEvent) => {
  event.preventDefault()
  if (event.dataTransfer) {
    event.dataTransfer.dropEffect = 'move'
  }
  // Add visual feedback
  const target = event.currentTarget as HTMLElement
  target.classList.add('drag-over')
}

const handleDragLeave = (event: DragEvent) => {
  const target = event.currentTarget as HTMLElement
  target.classList.remove('drag-over')
}

const handleDrop = (event: DragEvent, squareType: keyof SquareItems) => {
  event.preventDefault()
  
  // Remove visual feedback
  const target = event.currentTarget as HTMLElement
  target.classList.remove('drag-over')
  
  if (draggedPostItIndex.value !== null) {
    const postIt = availablePostIts.value[draggedPostItIndex.value]
    
    // Only add if the post-it has text
    if (postIt.text.trim()) {
      // Create a new post-it for the square with random position
      const newItem: PostIt = {
        text: postIt.text,
        id: Date.now().toString(),
        x: Math.random() * 200 + 20, // Random position between 20-220px
        y: Math.random() * 100 + 20  // Random position between 20-120px
      }
      
      // Add to the square
      squareItems.value[squareType].push(newItem)
      
      // Remove from available post-its
      availablePostIts.value.splice(draggedPostItIndex.value, 1)
      
      // Save the changes
      savePostItData()
    }
  }
  
  draggedPostItIndex.value = null
}

// Post-it dragging within squares
const startDrag = (event: MouseEvent, squareType: keyof SquareItems, index: number) => {
  event.preventDefault()
  event.stopPropagation()
  
  isDraggingPostIt.value = true
  hasMovedPostIt.value = false
  draggedItem.value = { squareType, index }
  
  const squareElement = document.querySelector(`.${squareType}-square`) as HTMLElement
  if (!squareElement) return
  
  const squareRect = squareElement.getBoundingClientRect()
  const item = squareItems.value[squareType][index]
  
  // Calculate offset from mouse to post-it's current position
  dragOffset.value = {
    x: event.clientX - squareRect.left - (item.x || 0),
    y: event.clientY - squareRect.top - (item.y || 0)
  }
  
  document.addEventListener('mousemove', handleMouseMove)
  document.addEventListener('mouseup', handleMouseUp)
}

const handleMouseMove = (event: MouseEvent) => {
  if (!isDraggingPostIt.value || !draggedItem.value) return
  
  hasMovedPostIt.value = true
  
  const squareElement = document.querySelector(`.${draggedItem.value.squareType}-square`) as HTMLElement
  if (!squareElement) return
  
  const rect = squareElement.getBoundingClientRect()
  
  // Calculate new position: mouse position minus the stored offset
  const newX = event.clientX - rect.left - dragOffset.value.x
  const newY = event.clientY - rect.top - dragOffset.value.y
  
  // Keep within bounds
  const constrainedX = Math.max(0, Math.min(newX, rect.width - 100))
  const constrainedY = Math.max(0, Math.min(newY, rect.height - 60))
  
  // Update the item position directly for immediate response
  const item = squareItems.value[draggedItem.value.squareType][draggedItem.value.index]
  if (item) {
    // Direct assignment for immediate update
    item.x = constrainedX
    item.y = constrainedY
  }
  
  // Force immediate DOM update
  requestAnimationFrame(() => {
    // This ensures the DOM is updated immediately
  })
}

const handleMouseUp = (event: MouseEvent) => {
  if (isDraggingPostIt.value) {
    if (event) {
      event.preventDefault()
      event.stopPropagation()
    }
    
    if (hasMovedPostIt.value) {
      savePostItData()
    }
    
    // Clear dragging state
    isDraggingPostIt.value = false
    draggedItem.value = null
  }
  
  document.removeEventListener('mousemove', handleMouseMove)
  document.removeEventListener('mouseup', handleMouseUp)
}

// Delete post-it function
const deletePostIt = (squareType: keyof SquareItems, index: number) => {
  squareItems.value[squareType].splice(index, 1)
  savePostItData()
}

// Watch for changes in post-it data and save automatically
watch([availablePostIts, squareItems], () => {
  savePostItData()
}, { deep: true })

// Load retrospective when component mounts
onMounted(() => {
  fetchRetrospective()
  loadPostItData()
})
</script>

<style scoped>
.run-retrospective {
  min-height: 100vh;
  background-color: #f9fafb;
}

/* Smooth transitions */
.transition-colors {
  transition: all 0.2s ease-in-out;
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

/* Retrospective Grid Layout */
.retrospective-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto auto auto;
  gap: 1.5rem;
  max-width: 800px;
  margin: 0 auto;
  transition: all 0.7s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

/* Expanded grid state */
.retrospective-grid.expanded {
  grid-template-columns: 1fr;
  grid-template-rows: 1fr;
  gap: 0;
}

/* Base Square Styling */
.retrospective-square {
  border-radius: 12px;
  padding: 1.5rem;
  min-height: 200px;
  display: flex;
  flex-direction: column;
  transition: all 0.7s cubic-bezier(0.4, 0, 0.2, 1);
  border: 2px solid transparent;
  position: relative;
  overflow: hidden;
  cursor: pointer;
}

.retrospective-square:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

/* Expanded square state */
.retrospective-square.expanded {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 10;
  min-height: 400px;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  transform: none;
}

.retrospective-square.expanded:hover {
  transform: none;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

/* Square Header */
.square-header {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.square-header-top {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
}

.square-icon {
  font-size: 1.5rem;
  margin-right: 0.75rem;
}

.square-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}

.square-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
  height: 100%;
}

.square-description {
  font-size: 0.95rem;
  opacity: 0.8;
  text-align: left;
  margin: 0;
  font-style: italic;
}

/* Good Square - Green and Happy */
.good-square {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border-color: #047857;
}

.good-square:hover {
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
}

/* Bad Square - Red and Sad */
.bad-square {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  border-color: #b91c1c;
}

.bad-square:hover {
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
}

/* Start Square - Blue and Energetic */
.start-square {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border-color: #1d4ed8;
}

.start-square:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
}

/* Stop Square - Orange and Warning */
.stop-square {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
  border-color: #b45309;
}

.stop-square:hover {
  background: linear-gradient(135deg, #d97706 0%, #b45309 100%);
}

/* Actions Square - Purple and Professional */
.actions-square {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  border-color: #6d28d9;
  grid-column: 1 / -1;
  min-height: 150px;
}

.actions-square:hover {
  background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
}

/* Hide non-expanded squares when one is expanded */
.retrospective-grid.expanded .retrospective-square:not(.expanded) {
  opacity: 0;
  pointer-events: none;
}

/* Responsive Design */
@media (max-width: 768px) {
  .retrospective-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .actions-square {
    grid-column: 1;
  }
  
  .retrospective-square {
    min-height: 150px;
    padding: 1rem;
  }
  
  .retrospective-square.expanded {
    min-height: 300px;
  }
  
  .square-title {
    font-size: 1.125rem;
  }
  
  .square-description {
    font-size: 0.875rem;
  }
}

/* Subtle animations */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.retrospective-square {
  animation: fadeInUp 0.6s ease-out;
}

.retrospective-square:nth-child(1) { animation-delay: 0.1s; }
.retrospective-square:nth-child(2) { animation-delay: 0.2s; }
.retrospective-square:nth-child(3) { animation-delay: 0.3s; }
.retrospective-square:nth-child(4) { animation-delay: 0.4s; }
.retrospective-square:nth-child(5) { animation-delay: 0.5s; }

/* Square Items Container */
.square-items-container {
  position: relative;
  width: 100%;
  flex: 1;
  overflow: hidden;
}

.square-item {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  padding: 0.5rem;
  border-radius: 6px;
  font-size: 0.875rem;
  word-wrap: break-word;
  border: 1px solid #f59e0b;
  color: #92400e;
  font-weight: 500;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transform: rotate(-1deg);
  transition: transform 0.1s ease, box-shadow 0.1s ease;
  position: absolute;
  width: 100px;
  min-height: 60px;
  cursor: grab;
  user-select: none;
  will-change: transform, left, top;
}

.square-item:hover {
  transform: rotate(0deg) scale(1.02);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
}

.square-item:active {
  cursor: grabbing;
  transform: rotate(0deg) scale(1.05);
  z-index: 1000;
  transition: none;
}

/* Delete button */
.delete-postit-btn {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #ef4444;
  color: white;
  border: none;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  display: none;
  align-items: center;
  justify-content: center;
  z-index: 10;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.delete-postit-btn:hover {
  background: #dc2626;
  transform: scale(1.1);
}

.square-item:hover .delete-postit-btn {
  display: flex;
}

/* Post-it Section */
.post-it-section {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  margin-top: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.post-it-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: flex-start;
}

.post-it-note {
  width: 120px;
  height: 120px;
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border-radius: 8px;
  padding: 0.75rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: grab;
  transition: all 0.3s ease;
  border: 1px solid #f59e0b;
  position: relative;
}

.post-it-note:hover {
  transform: rotate(2deg) scale(1.05);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.post-it-note:active {
  cursor: grabbing;
  transform: rotate(-2deg) scale(0.95);
}

.post-it-content {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.post-it-input {
  background: transparent;
  border: none;
  outline: none;
  font-size: 0.875rem;
  font-family: inherit;
  resize: none;
  flex: 1;
  width: 100%;
  color: #92400e;
  font-weight: 500;
}

.post-it-input::placeholder {
  color: #a16207;
  opacity: 0.7;
}

.add-post-it-btn {
  width: 120px;
  height: 120px;
  background: linear-gradient(135deg, #e5e7eb 0%, #d1d5db 100%);
  border: 2px dashed #9ca3af;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-post-it-btn:hover {
  background: linear-gradient(135deg, #d1d5db 0%, #9ca3af 100%);
  color: #374151;
  border-color: #6b7280;
}

/* Drag feedback */
.square-content {
  position: relative;
}

.square-content.drag-over {
  background: rgba(255, 255, 255, 0.1);
  border: 2px dashed rgba(255, 255, 255, 0.5);
  border-radius: 8px;
}

/* Responsive adjustments for post-its */
@media (max-width: 768px) {
  .post-it-container {
    justify-content: center;
  }
  
  .post-it-note,
  .add-post-it-btn {
    width: 100px;
    height: 100px;
  }
  
  .post-it-input {
    font-size: 0.75rem;
  }
}
</style>
