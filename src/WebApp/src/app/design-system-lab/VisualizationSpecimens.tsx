import { Button } from 'antd'
import { useState } from 'react'
import { Panel, SectionHeader } from '../../shared/design-system/patterns/Panel'
import { ChartSpecimens } from './ChartSpecimens'
import { WorkflowSpecimen } from './WorkflowSpecimen'
import './visualization-specimens.css'

export default function VisualizationSpecimens() {
  const [visible, setVisible] = useState(true)

  return (
    <section className="lab-visualization" aria-labelledby="lab-visualization-heading">
      <Panel>
        <SectionHeader
          id="lab-visualization-heading"
          level={2}
          title="نمایش داده و گردش کار"
          description="نمونه‌های آرکا برای مقایسهٔ فروش، بررسی یک افت و پیگیری تصمیم مدیر."
          actions={
            <Button aria-expanded={visible} aria-controls="lab-viz-content" onClick={() => setVisible(!visible)}>
              {visible ? 'پنهان کردن نمونه‌ها' : 'نمایش نمونه‌ها'}
            </Button>
          }
        />
        <div id="lab-viz-content" className="lab-viz-content" hidden={!visible}>
          {visible && <><ChartSpecimens /><WorkflowSpecimen /></>}
        </div>
      </Panel>
    </section>
  )
}
