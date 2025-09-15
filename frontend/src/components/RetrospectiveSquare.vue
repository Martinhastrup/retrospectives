<template>
    <div 
    :class="['retrospective-square', `${squareType}-square`, { 'expanded': isExpanded }]" 
    @click.stop="handleSquareClick"
  >
    <div class="square-header">
      <span class="square-icon">{{ icon }}</span>
      <span class="square-title">{{ title }}</span>
      <span class="square-description">{{ description }}</span>
    </div>
                <div 
              class="square-content"
              @dragover="$emit('dragover', $event)"
              @dragleave="$emit('dragleave', $event)"
              @drop="$emit('drop', $event, squareType)"
              @dblclick="handleSquareDoubleClick"
              @click="handleSquareContentClick"
            >
              <div class="square-items-container">
                <div 
                  v-for="(item, index) in items" 
                  :key="item.id"
                  class="square-item draggable-postit"
                  :class="{ 'small-mode': !isExpanded }"
                  :data-square-type="squareType"
                  :data-item-index="index"
                  :style="{ left: (isExpanded ? item.x_maximized : item.x_minimized) + 'px', top: (isExpanded ? item.y_maximized : item.y_minimized) + 'px' }"
                  @mousedown="$emit('startDrag', $event, squareType, index)"
                  @click.stop
                  @dblclick.stop="handlePostItDoubleClick($event, squareType, index)"
                >
                  <button 
                    class="delete-postit-btn"
                    @click.stop="$emit('deletePostIt', squareType, index)"
                    title="Delete post-it"
                  >
                    ×
                  </button>
                  <div 
                    v-if="isEditing && editingItem?.squareType === squareType && editingItem?.index === index" 
                    class="edit-input-container" 
                    @click.stop
                    :style="{ 
                      '--postit-width': (editingItem?.currentWidth || 100) + 'px', 
                      '--postit-height': (editingItem?.currentHeight || 60) + 'px', 
                      width: (editingItem?.currentWidth || 100) + 'px', 
                      height: (editingItem?.currentHeight || 60) + 'px',
                      minWidth: (editingItem?.currentWidth || 100) + 'px',
                      minHeight: (editingItem?.currentHeight || 60) + 'px',
                      maxWidth: (editingItem?.currentWidth || 100) + 'px',
                      maxHeight: (editingItem?.currentHeight || 60) + 'px'
                    }"
                  >
                    <textarea
                      :value="editingText"
                      class="edit-input"
                      @input="$emit('update:editingText', ($event.target as HTMLTextAreaElement).value)"
                      @blur="$emit('finishEdit')"
                      @keyup.ctrl-enter="$emit('finishEdit')"
                      @keyup.esc="$emit('cancelEdit')"
                      @mousedown.stop
                      @click.stop
                      @selectstart.stop
                      ref="editInput"
                    ></textarea>
                  </div>
                  <div v-else class="postit-text">
                    {{ !isExpanded && item.text.length > 30 ? item.text.substring(0, 30) + '...' : item.text }}
                  </div>
                </div>
              </div>
            </div>
  </div>
</template>

<script setup lang="ts">
import { computed, watch, onUnmounted } from 'vue'
import { scaleToMaximized, scaleToMinimized } from '@/utils/scaling'
import {
  smallPostItWidth,
  smallPostItHeight,
  expandedPostItWidth,
  expandedPostItHeight
} from '@/utils/config'

// Declare global property for drag state
declare global {
  interface Window {
    isDraggingPostIt?: boolean
  }
}

interface PostIt {
  text: string
  id: string
  x_minimized?: number
  y_minimized?: number
  x_maximized?: number
  y_maximized?: number
}

interface EditingItem {
  squareType: string
  index: number
  currentWidth?: number
  currentHeight?: number
}

interface Props {
  squareType: 'good' | 'bad' | 'start' | 'stop' | 'actions'
  items: PostIt[]
  isExpanded: boolean
  editingItem: EditingItem | null
  editingText: string
}

