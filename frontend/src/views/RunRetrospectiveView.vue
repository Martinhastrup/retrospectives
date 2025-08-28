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
        <p class="text-sm text-gray-600 mb-6 text-center">Single click to expand - Double click to create post-it notes</p>
        
        <!-- Retrospective Grid -->
        <div class="retrospective-grid" :class="{ 'expanded': expandedSquare }" @click="handleGridClick">
          <RetrospectiveSquare
            v-for="squareType in (['good', 'bad', 'start', 'stop', 'actions'] as const)"
            :key="squareType"
            :square-type="squareType"
            :items="squareItems[squareType]"
            :is-expanded="expandedSquare === squareType"
            :editing-item="editingItem"
            v-model:editing-text="editingText"
            @expand="safeExpandSquare"
            @dragover="handleDragOver"
            @dragleave="handleDragLeave"
            @drop="handleDrop"
            @start-drag="startDrag"
            @start-edit="startEdit"
            @delete-post-it="deletePostIt"
            @finish-edit="finishEdit"
            @cancel-edit="cancelEdit"
            @create-post-it="createPostIt"
          />
        </div>
      </div>


    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import RetrospectiveSquare from '@/components/RetrospectiveSquare.vue'

// Declare global property for drag state
declare global {
  interface Window {
    isDraggingPostIt?: boolean
  }
}

const route = useRoute()

// Reactive data
const retrospective = ref<Retrospective | null>(null)
const isLoading = ref(true)
const error = ref('')
const expandedSquare = ref<string | null>(null)
const squareItems = ref<SquareItems>({
  good: [],
  bad: [],
  start: [],
  stop: [],
  actions: []
})
const draggedItem = ref<{ squareType: keyof SquareItems, index: number } | null>(null)
const dragOffset = ref({ x: 0, y: 0 })

// Editing state
const editingItem = ref<{ squareType: keyof SquareItems, index: number, currentWidth?: number, currentHeight?: number } | null>(null)
const editingText = ref('')
const isFinishingEdit = ref(false)

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
  originalX?: number
  originalY?: number
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
  // Don't expand if we're currently editing one
  if (editingItem.value) {
    return
  }
  
  if (expandedSquare.value === squareType) {
    expandedSquare.value = null
  } else {
    expandedSquare.value = squareType
  }
}

// Safe expand function that checks editing state
const safeExpandSquare = (squareType: string) => {
  console.log('safeExpandSquare called for:', squareType, 'editingItem:', editingItem.value, 'isFinishingEdit:', isFinishingEdit.value)
  if (!editingItem.value && !isFinishingEdit.value) {
    expandSquare(squareType)
  } else {
    console.log('Preventing expansion - currently editing or finishing edit')
  }
}

// Handle grid click (click outside to collapse)
const handleGridClick = () => {
  // Don't collapse if we're currently editing a post-it
  if (editingItem.value) {
    return
  }
  expandedSquare.value = null
}



// Storage key for this retrospective
const getStorageKey = () => {
  const retrospectiveId = route.params.id
  return `retrospective_${retrospectiveId}_postits`
}

