import { Background, BackgroundVariant, Controls, MarkerType, ReactFlow } from '@xyflow/react'
import type { AriaLabelConfig, DefaultEdgeOptions, Edge } from '@xyflow/react'
import { Panel, SectionHeader } from '../../shared/design-system/patterns/Panel'
import { useDidrahTheme } from '../../shared/design-system/theme/DidrahThemeProvider'
import { WorkflowNode } from '../../shared/visualization/workflow/WorkflowNode'
import type { WorkflowStage } from '../../shared/visualization/workflow/WorkflowNode'

const stages: WorkflowStage[] = [
  { id: 'detection', type: 'stage', position: { x: 832, y: 84 }, data: {
    stage: 'تشخیص', title: 'افت فروش ونک', status: 'critical', statusLabel: 'بحرانی', hasOutgoing: true,
  } },
  { id: 'evidence', type: 'stage', position: { x: 624, y: 84 }, data: {
    stage: 'شواهد', title: 'گزارش سه‌شنبه', status: 'complete', statusLabel: 'تکمیل‌شده', hasIncoming: true, hasOutgoing: true,
  } },
  { id: 'recommendation', type: 'stage', position: { x: 416, y: 84 }, data: {
    stage: 'پیشنهاد هوش مصنوعی', title: 'بررسی موجودی قفسه', status: 'active', statusLabel: 'فعال', hasIncoming: true, hasOutgoing: true,
  } },
  { id: 'decision', type: 'stage', position: { x: 208, y: 84 }, data: {
    stage: 'تصمیم مدیر', title: 'تأیید اقدام اصلاحی', status: 'warning', statusLabel: 'نیاز به تصمیم', hasIncoming: true, hasOutgoing: true,
  } },
  { id: 'follow-up', type: 'stage', position: { x: 0, y: 16 }, data: {
    stage: 'نتیجه · در صورت تأیید', title: 'پیگیری فروش شعبه', status: 'normal', statusLabel: 'در انتظار', hasIncoming: true,
  } },
  { id: 'referral', type: 'stage', position: { x: 0, y: 150 }, data: {
    stage: 'نتیجه · مسیر جایگزین', title: 'ارجاع به مدیر منطقه', status: 'normal', statusLabel: 'در انتظار', hasIncoming: true,
  } },
]

const nodes = stages.map((stage) => ({
  ...stage,
  ariaLabel: `${stage.data.stage}، ${stage.data.title}، ${stage.data.statusLabel}`,
}))
const edges: Edge[] = [
  { id: 'detection-evidence', source: 'detection', target: 'evidence' },
  { id: 'evidence-recommendation', source: 'evidence', target: 'recommendation' },
  { id: 'recommendation-decision', source: 'recommendation', target: 'decision' },
  { id: 'decision-follow-up', source: 'decision', target: 'follow-up' },
  { id: 'decision-referral', source: 'decision', target: 'referral', style: { strokeDasharray: '5 4' } },
]
const nodeTypes = { stage: WorkflowNode }
const edgeOptions = {
  type: 'smoothstep',
  markerEnd: { type: MarkerType.ArrowClosed, color: 'var(--xy-edge-stroke)' },
} satisfies DefaultEdgeOptions
const fit = { padding: { x: '28px', y: '44px' }, maxZoom: 1.08 } as const
const ariaLabels = {
  'controls.ariaLabel': 'کنترل‌های نمای گردش کار',
  'controls.zoomIn.ariaLabel': 'بزرگ‌نمایی',
  'controls.zoomOut.ariaLabel': 'کوچک‌نمایی',
  'controls.fitView.ariaLabel': 'نمایش همهٔ مراحل',
  'node.a11yDescription.default': 'برای انتخاب مرحله کلید ورود یا فاصله را فشار دهید. برای لغو انتخاب کلید گریز را فشار دهید.',
} satisfies Partial<AriaLabelConfig>

export function WorkflowSpecimen() {
  const { theme } = useDidrahTheme()

  return (
    <Panel surface="raised" density="compact">
      <SectionHeader title="مسیر بررسی افت فروش" description="از ثبت سیگنال تا تصمیم مدیر و دو مسیر ممکن برای پیگیری." />
      <div className="lab-flow-frame">
        <ReactFlow
          className="didrah-flow"
          forceColorMode={theme}
          defaultNodes={nodes}
          defaultEdges={edges}
          nodeTypes={nodeTypes}
          defaultEdgeOptions={edgeOptions}
          ariaLabelConfig={ariaLabels}
          nodesDraggable={false}
          nodesConnectable={false}
          edgesReconnectable={false}
          edgesFocusable={false}
          deleteKeyCode={null}
          selectionKeyCode={null}
          minZoom={0.4}
          maxZoom={1.6}
          zoomOnScroll={false}
          fitView
          fitViewOptions={fit}
        >
          <Background variant={BackgroundVariant.Dots} gap={18} size={1.5} />
          <Controls position="bottom-left" orientation="horizontal" showInteractive={false} fitViewOptions={fit} />
        </ReactFlow>
      </div>
      <p className="lab-viz-note">برای انتخاب روی یک مرحله کلیک کنید یا از کلیدهای تب و ورود استفاده کنید. نمای نمودار را با کشیدن بوم جابه‌جا کنید.</p>
      <details className="lab-viz-equivalent">
        <summary>مراحل و وضعیت‌های گردش کار</summary>
        <ol>
          {stages.slice(0, 4).map(({ id, data }) => (
            <li key={id}>{data.stage} · {data.title} · {data.statusLabel}</li>
          ))}
          <li>
            مسیرهای نتیجه
            <ul>
              {stages.slice(4).map(({ id, data }) => (
                <li key={id}>{data.stage} · {data.title} · {data.statusLabel}</li>
              ))}
            </ul>
          </li>
        </ol>
      </details>
    </Panel>
  )
}
