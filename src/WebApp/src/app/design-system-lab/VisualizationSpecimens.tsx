import { Button } from 'antd'
import { lazy, Suspense, useState } from 'react'
import type { ReactNode } from 'react'
import './visualization-specimens.css'

const ChartSpecimens = lazy(async () => ({ default: (await import('./ChartSpecimens')).ChartSpecimens }))
const WorkflowSpecimen = lazy(async () => ({ default: (await import('./WorkflowSpecimen')).WorkflowSpecimen }))

function DeferredSpecimen({ id, name, children }: { id: string; name: string; children: ReactNode }) {
  const [visible, setVisible] = useState(() => window.location.hash === `#${id}`)

  return (
    <div className="lab-viz-content" id={id}>
      <Button aria-expanded={visible} aria-controls={`${id}-examples`} onClick={() => setVisible(!visible)}>
        {visible ? 'پنهان کردن' : 'نمایش'} {name}
      </Button>
      <div className="lab-viz-examples" id={`${id}-examples`} hidden={!visible}>
        {visible && <Suspense fallback={<p role="status">در حال آماده‌سازی نمونه…</p>}>{children}</Suspense>}
      </div>
    </div>
  )
}

export function ChartCatalogSpecimen() {
  return <DeferredSpecimen id="lab-viz-content" name="نمودارها"><ChartSpecimens /></DeferredSpecimen>
}

export function WorkflowCatalogSpecimen() {
  return <DeferredSpecimen id="lab-workflow-content" name="گردش کار"><WorkflowSpecimen /></DeferredSpecimen>
}