interface Emits {
  (e: 'expand', squareType: string): void
  (e: 'dragover', event: DragEvent): void
  (e: 'dragleave', event: DragEvent): void
  (e: 'drop', event: DragEvent, squareType: string): void
  (e: 'startDrag', event: MouseEvent, squareType: string, index: number): void
  (e: 'startEdit', squareType: string, index: number): void
  (e: 'deletePostIt', squareType: string, index: number): void
  (e: 'finishEdit'): void
  (e: 'cancelEdit'): void
  (e: 'update:editingText', value: string): void
  (e: 'createPostIt', squareType: string, event: MouseEvent): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

// Square configuration
const squareConfig = {
  good: {
    icon: '😊',
    title: 'Good',
    description: 'What went well?'
  },
  bad: {
    icon: '😞',
    title: 'Bad',
    description: 'What didn\'t go well?'
  },
  start: {
    icon: '🚀',
    title: 'Start',
    description: 'What should we start doing?'
  },
  stop: {
    icon: '🛑',
    title: 'Stop',
    description: 'What should we stop doing?'
  },
  actions: {
    icon: '✅',
    title: 'Actions',
    description: 'What actions will we take?'
  }
}

const config = computed(() => squareConfig[props.squareType])
const icon = computed(() => config.value.icon)
const title = computed(() => config.value.title)
const description = computed(() => config.value.description)
const isEditing = computed(() => props.editingItem !== null)

// Click delay management to distinguish single clicks from double-clicks
let clickTimeout: number | null = null
let clickCount = 0

// Flag to prevent square expansion immediately after editing
let justFinishedEditing = false
let editingFinishTimeout: number | null = null

// Handle single click with delay to distinguish from double-click
const handleSquareClick = () => {
  console.log(`[${props.squareType}] handleSquareClick called`)
  console.log(`[${props.squareType}] window.isDraggingPostIt:`, window.isDraggingPostIt)
  console.log(`[${props.squareType}] props.editingItem:`, props.editingItem)
  console.log(`[${props.squareType}] justFinishedEditing:`, justFinishedEditing)
  
  // Check if we're currently in a drag operation by looking at the global state
  if (window.isDraggingPostIt) {
    console.log(`[${props.squareType}] Click blocked: dragging post-it`)
    return // Don't handle clicks during drag operations
  }
  
  // Check if we're currently editing a post-it
  if (props.editingItem && props.editingItem.squareType === props.squareType) {
    console.log(`[${props.squareType}] Click blocked: currently editing`)
    return // Don't handle clicks during editing
  }
  
  // Check if we just finished editing (prevent immediate expansion)
  if (justFinishedEditing) {
    console.log(`[${props.squareType}] Click blocked: just finished editing`)
    return // Don't handle clicks immediately after editing
  }
  
  console.log(`[${props.squareType}] Click allowed: proceeding with square click`)
  clickCount++
  
  if (clickCount === 1) {
    // Set a timeout to wait for potential double-click
    clickTimeout = window.setTimeout(() => {
      if (clickCount === 1) {
        // Single click confirmed - expand the square
        console.log(`[${props.squareType}] Single click confirmed: expanding square`)
        emit('expand', props.squareType)
      }
      clickCount = 0
      clickTimeout = null
    }, 200) // 200ms delay to wait for double-click
  } else if (clickCount === 2) {
    // Double-click detected - clear the timeout
    if (clickTimeout) {
      clearTimeout(clickTimeout)
      clickTimeout = null
    }
    clickCount = 0
  }
}

// Handle clicks on square content area
const handleSquareContentClick = (event: MouseEvent) => {
  console.log(`[${props.squareType}] handleSquareContentClick called`)
  console.log(`[${props.squareType}] props.editingItem:`, props.editingItem)
  
  // If we're editing, don't let clicks bubble up to the square container
  if (props.editingItem && props.editingItem.squareType === props.squareType) {
    console.log(`[${props.squareType}] Content click blocked: currently editing`)
    event.stopPropagation()
    return
  }
  
  console.log(`[${props.squareType}] Content click allowed: letting it bubble up`)
  // If we're not editing, let the click bubble up normally
  // This allows the square container click handler to work
}

// Handle double-click on post-it to edit
const handlePostItDoubleClick = (event: MouseEvent, squareType: string, index: number) => {
  console.log(`[${props.squareType}] handlePostItDoubleClick called for index ${index}`)
  
  // Clear any pending single click on the square
  if (clickTimeout) {
    clearTimeout(clickTimeout)
    clickTimeout = null
  }
  clickCount = 0
  
  // Emit the edit event
  emit('startEdit', squareType, index)
}

// Handle double-click on empty space to create new post-it
const handleSquareDoubleClick = (event: MouseEvent) => {
  console.log(`[${props.squareType}] handleSquareDoubleClick called`)
  
  // Clear any pending single click
  if (clickTimeout) {
    clearTimeout(clickTimeout)
    clickTimeout = null
  }
  clickCount = 0
  
  // Only create if we're not clicking on an existing post-it
  const target = event.target as HTMLElement
  if (!target.closest('.square-item')) {
    console.log(`[${props.squareType}] Creating new post-it`)
    emit('createPostIt', props.squareType, event)
  } else {
    console.log(`[${props.squareType}] Double-click on existing post-it, not creating new one`)
  }
}

// Debug logging for editing state
watch(() => props.editingItem, (newValue) => {
  console.log(`[${props.squareType}] editingItem changed:`, newValue)
  
  if (newValue && newValue.squareType === props.squareType) {
    console.log(`[${props.squareType}] Editing item:`, newValue)
    console.log(`[${props.squareType}] Dimensions:`, { 
      width: newValue.currentWidth, 
      height: newValue.currentHeight 
    })
    
    // Clear the "just finished editing" flag when starting to edit
    justFinishedEditing = false
    if (editingFinishTimeout) {
      clearTimeout(editingFinishTimeout)
      editingFinishTimeout = null
    }
    console.log(`[${props.squareType}] Started editing, cleared justFinishedEditing flag`)
  } else if (!newValue) {
    // Editing finished - set flag to prevent immediate expansion
    justFinishedEditing = true
    
    // Clear any existing timeout
    if (editingFinishTimeout) {
      clearTimeout(editingFinishTimeout)
    }
    
    // Clear the flag after a delay to allow normal clicking again
    editingFinishTimeout = window.setTimeout(() => {
      justFinishedEditing = false
      editingFinishTimeout = null
      console.log(`[${props.squareType}] Editing finish timeout cleared, allowing clicks again`)
    }, 300) // 300ms delay to prevent immediate expansion
    
    console.log(`[${props.squareType}] Editing finished, set justFinishedEditing flag for 300ms`)
  }
}, { deep: true })



// Watch for square expansion state changes to scale coordinates
watch(() => props.isExpanded, (isExpanded) => {
  console.log(`[RetrospectiveSquare] Square ${props.squareType} isExpanded changed to: ${isExpanded}`)
  
  props.items.forEach((item, index) => {
    if (isExpanded) {
      // Square is expanding - scale minimized coordinates to maximized
      // Use reasonable maximized dimensions instead of full viewport
      const maximizedWidth = 1200
      const maximizedHeight = 800
      if (item.x_minimized !== undefined && item.y_minimized !== undefined) {
        const scaled = scaleToMaximized(item.x_minimized, item.y_minimized)
        item.x_maximized = scaled.x
        item.y_maximized = scaled.y
      }
    } else {
      // Square is minimizing - scale maximized coordinates to minimized
      if (item.x_maximized !== undefined && item.y_maximized !== undefined) {
        const scaled = scaleToMinimized(item.x_maximized, item.y_maximized)
        item.x_minimized = scaled.x
        item.y_minimized = scaled.y
      }
    }
  })
})

// Cleanup function to clear timeouts when component unmounts
onUnmounted(() => {
  if (clickTimeout) {
    clearTimeout(clickTimeout)
    clickTimeout = null
  }
  if (editingFinishTimeout) {
    clearTimeout(editingFinishTimeout)
    editingFinishTimeout = null
  }
})
</script>

<style scoped>
/* Square Header Styles */
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

.square-description {
  font-size: 0.9rem;
  opacity: 0.8;
  text-align: left;
  margin: 0;
  font-style: italic;
  line-height: 1;
}

/* Square Content */
.square-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
  height: 100%;
}

