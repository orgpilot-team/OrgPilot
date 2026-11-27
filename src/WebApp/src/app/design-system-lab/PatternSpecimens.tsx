import { ArrowDownOutlined, FileTextOutlined, HistoryOutlined, InboxOutlined, ShopOutlined } from '@ant-design/icons'
import { Button, Menu, Popover, Radio, Tag } from 'antd'
import { useRef, useState } from 'react'
import type { ComponentRef } from 'react'
import { Panel, SectionHeader } from '../../shared/design-system/patterns/Panel'
import { PanelState } from '../../shared/design-system/patterns/PanelState'
import './pattern-specimens.css'

const navigation = [
  { key: 'inventory', icon: <InboxOutlined />, label: 'موجودی شعبه' },
  { key: 'sales', icon: <ShopOutlined />, label: 'فروش روزانه' },
  { key: 'orders', icon: <FileTextOutlined />, label: 'سفارش‌های تأمین' },
  { key: 'archive', icon: <HistoryOutlined />, label: 'بایگانی گزارش‌ها', disabled: true },
]

const reviewOptions = [
  { value: 'empty', label: 'خالی' },
  { value: 'loading', label: 'بارگیری' },
  { value: 'success', label: 'موفق' },
  { value: 'warning', label: 'هشدار' },
  { value: 'error', label: 'خطا' },
] as const

type ReviewState = (typeof reviewOptions)[number]['value']

export function ReviewStateSpecimen() {
  const [state, setState] = useState<ReviewState>('empty')
  const resetButton = useRef<ComponentRef<typeof Button>>(null)

  function retry() {
    resetButton.current?.focus()
    setState('success')
  }

  return (
    <Panel surface="raised">
      <SectionHeader
        title="وضعیت دریافت گزارش فروش"
        actions={<Button ref={resetButton} type="text" onClick={() => setState('empty')}>بازنشانی نمونه</Button>}
      />
      <Radio.Group
        aria-label="وضعیت نمونهٔ گزارش"
        className="lab-pattern-options"
        options={[...reviewOptions]}
        value={state}
        onChange={(event) => setState(event.target.value)}
      />
      <div className="lab-pattern-state">
        {state === 'empty' && (
          <PanelState
            kind="empty"
            title="تراکنشی ثبت نشده است"
            description="برای شیفت صبح شعبهٔ ونک هنوز داده‌ای در دسترس نیست."
          />
        )}
        {state === 'loading' && <PanelState kind="loading" title="در حال دریافت گزارش فروش شعبهٔ ونک…" />}
        {state === 'success' && (
          <PanelState kind="success" title="گزارش دریافت شد" description="گزارش فروش شیفت صبح آمادهٔ بررسی است." />
        )}
        {state === 'warning' && (
          <PanelState
            kind="warning"
            title="گزارش ناقص است"
            description="داده‌های یکی از صندوق‌ها هنوز به گزارش شیفت اضافه نشده است."
          />
        )}
        {state === 'error' && (
          <PanelState
            kind="error"
            title="دریافت گزارش ناموفق بود"
            description="ارتباط با سرویس گزارش‌گیری قطع شد."
            action={<Button size="small" onClick={retry}>تلاش دوباره</Button>}
          />
        )}
      </div>
    </Panel>
  )
}

export function NavigationPatternSpecimen() {
  const [selection, setSelection] = useState('inventory')
  const selectedItem = navigation.find(({ key }) => key === selection)

  return (
    <div className="lab-ant-grid">
      <Panel surface="raised" density="compact">
        <SectionHeader title="بخش‌های شعبه" />
        <Menu
          aria-label="بخش‌های شعبه"
          mode="inline"
          style={{ background: 'transparent', borderInlineEnd: 0 }}
          selectedKeys={[selection]}
          items={navigation}
          onSelect={({ key }) => setSelection(key)}
        />
        <Panel surface="selected" density="compact">
          <div className="lab-pattern-selection" role="status">
            <span>بخش انتخاب‌شده</span>
            <strong>{selectedItem?.label}</strong>
          </div>
        </Panel>
      </Panel>
      <Panel surface="raised" density="compact">
        <SectionHeader title="منوی افقی" />
        <Menu
          aria-label="بخش‌های گزارش"
          className="lab-ant-menu"
          mode="horizontal"
          defaultSelectedKeys={['inventory']}
          items={[
            { key: 'inventory', label: 'موجودی' },
            { key: 'sales', label: 'فروش' },
            { key: 'orders', label: 'سفارش‌ها' },
          ]}
        />
      </Panel>
    </div>
  )
}

export function InsightSpecimen() {
  const [reviewed, setReviewed] = useState(false)

  return (
    <Panel surface="raised">
      <SectionHeader
        title="بررسی موجودی شعبهٔ ونک"
        description={<>گزارش شیفت صبح <bdi dir="ltr" lang="en">INV-ARK/1405-0905</bdi></>}
        actions={
          <>
            <Popover
              title="جزئیات بررسی"
              content="موجودی قفسه‌ها با آخرین گزارش انبار مرکزی مقایسه شده است."
              trigger="click"
            >
              <Button>جزئیات</Button>
            </Popover>
            <Button
              type={reviewed ? 'default' : 'primary'}
              onClick={() => setReviewed(!reviewed)}
            >
              {reviewed ? 'بازنشانی بررسی' : 'ثبت بررسی'}
            </Button>
          </>
        }
      />
      <Panel surface="overlay" density="compact">
        <dl className="lab-pattern-kpi">
          <dt>ارزش خالص موجودی شعبهٔ ونک</dt>
          <dd className="lab-pattern-kpi-value"><bdi dir="ltr">2,584,320,750.25</bdi> <span>ریال</span></dd>
          <dd className="lab-pattern-kpi-comparison">
            <ArrowDownOutlined aria-hidden="true" />
            <span><bdi dir="ltr">186,432,500.00</bdi> ریال کاهش نسبت به شیفت قبل</span>
          </dd>
        </dl>
        <div className="lab-pattern-tags">
          <Tag color={reviewed ? 'success' : 'warning'}>{reviewed ? 'بررسی شد' : 'در انتظار بررسی'}</Tag>
          <Tag color="processing">شعبهٔ ونک</Tag>
        </div>
      </Panel>
      {reviewed
        ? <PanelState kind="success" title="بررسی نمونه ثبت شد." />
        : <PanelState
            kind="warning"
            title="موجودی ۳ کالا کمتر از حد سفارش است."
            description="موجودی قفسه و انبار این کالاها را پیش از سفارش بعدی تطبیق دهید."
          />}
    </Panel>
  )
}
