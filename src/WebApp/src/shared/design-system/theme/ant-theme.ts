import { CheckOutlined } from '@ant-design/icons'
import { theme as ant } from 'antd'
import type { ConfigProviderProps, ThemeConfig } from 'antd'
import { createElement } from 'react'
import { darkTheme } from '../tokens/dark-theme'
import { layout, overlayShadow } from '../tokens/layout'
import { lightTheme } from '../tokens/light-theme'
import type { ThemeColors, ThemeName } from '../tokens/theme-contract'
import { typography } from '../tokens/typography'
import './ant-controls.css'
import './ant-selection-overlays.css'

const { roles } = typography
const toAntPixels = (size: (typeof roles)[keyof typeof roles]['size']) => Number.parseFloat(size) * 16

const fieldClassNames = { root: 'didrah-ant-field' }

export const antControlConfig = {
  button: { classNames: { root: 'didrah-ant-button' } },
  input: { classNames: fieldClassNames },
  textArea: { classNames: fieldClassNames },
  inputNumber: { classNames: { ...fieldClassNames, input: 'didrah-ant-number-editor' } },
  select: {
    classNames: { ...fieldClassNames, popup: { root: 'didrah-ant-select-popup' } },
    menuItemSelectedIcon: createElement(CheckOutlined, { 'aria-hidden': true }),
  },
  checkbox: { classNames: { icon: 'didrah-ant-choice' } },
  radio: { classNames: { icon: 'didrah-ant-choice' } },
  switch: { classNames: { root: 'didrah-ant-switch' } },
  segmented: { classNames: { root: 'didrah-ant-segmented', item: 'didrah-ant-segment' } },
  modal: { classNames: { container: 'didrah-ant-dialog' } },
  drawer: { classNames: { section: 'didrah-ant-dialog' } },
  dropdown: { classNames: { menu: 'didrah-ant-popup', item: 'didrah-ant-menu-item' } },
  popover: { classNames: { container: 'didrah-ant-popup' } },
  tooltip: { classNames: { container: 'didrah-ant-tooltip' } },
} satisfies ConfigProviderProps

