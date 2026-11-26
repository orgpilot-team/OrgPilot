import { Button, Segmented } from 'antd'
import { useState } from 'react'
import { useDidrahTheme } from '../../shared/design-system/theme/DidrahThemeProvider'
import { BranchSalesChart } from '../../shared/visualization/charts/BranchSalesChart'
import { defaultChartFrameRate } from '../../shared/visualization/charts/chart-motion'
import type { ChartFrameRate } from '../../shared/visualization/charts/chart-motion'
import { ChartMotionGroup } from '../../shared/visualization/charts/SalesChartMotion'
import { SalesTrendChart } from '../../shared/visualization/charts/SalesTrendChart'
import { initialSalesData, updatedSalesData } from './chart-specimen-data'
import type { SalesSpecimenData } from './chart-specimen-data'

const unit = 'میلیون ریال'
const previousLabel = 'دورهٔ قبل · \u2066POS\u2069'
const referenceAxis = { min: 0, max: 80, interval: 20 }
const fixtureSalesNote = 'فروش سه‌شنبه افت کرد. مقدار چهارشنبه در دورهٔ قبل ثبت نشده است.'

function branchNote(target: string | null) {
  return target === null ? undefined : <>خط‌چین، هدف <bdi dir="ltr">{target}</bdi> میلیون ریالی را نشان می‌دهد.</>
}

export function ChartSpecimens({ data }: { data?: SalesSpecimenData | null } = {}) {
  const { theme } = useDidrahTheme()
  const [mock, setMock] = useState(initialSalesData)
  const [replayKey, setReplay] = useState(0)
  const [motion, setMotion] = useState(true)
  const [frameRate, setFrameRate] = useState<ChartFrameRate>(defaultChartFrameRate)
  const observations = data === undefined ? mock : data
  const animation = { enabled: motion, frameRate, replayKey }

  return (
    <>
      <ChartMotionGroup>
        <div className="lab-chart-grid">
          <SalesTrendChart
            title="روند فروش خالص"
            description={<>عملکرد هفتهٔ جاری و هفتهٔ قبل · {unit}</>}
            accessibleName="نمودار مقایسهٔ فروش خالص هفتگی"
            data={initialSalesData.trend}
            previousLabel={previousLabel}
            unit={unit}
            valueAxis={referenceAxis}
            note={fixtureSalesNote}
          />
          <SalesTrendChart
            title="روند فروش خالص"
            description={<>آزمایش بصری · عملکرد هفتهٔ جاری و هفتهٔ قبل · {unit}</>}
            accessibleName="نمودار آزمایشی مقایسهٔ فروش خالص هفتگی"
            regionLabel="آزمایش بصری روند فروش خالص"
            className="lab-sales-experiment"
            variant="luminous"
            data={observations?.trend ?? null}
            previousLabel={previousLabel}
            unit={unit}
            note={observations === initialSalesData ? fixtureSalesNote : undefined}
            animation={animation}
          />
          <BranchSalesChart
            title="فروش خالص شعب"
            description={<>فروش در برابر هدف هفتگی · {unit}</>}
            accessibleName="نمودار فروش شعب آرکا در برابر هدف"
            data={initialSalesData.branches}
            target={initialSalesData.target}
            unit={unit}
            valueAxis={referenceAxis}
            note={branchNote(initialSalesData.target)}
          />
          <BranchSalesChart
            title="فروش خالص شعب"
            description={<>آزمایش بصری · فروش در برابر هدف هفتگی · {unit}</>}
            accessibleName="نمودار آزمایشی فروش شعب آرکا در برابر هدف"
            regionLabel="آزمایش بصری فروش خالص شعب"
            className="lab-branch-experiment"
            variant="luminous"
            data={observations?.branches ?? null}
            target={observations?.target ?? null}
            unit={unit}
            note={branchNote(observations?.target ?? null)}
            animation={animation}
          />
        </div>
      </ChartMotionGroup>
      {import.meta.env.DEV && data === undefined && (
        <div className="lab-chart-motion-controls" role="group" aria-label="کنترل‌های آزمایش نمودار">
          <Button size="small" onClick={() => setReplay((count) => count + 1)}>بازپخش ورود</Button>
          <Button size="small" onClick={() => setMock(updatedSalesData)}>دادهٔ نمونهٔ دوم</Button>
          <Button size="small" onClick={() => setMock(initialSalesData)}>بازنشانی داده</Button>
          <Button size="small" aria-pressed={motion} onClick={() => setMotion(!motion)}>پویانمایی</Button>
          {theme === 'dark' && (
            <Segmented<ChartFrameRate>
              size="small"
              aria-label="نرخ فریم پویانمایی"
              options={[{ label: <bdi dir="ltr">30 FPS</bdi>, value: defaultChartFrameRate }, { label: 'بومی (بدون سقف)', value: 'native' }]}
              value={frameRate}
              onChange={setFrameRate}
            />
          )}
        </div>
      )}
    </>
  )
}
