import { use } from 'echarts/core'
import type { ComposeOption } from 'echarts/core'
import { BarChart, LineChart } from 'echarts/charts'
import type { BarSeriesOption, CustomSeriesOption, LineSeriesOption } from 'echarts/charts'
import { GridComponent, LegendComponent, MarkLineComponent, MarkPointComponent, TooltipComponent } from 'echarts/components'
import type {
  GridComponentOption, LegendComponentOption, MarkLineComponentOption, MarkPointComponentOption, TooltipComponentOption,
} from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

use([BarChart, LineChart, GridComponent, LegendComponent, MarkLineComponent, MarkPointComponent, TooltipComponent, CanvasRenderer])

export type ChartOption = ComposeOption<
  BarSeriesOption | CustomSeriesOption | LineSeriesOption | GridComponentOption | LegendComponentOption
  | MarkLineComponentOption | MarkPointComponentOption | TooltipComponentOption
>