/* Square Items Container */
.square-items-container {
  position: relative;
  width: 100%;
  flex: 1;
  overflow: hidden;
}

/* Post-it Items */
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
  transition: all 0.3s ease;
  position: absolute;
  width: 100px;
  min-height: 60px;
  cursor: grab;
  user-select: none;
  will-change: transform, left, top;
}

/* Small mode styling for post-its when square is not expanded */
.square-item.small-mode {
  width: 60px;
  min-height: 40px;
  padding: 0.25rem;
  font-size: 0.6rem;
  transform: rotate(-0.5deg) scale(0.8);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
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
  z-index: 200;
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

/* Post-it editing styles */
.edit-input-container {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 100;
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border-radius: 6px;
  padding: 0;
  box-sizing: border-box;
  min-width: 100px;
  min-height: 60px;
  resize: none;
  overflow: hidden;
  width: var(--postit-width, 100px) !important;
  height: var(--postit-height, 60px) !important;
  max-width: var(--postit-width, 100px) !important;
  max-height: var(--postit-height, 60px) !important;
  flex-shrink: 0 !important;
  flex-grow: 0 !important;
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
  padding: 0.5rem;
  margin: 0;
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

/* Small mode text styling */
.square-item.small-mode .postit-text {
  word-wrap: break-word;
  overflow: hidden;
  font-size: 0.5rem;
  line-height: 1.0;
}

/* Additional safeguards for editing container */
.edit-input-container * {
  box-sizing: border-box;
}

.edit-input-container:has(.edit-input:focus) {
  width: var(--postit-width, 100px) !important;
  height: var(--postit-height, 60px) !important;
  min-width: var(--postit-width, 100px) !important;
  min-height: var(--postit-height, 60px) !important;
}

/* Responsive adjustments */
@media (max-width: 768px) {
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
  
  .square-description {
    font-size: 0.875rem;
  }
}
</style>
