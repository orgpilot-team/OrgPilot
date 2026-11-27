import { Handle, Position } from '@xyflow/react'
import type { Node, NodeProps } from '@xyflow/react'
import '@xyflow/react/dist/style.css'
import './workflow-theme.css'

export type WorkflowStage = Node<{
  stage: string
  title: string
  status: 'normal' | 'active' | 'warning' | 'critical' | 'complete'
  statusLabel: string
  hasIncoming?: boolean
  hasOutgoing?: boolean
}, 'stage'>

export function WorkflowNode({ data, selected }: NodeProps<WorkflowStage>) {
  return (
    <div className="didrah-flow-stage" data-status={data.status} data-selected={selected}>
      {data.hasIncoming && <Handle type="target" position={Position.Right} isConnectable={false} />}
      <span className="didrah-flow-stage-label">{data.stage}</span>
      <strong>{data.title}</strong>
      <span className="didrah-flow-stage-status">{data.statusLabel}</span>
      {data.hasOutgoing && <Handle type="source" position={Position.Left} isConnectable={false} />}
    </div>
  )
}
