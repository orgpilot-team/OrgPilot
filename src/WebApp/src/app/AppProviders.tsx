import { App, ConfigProvider } from 'antd'
import faIR from 'antd/locale/fa_IR'
import type { PropsWithChildren } from 'react'
import { antControlConfig, antThemes } from '../shared/design-system/theme/ant-theme'
import { DidrahThemeProvider, useDidrahTheme } from '../shared/design-system/theme/DidrahThemeProvider'

function AntProviders({ children }: PropsWithChildren) {
  const { theme } = useDidrahTheme()

  return (
    <ConfigProvider direction="rtl" locale={faIR} theme={antThemes[theme]} {...antControlConfig}>
      <App>{children}</App>
    </ConfigProvider>
  )
}

export function AppProviders({ children }: PropsWithChildren) {
  return (
    <DidrahThemeProvider>
      <AntProviders>{children}</AntProviders>
    </DidrahThemeProvider>
  )
}
