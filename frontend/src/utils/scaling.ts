// Scaling functions to maintain relative positioning between minimized and maximized views
import {
  margin,
  padding,
  headerHeight,
  smallContentWidth,
  smallContentHeight,
  expandedContentWidth,
  expandedContentHeight,
  smallPostItWidth,
  smallPostItHeight,
  expandedPostItWidth,
  expandedPostItHeight,
  smallAvailableWidth,
  smallAvailableHeight,
  expandedAvailableWidth,
  expandedAvailableHeight
} from './config'

export const scaleToMaximized = (x: number, y: number) => {
  // The input coordinates (x, y) are already relative to the content area
  // No need to subtract padding and header height
  const contentX = x
  const contentY = y
  
  // Calculate fractions based on available space for post-it placement (0 to 1)
  // This ensures proportional scaling regardless of post-it size changes
  const fractionX = Math.max(0, Math.min(1, contentX / smallAvailableWidth))
  const fractionY = Math.max(0, Math.min(1, contentY / smallAvailableHeight))
  
  // Scale to expanded coordinates maintaining the same fractions
  // Then adjust for the different post-it size to keep it within bounds
  const scaledX = fractionX * expandedAvailableWidth
  const scaledY = fractionY * expandedAvailableHeight
  
  // Ensure within bounds by accounting for the larger post-it size
  const maxX = expandedContentWidth - expandedPostItWidth - margin
  const maxY = expandedContentHeight - expandedPostItHeight - margin
  
  return { 
    x: Math.max(margin, Math.min(scaledX, maxX)), 
    y: Math.max(margin, Math.min(scaledY, maxY)) 
  }
}

export const scaleToMinimized = (x: number, y: number) => {
  // The input coordinates (x, y) are already relative to the content area
  // No need to subtract padding and header height
  const contentX = x
  const contentY = y
  
  // Calculate fractions based on available space for post-it placement (0 to 1)
  // This ensures proportional scaling regardless of post-it size changes
  const fractionX = Math.max(0, Math.min(1, contentX / expandedAvailableWidth))
  const fractionY = Math.max(0, Math.min(1, contentY / expandedAvailableHeight))
  
  // Scale to minimized coordinates maintaining the same fractions
  // Then adjust for the different post-it size to keep it within bounds
  const scaledX = fractionX * smallAvailableWidth
  const scaledY = fractionY * smallAvailableHeight
  
  // Ensure within bounds by accounting for the smaller post-it size
  const maxX = smallContentWidth - smallPostItWidth - margin
  const maxY = smallContentHeight - smallPostItHeight - margin
  
  return { 
    x: Math.max(margin, Math.min(scaledX, maxX)), 
    y: Math.max(margin, Math.min(scaledY, maxY)) 
  }
}
