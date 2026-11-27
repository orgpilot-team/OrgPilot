import { createContext, useContext, useEffect, useLayoutEffect, useState } from 'react'
import type { PropsWithChildren } from 'react'
import { darkTheme } from '../tokens/dark-theme'
import { lightTheme } from '../tokens/light-theme'
import type { ThemeColors, ThemeName } from '../tokens/theme-contract'
import { applyLayout, applyThemeVariables, applyTypography } from './css-variables'

type ThemeContextValue = {
  theme: ThemeName
  colors: ThemeColors
  setTheme: (theme: ThemeName) => void
}

const themes = { dark: darkTheme, light: lightTheme } satisfies Record<ThemeName, ThemeColors>
const ThemeContext = createContext<ThemeContextValue | null>(null)
const themeStorageKey = 'didrah-theme'

function readStoredTheme(): ThemeName {
  try {
    return window.localStorage.getItem(themeStorageKey) === 'light' ? 'light' : 'dark'
  } catch {
    return 'dark'
  }
}

export function DidrahThemeProvider({ children }: PropsWithChildren) {
  const [theme, setTheme] = useState<ThemeName>(readStoredTheme)
  const colors = themes[theme]

  useLayoutEffect(() => applyTypography(document.documentElement.style), [])
  useLayoutEffect(() => applyLayout(document.documentElement.style), [])

  useLayoutEffect(() => {
    const root = document.documentElement
    const clearTheme = applyThemeVariables(root.style, theme, colors)
    root.dataset.theme = theme
    root.style.colorScheme = theme

    return () => {
      clearTheme()
      delete root.dataset.theme
      root.style.removeProperty('color-scheme')
    }
  }, [theme, colors])

  useEffect(() => {
    try {
      window.localStorage.setItem(themeStorageKey, theme)
    } catch {
      // Theme changes still apply when browser storage is unavailable.
    }
  }, [theme])

  return <ThemeContext.Provider value={{ theme, colors, setTheme }}>{children}</ThemeContext.Provider>
}

export function useDidrahTheme() {
  const context = useContext(ThemeContext)

  if (!context) {
    throw new Error('useDidrahTheme requires DidrahThemeProvider.')
  }

  return context
}