// Save post-it data to localStorage
const savePostItData = () => {
  const data = {
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

// Drag and drop functionality (simplified - only for moving post-its within squares)
const handleDragOver = (event: DragEvent) => {
  event.preventDefault()
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
}

// Post-it dragging within squares
const startDrag = (event: MouseEvent, squareType: keyof SquareItems, index: number) => {
  event.preventDefault()
  event.stopPropagation()
  
  // Set global drag flag
  window.isDraggingPostIt = true
  
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
  if (!draggedItem.value) return
  
  const squareElement = document.querySelector(`.${draggedItem.value.squareType}-square`) as HTMLElement
  if (!squareElement) return
  
  const rect = squareElement.getBoundingClientRect()
  
  // Calculate new position: mouse position minus the stored offset
  const newX = event.clientX - rect.left - dragOffset.value.x
  const newY = event.clientY - rect.top - dragOffset.value.y
  
  // Keep within bounds with 25px margin from edges
  // Account for the square's padding (1.5rem = 24px) and header height
  const margin = 25 // 25px margin from edges
  const padding = 24 // 1.5rem padding
  const headerHeight = 60 // Approximate header height including margin
  
  // Calculate the available content area (excluding padding and header)
  const contentWidth = rect.width - (padding * 2)
  const contentHeight = rect.height - padding - headerHeight
  
  // Check if the square is expanded to determine post-it size constraints
  const isExpanded = expandedSquare.value === draggedItem.value.squareType
  const postItWidth = isExpanded ? 100 : 60
  const postItHeight = isExpanded ? 60 : 40
  
  const constrainedX = Math.max(margin, Math.min(newX, contentWidth - postItWidth - margin))
  const constrainedY = Math.max(margin, Math.min(newY, contentHeight - postItHeight - margin))
  
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
  if (draggedItem.value) {
    if (event) {
      event.preventDefault()
      event.stopPropagation()
    }
    
    // Save the changes
    savePostItData()
    
    // Clear dragging state
    draggedItem.value = null
  }
  
  // Clear global drag flag
  window.isDraggingPostIt = false
  
  document.removeEventListener('mousemove', handleMouseMove)
  document.removeEventListener('mouseup', handleMouseUp)
}



// Delete post-it function
const deletePostIt = (squareType: keyof SquareItems, index: number) => {
  squareItems.value[squareType].splice(index, 1)
  savePostItData()
}

// Watch for changes in post-it data and save automatically
watch([squareItems], () => {
  savePostItData()
}, { deep: true })

// Additional safeguard: ensure editing dimensions are preserved
watch(editingItem, (newValue) => {
  if (newValue && newValue.currentWidth && newValue.currentHeight) {
    // Force the dimensions to be preserved
    nextTick(() => {
      const container = document.querySelector('.edit-input-container') as HTMLElement
      if (container) {
        container.style.width = newValue.currentWidth + 'px'
        container.style.height = newValue.currentHeight + 'px'
        container.style.setProperty('--postit-width', newValue.currentWidth + 'px')
        container.style.setProperty('--postit-height', newValue.currentHeight + 'px')
      }
    })
  }
}, { deep: true })

// Editing functions
const startEdit = (squareType: keyof SquareItems, index: number) => {
  console.log('startEdit called for:', squareType, index)
  editingItem.value = { squareType, index }
  editingText.value = squareItems.value[squareType][index].text
  console.log('editingItem set to:', editingItem.value)
  
  // Capture the current post-it dimensions before editing
  // Use data attributes for reliable element selection
  const postItElement = document.querySelector(`[data-square-type="${squareType}"][data-item-index="${index}"]`) as HTMLElement
  if (postItElement) {
    const currentWidth = postItElement.offsetWidth
    const currentHeight = postItElement.offsetHeight
    
    // Store the dimensions in the editing state with fallback values
    editingItem.value.currentWidth = Math.max(currentWidth, 100)
    editingItem.value.currentHeight = Math.max(currentHeight, 60)
    
    console.log('Captured dimensions:', { width: currentWidth, height: currentHeight, stored: { width: editingItem.value.currentWidth, height: editingItem.value.currentHeight } })
  } else {
    // Fallback dimensions if element not found
    editingItem.value.currentWidth = 100
    editingItem.value.currentHeight = 60
    console.log('Using fallback dimensions:', { width: 100, height: 60 })
  }
  
  // Focus the input on next tick to ensure it's rendered
  nextTick(() => {
    const input = document.querySelector('.edit-input') as HTMLInputElement
    if (input) {
      input.focus()
    }
  })
}

const finishEdit = () => {
  console.log('finishEdit called, editingItem:', editingItem.value)
  if (editingItem.value) {
    const { squareType, index } = editingItem.value
    if (editingText.value.trim()) {
      squareItems.value[squareType][index].text = editingText.value.trim()
      savePostItData()
    }
    
    // Set flag to prevent expansion during the finishing process
    isFinishingEdit.value = true
    
    // Clear editing state
    editingItem.value = null
    editingText.value = ''
    console.log('editingItem cleared')
    
    // Reset flag after a short delay to allow click events to complete
    setTimeout(() => {
      isFinishingEdit.value = false
      console.log('isFinishingEdit reset to false')
    }, 100)
  }
}

const cancelEdit = () => {
  editingItem.value = null
  editingText.value = ''
  isFinishingEdit.value = false
}

// Create new post-it in a specific square
const createPostIt = (squareType: keyof SquareItems, event: MouseEvent) => {
  // Get the position relative to the square
  const squareElement = event.currentTarget as HTMLElement
  const rect = squareElement.getBoundingClientRect()
  
  // Check if the square is expanded to determine post-it size
  const isExpanded = expandedSquare.value === squareType
  const postItWidth = isExpanded ? 100 : 60
  const postItHeight = isExpanded ? 60 : 40
  
  const x = event.clientX - rect.left - (postItWidth / 2) // Center the post-it on the click
  const y = event.clientY - rect.top - (postItHeight / 2)
  
  // Create a new post-it
  const newItem: PostIt = {
    text: '',
    id: Date.now().toString(),
    x: Math.max(20, Math.min(x, rect.width - postItWidth - 20)), // Keep within bounds
    y: Math.max(20, Math.min(y, rect.height - postItHeight - 20))
  }
  
  // Add to the square
  squareItems.value[squareType].push(newItem)
  
  // Start editing immediately
  editingItem.value = { squareType, index: squareItems.value[squareType].length - 1 }
  editingText.value = ''
  
  // Save the changes
  savePostItData()
  
  // Focus the input on next tick
  nextTick(() => {
    const input = document.querySelector('.edit-input') as HTMLInputElement
    if (input) {
      input.focus()
    }
  })
}

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
  border: none;
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
  flex-direction: row;
  align-items: baseline;
  margin-bottom: 1rem;
  gap: 0.5rem;
  justify-content: flex-start;
}



.square-icon {
  font-size: 1.25rem;
  margin-right: 0.25rem;
  line-height: 1;
  display: flex;
  align-items: center;
}

.square-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0;
  line-height: 1;
}

