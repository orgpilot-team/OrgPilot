import { Alert, Empty, Skeleton } from 'antd'
import type { ReactNode } from 'react'
import './patterns.css'

type PanelStateProps = {
  kind: 'empty' | 'error' | 'success' | 'warning'
  title: string
  description?: ReactNode
  action?: ReactNode
} | {
  kind: 'loading'
  title: string
}

export function PanelState(props: PanelStateProps) {
  if (props.kind === 'loading') {
    return (
      <div className="didrah-panel-loading" role="status">
        <span className="didrah-panel-state-title">{props.title}</span>
        <div aria-hidden="true">
          <Skeleton title={false} paragraph={{ rows: 3 }} />
        </div>
      </div>
    )
  }

  const { kind, title, description, action } = props

  if (kind === 'empty') {
    return (
      <Empty
        image={Empty.PRESENTED_IMAGE_SIMPLE}
        description={
          <div className="didrah-panel-empty" role="status">
            <span className="didrah-panel-state-title">{title}</span>
            {description && <div>{description}</div>}
          </div>
        }
      >
        {action}
      </Empty>
    )
  }

  return <Alert type={kind} showIcon title={title} description={description} action={action} />
}
