# Frontend Code Rule

**Path Scope:** `src/frontend/**/*.{js,jsx,ts,tsx,css,scss}`

**Severity:** STANDARD

---

## Rule: Frontend Code Standards

All frontend code must follow these standards for consistency, maintainability, and quality.

---

## Component Structure

### File Organization

```
src/frontend/
├── components/          # Reusable UI components
│   ├── common/          # Generic components (Button, Input, etc.)
│   ├── layout/          # Layout components (Header, Footer, etc.)
│   └── features/        # Feature-specific components
├── pages/               # Page-level components
├── hooks/               # Custom React hooks
├── services/            # API service clients
├── utils/               # Utility functions
└── styles/              # Global styles and design tokens
```

### Component File Template

```typescript
// components/common/Button.tsx
import React from 'react';
import styled from 'styled-components';
import { colors, spacing } from '../../styles/tokens';

interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'small' | 'medium' | 'large';
  disabled?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}

/**
 * Button component for user interactions.
 * 
 * @example
 * <Button variant="primary" onClick={handleClick}>
 *   Click me
 * </Button>
 */
export function Button({
  variant = 'primary',
  size = 'medium',
  disabled = false,
  onClick,
  children,
}: ButtonProps) {
  return (
    <StyledButton
      variant={variant}
      size={size}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </StyledButton>
  );
}

const StyledButton = styled.button<ButtonProps>`
  /* styles using design tokens */
`;
```

---

## Design System

### Use Design Tokens

```typescript
// GOOD - Use design tokens
import { colors, spacing, typography } from '../styles/tokens';

const StyledButton = styled.button`
  color: ${colors.text.primary};
  padding: ${spacing.medium};
  font-size: ${typography.body};
`;

// BAD - Hardcoded values
const StyledButton = styled.button`
  color: #333;  /* Don't do this */
  padding: 16px;  /* Don't do this */
`;
```

### Color Tokens

```typescript
// styles/tokens.ts
export const colors = {
  primary: {
    main: '#1976d2',
    light: '#42a5f5',
    dark: '#1565c0',
  },
  secondary: {
    main: '#9c27b0',
    light: '#ba68c8',
    dark: '#7b1fa2',
  },
  text: {
    primary: '#212121',
    secondary: '#757575',
    disabled: '#9e9e9e',
  },
  background: {
    default: '#ffffff',
    paper: '#f5f5f5',
  },
  error: {
    main: '#f44336',
    light: '#e57373',
  },
  success: {
    main: '#4caf50',
    light: '#81c784',
  },
};
```

---

## State Management

### Local State

Use `useState` for component-local state:

```typescript
function Counter() {
  const [count, setCount] = useState(0);
  
  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}
```

### Global State

Use context or state library for shared state:

```typescript
// contexts/UserContext.tsx
const UserContext = createContext<User | null>(null);

export function UserProvider({ children }) {
  const [user, setUser] = useState<User | null>(null);
  
  return (
    <UserContext.Provider value={{ user, setUser }}>
      {children}
    </UserContext.Provider>
  );
}

export function useUser() {
  return useContext(UserContext);
}
```

---

## API Integration

### Use Service Hooks

```typescript
// hooks/useApi.ts
export function useApi<T>(endpoint: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    fetch(endpoint)
      .then(res => res.json())
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [endpoint]);

  return { data, loading, error };
}

// Usage in component
function UserProfile() {
  const { data: user, loading, error } = useApi<User>('/api/users/me');
  
  if (loading) return <Loading />;
  if (error) return <Error message={error.message} />;
  return <UserDetails user={user} />;
}
```

---

## Accessibility

### Required Attributes

```typescript
// Images must have alt
<img src="logo.png" alt="Company logo" />

// Buttons must have accessible labels
<button aria-label="Close dialog">
  <XIcon />
</button>

// Form inputs must have labels
<label htmlFor="email">Email</label>
<input id="email" type="email" />

// Or use aria-label
<input aria-label="Search" type="search" />
```

### Keyboard Navigation

```typescript
// Ensure interactive elements are focusable
<button tabIndex={0} onClick={handleClick}>
  Click me
</button>

// Handle keyboard events
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      handleClick();
    }
  }}
>
  Custom button
</div>
```

---

## Testing

### Component Tests

```typescript
// Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('renders with correct text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('handles click events', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click</Button>);
    fireEvent.click(screen.getByText('Click'));
    expect(handleClick).toHaveBeenCalled();
  });

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click</Button>);
    expect(screen.getByText('Click')).toBeDisabled();
  });
});
```

---

## Performance

### Memoization

```typescript
// Memo expensive components
const ExpensiveList = React.memo(function ExpensiveList({ items }) {
  return (
    <ul>
      {items.map(item => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  );
});

// Memo expensive computations
function Component({ data }) {
  const processedData = useMemo(() => {
    return data.map(transformItem);
  }, [data]);
  
  return <List items={processedData} />;
}
```

### Lazy Loading

```typescript
// Lazy load heavy components
const HeavyChart = React.lazy(() => import('./HeavyChart'));

function Dashboard() {
  return (
    <Suspense fallback={<Loading />}>
      <HeavyChart />
    </Suspense>
  );
}
```

---

## Anti-Patterns to Avoid

1. **Inline Styles**: Use design system tokens
2. **Direct API Calls**: Use hooks/services
3. **Missing Error States**: Always handle loading/error
4. **Missing Accessibility**: Include ARIA, labels
5. **Uncontrolled State**: Avoid direct mutations
6. **Large Components**: Extract to smaller units
7. **Missing Tests**: Test critical paths
8. **Hardcoded Values**: Use constants/config