.square-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
  height: 100%;
}

.square-description {
  font-size: 0.9rem;
  opacity: 0.8;
  text-align: left;
  margin: 0;
  font-style: italic;
  line-height: 1;
}

/* Good Square - Green and Happy */
.good-square {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.good-square:hover {
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
}

/* Bad Square - Red and Sad */
.bad-square {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
}

.bad-square:hover {
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
}

/* Start Square - Blue and Energetic */
.start-square {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
}

.start-square:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
}

/* Stop Square - Orange and Warning */
.stop-square {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
}

.stop-square:hover {
  background: linear-gradient(135deg, #d97706 0%, #b45309 100%);
}

/* Actions Square - Purple and Professional */
.actions-square {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
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
  
  .square-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }
  
  .square-icon {
    font-size: 1.1rem;
    margin-right: 0;
  }
  
  .square-title {
    font-size: 1rem;
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

/* Ensure post-it items maintain size during editing */
.square-item:has(.edit-input-container) {
  width: auto !important;
  height: auto !important;
  min-width: 100px;
  min-height: 60px;
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

/* Post-it editing styles */
.edit-input-container {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 100;
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border-radius: 6px;
  padding: 0.5rem;
  box-sizing: border-box;
  min-width: 100px;
  min-height: 60px;
  resize: none;
  overflow: hidden;
  width: var(--postit-width, 100px) !important;
  height: var(--postit-height, 60px) !important;
  max-width: var(--postit-width, 100px) !important;
  max-height: var(--postit-height, 60px) !important;
}

.edit-input {
  width: 100%;
  height: 100%;
  background: transparent;
  border: none;
  font-size: 0.875rem;
  font-family: inherit;
  color: #92400e;
  font-weight: 500;
  outline: none;
  resize: none;
  box-sizing: border-box;
  word-wrap: break-word;
  white-space: pre-wrap;
  overflow-wrap: break-word;
  line-height: 1.2;
  overflow: hidden;
  cursor: text;
  user-select: text;
  min-width: 100px;
  min-height: 60px;
}

.edit-input:focus {
  border-color: #d97706;
  box-shadow: 0 0 0 3px rgba(217, 119, 6, 0.1);
}

/* Prevent text selection from affecting size */
.edit-input::selection {
  background-color: rgba(217, 119, 6, 0.3);
}

.edit-input::-moz-selection {
  background-color: rgba(217, 119, 6, 0.3);
}

.postit-text {
  word-wrap: break-word;
  line-height: 1.2;
  width: 100%;
  height: 100%;
  display: block;
}
</style>
