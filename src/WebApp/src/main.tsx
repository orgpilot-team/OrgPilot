import { lazy, StrictMode, Suspense } from 'react'
import { createRoot } from 'react-dom/client'
import { AppProviders } from './app/AppProviders'
import './shared/design-system/styles/fonts.css'
import './shared/design-system/styles/globals.css'

const rootElement = document.getElementById('root')

if (!rootElement) {
  throw new Error('The application root element is missing.')
}

const DesignSystemLab = import.meta.env.DEV && /^\/design-system\/?$/.test(window.location.pathname)
  ? lazy(() => import('./app/design-system-lab/DesignSystemLab'))
  : null

createRoot(rootElement).render(
  <StrictMode>
    <AppProviders>
      {DesignSystemLab ? (
        <Suspense fallback={null}>
          <DesignSystemLab />
        </Suspense>
      ) : (
        <main>
          <h1>OrgPilot</h1>
        </main>
      )}
    </AppProviders>
  </StrictMode>,
)
