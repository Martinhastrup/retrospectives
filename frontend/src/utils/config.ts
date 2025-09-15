// Global configuration for retrospective square dimensions and post-it sizes

// Layout constants
export const margin = 2
export const padding = 24 // 1.5rem padding
export const headerHeight = 60 // Approximate header height including margin

// Square dimensions (full square including padding and header)
export const smallSquareWidth = 340
export const smallSquareHeight = 200
export const expandedSquareWidth = 800
export const expandedSquareHeight = 600

// Content area dimensions (excluding padding and header)
export const smallContentWidth = smallSquareWidth - (padding * 2)  // 340 - 48 = 292
export const smallContentHeight = smallSquareHeight - padding - headerHeight  // 200 - 24 - 60 = 116
export const expandedContentWidth = expandedSquareWidth - (padding * 2)  // 800 - 48 = 752
export const expandedContentHeight = expandedSquareHeight - padding - headerHeight  // 600 - 24 - 60 = 516

// Post-it dimensions
export const smallPostItWidth = 60
export const smallPostItHeight = 40
export const expandedPostItWidth = 100
export const expandedPostItHeight = 60

// Available space for post-it placement (content area minus post-it size)
export const smallAvailableWidth = smallContentWidth - smallPostItWidth  // 292 - 60 = 232
export const smallAvailableHeight = smallContentHeight - smallPostItHeight  // 116 - 40 = 76
export const expandedAvailableWidth = expandedContentWidth - expandedPostItWidth  // 752 - 100 = 652
export const expandedAvailableHeight = expandedContentHeight - expandedPostItHeight  // 516 - 60 = 456
