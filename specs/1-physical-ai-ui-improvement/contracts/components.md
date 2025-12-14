# Component Interface Contract: Physical AI Home Page UI Components

## Purpose
This contract defines the interface, styling, and behavior standards for UI components used in the Physical AI home page improvements. All new components must adhere to these standards to ensure consistency and maintainability.

## Component Naming Convention
- Use PascalCase for React components: `HomepageHero`, `FeatureCard`
- Use kebab-case for CSS classes: `homepage-hero`, `feature-card`
- Prefix custom classes with `pai-` (Physical AI): `pai-button-primary`, `pai-card-featured`

## HomepageHero Component Contract

### Props Interface
```typescript
interface HomepageHeroProps {
  title: string;           // Main headline text
  subtitle: string;        // Supporting text
  primaryButton?: {
    text: string;          // Button text
    href: string;          // Destination URL
    variant?: 'primary' | 'secondary'; // Button style
  };
  secondaryButton?: {
    text: string;          // Button text
    href: string;          // Destination URL
  };
  backgroundImage?: string; // Optional background image URL
  className?: string;      // Additional CSS classes
}
```

### Styling Requirements
- Must support light and dark mode
- Text must meet WCAG 2.1 AA contrast ratios
- Responsive layout for all screen sizes
- Hover and focus states for interactive elements
- Minimum touch target size of 44px

### Behavior Specifications
- Primary button should have prominent styling
- Hover state: subtle elevation or color shift
- Focus state: visible focus ring for accessibility
- Animation duration: 300ms for transitions

## FeatureCard Component Contract

### Props Interface
```typescript
interface FeatureCardProps {
  title: string;           // Card title
  description: string;     // Card description
  icon?: React.ReactNode;  // Optional icon component
  link?: {
    text: string;          // Link text
    href: string;          // Destination URL
  };
  variant?: 'default' | 'highlight'; // Visual variant
  className?: string;      // Additional CSS classes
}
```

### Styling Requirements
- Consistent spacing and padding
- Card shadow for depth perception
- Hover effect for interactive cards
- Responsive grid layout
- Accessibility-compliant colors

## Button Component Contract

### Props Interface
```typescript
interface ButtonProps {
  children: React.ReactNode; // Button content
  variant?: 'primary' | 'secondary' | 'tertiary'; // Style variant
  size?: 'small' | 'medium' | 'large'; // Size variant
  disabled?: boolean;      // Disabled state
  href?: string;          // For link buttons
  onClick?: () => void;   // Click handler
  className?: string;     // Additional CSS classes
}
```

### Styling Requirements
- Consistent padding based on size
- Proper color contrast in all states
- Focus indicators for keyboard navigation
- Disabled state with reduced opacity
- Smooth transitions between states

## CSS Custom Properties Contract

### Color Variables
```css
:root {
  /* Primary Colors */
  --pai-color-primary: #1a73e8;
  --pai-color-primary-light: #4285f4;
  --pai-color-primary-dark: #0d62c9;

  /* Secondary Colors */
  --pai-color-secondary: #34a853;
  --pai-color-accent: #fbbc05;

  /* Neutral Colors */
  --pai-color-text-primary: #202124;
  --pai-color-text-secondary: #5f6368;
  --pai-color-background: #ffffff;
  --pai-color-background-elevated: #f8f9fa;

  /* Functional Colors */
  --pai-color-success: #34a853;
  --pai-color-warning: #fbbc05;
  --pai-color-error: #ea4335;
}
```

### Spacing Scale
```css
:root {
  --pai-spacing-xs: 0.25rem;   /* 4px */
  --pai-spacing-sm: 0.5rem;    /* 8px */
  --pai-spacing-md: 1rem;      /* 16px */
  --pai-spacing-lg: 1.5rem;    /* 24px */
  --pai-spacing-xl: 2rem;      /* 32px */
  --pai-spacing-2xl: 3rem;     /* 48px */
}
```

### Typography Scale
```css
:root {
  --pai-font-size-xs: 0.75rem;   /* 12px */
  --pai-font-size-sm: 0.875rem;  /* 14px */
  --pai-font-size-base: 1rem;    /* 16px */
  --pai-font-size-lg: 1.125rem;  /* 18px */
  --pai-font-size-xl: 1.25rem;   /* 20px */
  --pai-font-size-2xl: 1.5rem;   /* 24px */
  --pai-font-size-3xl: 1.875rem; /* 30px */
  --pai-font-size-4xl: 2.25rem;  /* 36px */
}
```

## Responsive Breakpoints
```css
:root {
  --pai-breakpoint-sm: 576px;
  --pai-breakpoint-md: 768px;
  --pai-breakpoint-lg: 992px;
  --pai-breakpoint-xl: 1200px;
}
```

## Accessibility Standards
- All interactive elements must have discernible names
- Color must not be the only means of conveying information
- Sufficient color contrast (4.5:1 for normal text, 3:1 for large text)
- Focus indicators visible for keyboard navigation
- Semantic HTML elements used appropriately
- ARIA attributes where necessary for complex components