function createAntTheme(name: ThemeName, colors: ThemeColors): ThemeConfig {
  const isDark = name === 'dark'
  const primary = colors['brand-primary']
  const accent = isDark ? colors['brand-indigo'] : primary
  const focus = colors['focus-ring']
  const input = colors['surface-input']
  const raised = colors['surface-raised']
  const selected = colors['surface-selected']
  const text = colors['text-primary']
  const secondary = colors['text-secondary']
  const muted = colors['text-muted']
  const border = colors['border-subtle']
  const surface = colors['surface-base']
  const success = colors['status-success']
  const warning = colors['status-warning']
  const error = colors['status-critical']
  const info = colors['status-information']
  const tint = (color: string, amount: number) => `color-mix(in srgb, ${color} ${amount}%, ${surface})`
  const status = {
    colorSuccess: success,
    colorWarning: warning,
    colorError: error,
    colorInfo: info,
    colorSuccessBg: tint(success, 8),
    colorWarningBg: tint(warning, 8),
    colorErrorBg: tint(error, 8),
    colorInfoBg: tint(info, 8),
    colorSuccessBorder: tint(success, 24),
    colorWarningBorder: tint(warning, 24),
    colorErrorBorder: tint(error, 24),
    colorInfoBorder: tint(info, 24),
  }
  const field = {
    colorTextPlaceholder: 'var(--didrah-control-muted)',
    colorTextDisabled: 'var(--didrah-control-muted)',
  }
  const inputField = {
    ...field,
    paddingInline: layout.space.gap,
  }
  const choice = {
    colorBorder: 'var(--didrah-control-edge)',
    colorBgContainer: 'var(--didrah-control-fill)',
    colorBgContainerDisabled: 'var(--didrah-control-disabled)',
    colorPrimaryBorder: focus,
    colorPrimary: isDark ? '#5162c6' : '#3e50ac',
    colorPrimaryHover: isDark ? '#6072d6' : '#35499d',
  }
  const overlay = colors['surface-overlay']

  return {
    algorithm: isDark ? ant.darkAlgorithm : ant.defaultAlgorithm,
    cssVar: { key: 'didrah' },
    token: {
      colorPrimary: primary,
      colorPrimaryText: accent,
      colorPrimaryBorder: focus,
      colorLink: accent,
      colorSuccess: success,
      colorWarning: warning,
      colorError: error,
      colorInfo: info,
      colorText: text,
      colorTextSecondary: secondary,
      colorTextTertiary: muted,
      colorTextPlaceholder: muted,
      colorTextDisabled: muted,
      colorTextLightSolid: colors['brand-on-primary'],
      colorBgLayout: colors.canvas,
      colorBgContainer: surface,
      colorBgContainerDisabled: raised,
      colorBgElevated: colors['surface-overlay'],
      colorBgMask: `${darkTheme.canvas}99`,
      colorBorder: colors['border-control'],
      colorBorderSecondary: border,
      colorSplit: border,
      controlItemBgHover: raised,
      controlItemBgActive: selected,
      controlOutline: `${focus}40`,
      controlOutlineWidth: 2,
      fontFamily: typography.family,
      fontFamilyCode: typography.family,
      fontSize: toAntPixels(roles.body.size),
      fontSizeSM: toAntPixels(roles['table-compact'].size),
      fontSizeLG: toAntPixels(roles['body-large'].size),
      fontSizeHeading1: toAntPixels(roles['heading-1'].size),
      fontSizeHeading2: toAntPixels(roles['heading-2'].size),
      fontSizeHeading3: toAntPixels(roles['heading-3'].size),
      lineHeight: roles.body.lineHeight,
      fontWeightStrong: roles.control.weight,
      borderRadius: layout.radius.control,
      controlHeight: layout.controlHeight,
      boxShadowSecondary: overlayShadow(name, colors),
    },
    components: {
      Button: {
        primaryShadow: 'none',
        defaultShadow: 'none',
        dangerShadow: 'none',
        paddingInline: layout.space.inset - 2,
        fontSize: toAntPixels(roles.control.size),
        fontWeight: roles.control.weight,
      },
      Input: inputField,
      InputNumber: {
        ...inputField,
        handleVisible: true,
        handleWidth: 24,
        handleBg: 'var(--didrah-control-secondary)',
        handleActiveBg: 'var(--didrah-control-secondary-pressed)',
        handleHoverColor: text,
        handleBorderColor: 'var(--didrah-control-edge-disabled)',
      },
      Select: {
        ...field,
        paddingSM: layout.space.gap + 1,
        optionHeight: 34,
        optionPadding: '5px 10px',
        optionSelectedColor: text,
        optionActiveBg: 'var(--didrah-control-option-active)',
        optionSelectedBg: 'var(--didrah-control-option-selected)',
        controlItemBgActiveHover: 'var(--didrah-control-option-selected-active)',
      },
      DatePicker: {
        colorBgContainer: input,
        colorBorder: isDark ? muted : colors['border-control'],
        hoverBorderColor: accent,
        activeBorderColor: focus,
      },
      Checkbox: choice,
      Radio: { ...choice, dotColorDisabled: muted },
      Switch: {
        ...choice,
        colorTextQuaternary: 'var(--didrah-control-edge)',
        colorTextTertiary: 'var(--didrah-control-edge-hover)',
        handleShadow: 'none',
      },
      Segmented: {
        trackBg: 'var(--didrah-control-fill)',
        trackPadding: 3,
        itemColor: secondary,
        itemHoverColor: text,
        itemHoverBg: 'var(--didrah-control-hover)',
        itemActiveBg: 'var(--didrah-control-option-active)',
        itemSelectedBg: 'var(--didrah-control-option-selected)',
        itemSelectedColor: text,
      },
      Modal: {
        contentBg: overlay,
        headerBg: 'transparent',
        footerBg: 'transparent',
        titleColor: text,
        borderRadiusLG: layout.radius.panel,
      },
      Drawer: { colorBgElevated: overlay, colorSplit: border },
      Dropdown: { colorBgElevated: overlay, controlItemBgHover: raised },
      Popover: { colorBgElevated: overlay, colorText: text },
      Tag: status,
      Alert: status,
      Menu: {
        itemSelectedBg: selected,
        itemSelectedColor: text,
        horizontalItemSelectedColor: accent,
        horizontalItemHoverColor: accent,
      },
      Table: {
        headerBg: raised,
        headerColor: secondary,
        rowHoverBg: raised,
        fontSize: toAntPixels(roles.table.size),
        lineHeight: roles.table.lineHeight,
        cellPaddingBlock: 10,
        cellPaddingInline: layout.space.gap,
      },
      Tooltip: {
        colorBgSpotlight: overlay,
        colorTextLightSolid: text,
      },
    },
  }
}

export const antThemes = {
  dark: createAntTheme('dark', darkTheme),
  light: createAntTheme('light', lightTheme),
} satisfies Record<ThemeName, ThemeConfig>
