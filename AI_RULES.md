# AI_RULES.md

## Tech Stack (5-10 bullet points)
- **React** with **TypeScript** for the frontend UI.
- **React Router** for client‑side routing (routes defined in `src/App.tsx`).
- **Tailwind CSS** for styling and layout throughout the app.
- **shadcn/ui** component library (pre‑built UI components, Radix UI primitives underneath).
- **lucide-react** for SVG icons.
- **Vite** (or Create‑React‑App) as the build tool (standard for this starter).
- **ESLint + Prettier** for code quality and formatting.
- **Jest / React Testing Library** for unit tests (if present).
- **Git** for version control.

## Library Usage Rules
1. **UI Components** – Use shadcn/ui components for all UI elements (buttons, dialogs, forms, tables, etc.). Import directly from `@/components/ui/*` and avoid creating duplicate UI primitives.
2. **Icons** – Use the `lucide-react` package for icons. Prefer the named exports (e.g., `import { Search } from "lucide-react"`).
3. **Styling** – Apply layout and visual styles with Tailwind CSS utility classes. Do not write custom CSS files unless absolutely necessary.
4. **Routing** – All routes must be declared in `src/App.tsx` using `react-router-dom`. Do not create additional router files.
5. **State Management** – Use React's built‑in `useState`, `useReducer`, or Context API. Do not add external state libraries unless the project explicitly requires them.
6. **Data Fetching** – Use the native `fetch` API or `axios` (if already installed). Keep data‑fetching logic inside React components or custom hooks under `src/hooks/`.
7. **Component Organization** – Place page components in `src/pages/` and reusable UI components in `src/components/`. Keep each component in its own file.
8. **Type Safety** – All new code must be typed with TypeScript. Avoid using `any` unless a temporary workaround is explicitly justified and will be removed later.
9. **Accessibility** – Leverage the accessibility features built into shadcn/ui and Radix UI. Ensure interactive elements have appropriate ARIA attributes.
10. **Security** – Never interpolate user‑provided data directly into HTML or SQL queries. Sanitize any external input before rendering.
