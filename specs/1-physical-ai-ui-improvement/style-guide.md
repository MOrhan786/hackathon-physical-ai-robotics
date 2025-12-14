# Physical AI UI Style Guide

## Overview
This document outlines the design system and UI components for the Physical AI website. It provides guidelines for consistent styling across all pages and components.

## Color Palette

### Primary Colors
- **Primary**: `#6366f1` (Indigo)
- **Primary Dark**: `#4f46e5`
- **Primary Darker**: `#4338ca`
- **Primary Darkest**: `#3730a3`
- **Primary Light**: `#818cf8`
- **Primary Lighter**: `#a5b4fc`
- **Primary Lightest**: `#c7d2fe`

### Secondary Colors
- **Secondary**: `#34a853` (Green)
- **Accent**: `#fbbc05` (Yellow)

### Neutral Colors
- **Text Primary**: `#202124`
- **Text Secondary**: `#5f6368`
- **Background**: `#ffffff`
- **Background Elevated**: `#f8f9fa`

### Functional Colors
- **Success**: `#34a853`
- **Warning**: `#fbbc05`
- **Error**: `#ea4335`

## Typography

### Font Family
- **Primary Font**: Inter (imported from Google Fonts)
- **Fallback**: system-ui, -apple-system, sans-serif

### Font Sizes
- **XS**: 12px (`0.75rem`)
- **SM**: 14px (`0.875rem`)
- **Base**: 16px (`1rem`)
- **LG**: 18px (`1.125rem`)
- **XL**: 20px (`1.25rem`)
- **2XL**: 24px (`1.5rem`)
- **3XL**: 30px (`1.875rem`)
- **4XL**: 36px (`2.25rem`)

### Hierarchy
- **H1**: 36px-56px (responsive with clamp), Weight: 700
- **H2**: 28px-40px (responsive with clamp), Weight: 600
- **H3**: 24px, Weight: 600
- **H4**: 20px, Weight: 600
- **Body**: 16px, Weight: 400

## Spacing System

### Spacing Scale
- **XS**: 4px (`0.25rem`)
- **SM**: 8px (`0.5rem`)
- **MD**: 16px (`1rem`)
- **LG**: 24px (`1.5rem`)
- **XL**: 32px (`2rem`)
- **2XL**: 48px (`3rem`)

## Responsive Breakpoints

- **SM**: 576px
- **MD**: 768px
- **LG**: 992px
- **XL**: 1200px

## Component Guidelines

### Buttons
- **Primary**: Gradient background with primary colors, pill-shaped (50px border-radius)
- **Hover Effect**: Slight elevation and enhanced shadow
- **Padding**: 0.6rem 1.5rem
- **Font Weight**: 600

### Cards
- **Border**: 1px solid emphasis color
- **Shadow**: Light shadow by default, enhanced on hover
- **Hover Effect**: Slight elevation and primary border color
- **Border Radius**: 12px

### Navigation
- **Glass Effect**: With backdrop filter for blur effect
- **Border**: Bottom border with emphasis color
- **Height**: 64px

## Accessibility Standards

### Focus Indicators
- **Width**: 3px
- **Color**: Primary color
- **Offset**: 2px
- **Style**: Solid outline

### Contrast Ratios
- All text elements maintain WCAG 2.1 AA compliant contrast ratios
- Minimum 4.5:1 for normal text, 3:1 for large text

## Utility Classes

### Spacing Utilities
- `.m-{size}`: margin
- `.p-{size}`: padding
- `.mt-{size}`: margin-top
- `.mb-{size}`: margin-bottom
- `.ml-{size}`: margin-left
- `.mr-{size}`: margin-right
- `.pt-{size}`: padding-top
- `.pb-{size}`: padding-bottom
- `.pl-{size}`: padding-left
- `.pr-{size}`: padding-right

### Color Utilities
- `.text-{color}`: text color
- `.bg-{color}`: background color

### Layout Utilities
- `.d-flex`, `.d-none`, etc.: display utilities
- `.w-100`, `.h-100`: sizing utilities
- `.text-center`, `.text-left`, `.text-right`: text alignment

### Responsive Utilities
- `.d-sm-flex`, `.d-md-flex`, etc.: responsive display utilities based on breakpoints

## CSS Custom Properties

All design tokens are available as CSS custom properties (CSS variables) prefixed with `--pai-` for Physical AI components or `--ifm-` for Docusaurus components.