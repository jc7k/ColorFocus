# Tech Stack

## Frontend

### Framework & Language
- **Framework:** React 18+ with TypeScript
- **Rationale:** React's component model supports building accessible, reusable UI components. TypeScript provides type safety critical for ensuring color tokens and puzzle data structures remain consistent across the application.

### Styling
- **CSS Framework:** Tailwind CSS
- **Rationale:** Tailwind's utility-first approach enables rapid iteration on accessibility features like spacing, font sizes, and color contrast. Custom color tokens can be defined in the Tailwind config for consistent use of the color-blind-safe palette.

### UI Components
- **Component Library:** Custom components built on accessible primitives
- **Rationale:** Given the strict accessibility requirements for older adults and users with visual impairments, custom components ensure full control over focus management, font sizing, contrast ratios, and interaction patterns. Third-party component libraries may not meet the specific accessibility guarantees required.

### State Management
- **Approach:** React Context + hooks for global state, component state for local concerns
- **Rationale:** The application has relatively simple state requirements (current puzzle, user session, settings). Heavy state management libraries are unnecessary overhead.

## Backend

### Framework & Language
- **Framework:** FastAPI (Python)
- **Language:** Python 3.11+
- **Rationale:** Python excels at algorithmic puzzle generation and scientific computing. FastAPI provides modern async support, automatic OpenAPI documentation, and strong typing with Pydantic models.

### Dependency Management
- **Package Manager:** uv with pyproject.toml
- **Rationale:** Modern Python dependency management with faster resolution and reproducible builds. Never use pip directly.

### Runtime
- **Execution:** Always use `uv run` or activate project `.venv`
- **Rationale:** Ensures consistent environment and dependency isolation across development and deployment.

### API Design
- **Style:** RESTful JSON API
- **Documentation:** Auto-generated OpenAPI/Swagger via FastAPI
- **Rationale:** Simple resource-based endpoints for puzzles, users, and progress data. OpenAPI documentation supports frontend development and potential third-party integrations.

## Database & Storage

### Primary Database
- **Database:** PostgreSQL 15+
- **Rationale:** Robust relational database for user accounts, puzzle history, scoring data, and caregiver relationships. Strong support for JSON columns enables flexible storage of puzzle configurations and detailed metrics.

### ORM
- **Library:** SQLAlchemy 2.0 with async support
- **Rationale:** Mature ORM with excellent PostgreSQL support. Async capabilities align with FastAPI's async architecture for optimal performance.

### Caching
- **Strategy:** Application-level caching for generated puzzles
- **Rationale:** Puzzle generation is deterministic given seed parameters. Caching avoids regeneration overhead. Redis may be added in Phase 2 if caching requirements grow.

## Testing & Quality

### Frontend Testing
- **Framework:** Vitest
- **Component Testing:** React Testing Library
- **Rationale:** Vitest provides fast, modern testing with excellent TypeScript support. React Testing Library encourages testing components as users interact with them, which aligns with accessibility-focused development.

### Backend Testing
- **Framework:** pytest
- **Coverage:** pytest-cov
- **Rationale:** pytest is the standard for Python testing with excellent fixture support for database and API testing.

### Accessibility Testing
- **Tools:** axe-core integration, manual screen reader testing
- **Rationale:** Automated accessibility scanning catches common issues. Manual testing with screen readers (NVDA, VoiceOver) validates real-world accessibility for target users.

### Linting & Formatting
- **Frontend:** ESLint + Prettier
- **Backend:** Ruff (linting and formatting)
- **Rationale:** Consistent code style enforced automatically. Ruff provides fast Python linting with modern rule sets.

### Type Checking
- **Frontend:** TypeScript strict mode
- **Backend:** mypy with strict configuration
- **Rationale:** Strong typing catches errors early and improves maintainability, especially important for color token handling and puzzle data structures.

## Deployment & Infrastructure

### Frontend Hosting
- **Platform:** Vercel
- **Rationale:** Optimized for React applications with excellent performance, automatic HTTPS, and simple deployment from Git. Edge network ensures fast loading for users regardless of location.

### Backend Hosting
- **Platform:** Railway
- **Rationale:** Simple container-based deployment with managed PostgreSQL. Straightforward scaling and environment management without complex infrastructure setup.

### CI/CD
- **Platform:** GitHub Actions
- **Rationale:** Integrated with repository for automated testing, linting, and deployment on push. Workflows for both frontend and backend validation.

### Environment Configuration
- **Approach:** Environment variables via platform secrets
- **Rationale:** Sensitive configuration (database URLs, API keys) never committed to version control. Both Vercel and Railway provide secure environment variable management.

## Third-Party Services

### Authentication
- **Approach:** Custom JWT-based authentication
- **Rationale:** Simple user accounts without social login complexity. Custom implementation ensures full control over session management and caregiver linking logic.

### PDF Generation
- **Library:** WeasyPrint (Python) or react-pdf (frontend)
- **Rationale:** Server-side PDF generation for progress reports ensures consistent formatting. Client-side generation may be used for individual puzzle printing.

### Monitoring
- **Error Tracking:** Sentry
- **Rationale:** Production error tracking with context for debugging. Important for identifying accessibility issues that may only manifest for specific user configurations.

## Architecture Decisions

### Monorepo Structure
```
/
  frontend/          # React application
  backend/           # FastAPI application
  shared/            # Shared types/schemas (if needed)
```
- **Rationale:** Keeps related code together while maintaining clear separation of concerns.

### Color Token Implementation
- Color tokens defined as constants in both frontend and backend
- Shared color definitions ensure consistency between generation and display
- HSL values chosen for consistent brightness variants

### Accessibility-First Patterns
- All interactive elements keyboard accessible
- ARIA attributes for screen reader support
- Focus indicators clearly visible
- No information conveyed by color alone (text labels always present)
- Minimum contrast ratios exceed WCAG AAA standards
