import { CloseCircleOutlined, ExclamationCircleOutlined } from '@ant-design/icons'
import {
  Alert, App, Button, Checkbox, DatePicker, Drawer, Dropdown, Empty, Input,
  InputNumber, Menu, Popover, Radio, Select, Skeleton, Spin, Switch, Table, Tag, Tooltip,
} from 'antd'
import type { TableColumnsType } from 'antd'
// Ant Design's DatePicker uses the bundled Day.js locale data for calendar labels.
import 'dayjs/locale/fa'
import { useEffect, useState } from 'react'
import './ant-specimens.css'

const branches = [
  { value: 'vanak', label: 'شعبهٔ ونک' },
  { value: 'sadeghieh', label: 'شعبهٔ صادقیه' },
  { value: 'tehranpars', label: 'شعبهٔ تهرانپارس' },
  { value: 'tajrish', label: 'شعبهٔ تجریش', disabled: true },
]

const retailRows = [
  { sku: 'SKU-ARK-04821', name: 'قهوهٔ آسیاب‌شده', branch: 'ونک', stock: '1,248', sales: '58,240,750.25', lowStock: false },
  { sku: 'SKU-ARK-10236', name: 'شیر کم‌چرب', branch: 'صادقیه', stock: '18', sales: '43,701,056.75', lowStock: true },
  { sku: 'SKU-ARK-23107', name: 'برنج ایرانی', branch: 'تهرانپارس', stock: '684', sales: '12,670,280.50', lowStock: false },
]

const columns: TableColumnsType<(typeof retailRows)[number]> = [
  { title: 'کالا', dataIndex: 'name', key: 'name', rowScope: 'row' },
  {
    title: 'شناسه',
    dataIndex: 'sku',
    key: 'sku',
    render: (sku: string) => <bdi className="lab-ant-identifier" dir="ltr" lang="en">{sku}</bdi>,
  },
  { title: 'شعبه', dataIndex: 'branch', key: 'branch' },
  {
    title: 'موجودی',
    dataIndex: 'stock',
    key: 'stock',
    render: (stock: string) => <bdi className="lab-ant-number" dir="ltr">{stock}</bdi>,
  },
  {
    title: 'فروش خالص (ریال)',
    dataIndex: 'sales',
    key: 'sales',
    render: (sales: string) => <bdi className="lab-ant-number" dir="ltr">{sales}</bdi>,
  },
  {
    title: 'وضعیت',
    key: 'status',
    render: (_, row) => row.lowStock
      ? <Tag color="warning">کمبود موجودی</Tag>
      : <Tag color="success">موجودی کافی</Tag>,
  },
]

export function AntSpecimens() {
  const { message, notification, modal } = App.useApp()
  const [reference, setReference] = useState('')
  const [orderLevel, setOrderLevel] = useState<string | null>('20.00')
  const [branchesLoading, setBranchesLoading] = useState(false)
  const [drawerOpen, setDrawerOpen] = useState(false)
  const [refreshing, setRefreshing] = useState(false)
  const [pending, setPending] = useState(false)
  const [empty, setEmpty] = useState(false)
  const [lowStockOnly, setLowStockOnly] = useState(false)

  useEffect(() => {
    if (!refreshing) return

    const timer = window.setTimeout(() => setRefreshing(false), 1200)
    return () => window.clearTimeout(timer)
  }, [refreshing])

  const validReference = /^ARK-\d{5}$/.test(reference.trim())
  const lowOrderLevel = orderLevel !== null && Number(orderLevel) < 25
  const rows = empty ? [] : retailRows.filter((item) => !lowStockOnly || item.lowStock)

  return (
    <section className="lab-panel lab-ant" aria-labelledby="lab-ant-heading">
      <div className="lab-ant-heading">
        <h2 id="lab-ant-heading">اجزای رابط کاربری</h2>
        <bdi lang="en" dir="ltr">Ant Design</bdi>
      </div>

      <div className="lab-ant-grid">
        <section className="lab-ant-card">
          <h3>دکمه‌ها و بازخورد</h3>
          <div className="lab-ant-actions">
            <Button type="primary" onClick={() => void message.success('نمونهٔ گزارش ذخیره شد.')}>
              ذخیرهٔ گزارش
            </Button>
            <Button onClick={() => setRefreshing(true)} loading={refreshing} aria-busy={refreshing}>
              {refreshing ? 'در حال تازه‌سازی…' : 'تازه‌سازی'}
            </Button>
            <Button type="text" onClick={() => notification.info({
              key: 'lab-shift-notice',
              title: 'گزارش شیفت',
              description: <>فهرست موجودی <bdi dir="ltr" lang="en">Stock Audit</bdi> آمادهٔ بررسی است.</>,
              duration: 0,
              placement: 'bottomLeft',
            })}>
              اعلان گزارش
            </Button>
            <Button type="primary" danger onClick={() => modal.confirm({
              title: 'پیش‌نویس نمونه حذف شود؟',
              content: 'این پیش‌نویس فقط برای آزمایش رابط کاربری است.',
              okButtonProps: { danger: true },
              onOk: () => { void message.success('پیش‌نویس نمونه حذف شد.') },
            })}>
              حذف پیش‌نویس
            </Button>
            <Button disabled>ارسال نهایی</Button>
          </div>
          <div className="lab-ant-actions lab-ant-status">
            <Tag color="success">تأیید شد</Tag>
            <Tag color="warning">نیاز به بررسی</Tag>
            <Tag color="error">ناموفق</Tag>
            <Tag color="processing">در حال بررسی</Tag>
          </div>
          <Alert type="warning" showIcon title="موجودی شعبهٔ صادقیه کمتر از حد سفارش است." />
        </section>

        <section className="lab-ant-card">
          <h3>منوها و پنجره‌ها</h3>
          <Menu
            className="lab-ant-menu"
            mode="horizontal"
            defaultSelectedKeys={['inventory']}
            items={[
              { key: 'inventory', label: 'موجودی' },
              { key: 'sales', label: 'فروش' },
              { key: 'orders', label: 'سفارش‌ها' },
            ]}
          />
          <div className="lab-ant-actions">
            <Dropdown menu={{
              items: [
                { key: 'daily', label: 'گزارش روزانه' },
                { key: 'weekly', label: 'گزارش هفتگی' },
              ],
              onClick: ({ key }) => void message.info(key === 'daily' ? 'گزارش روزانه انتخاب شد.' : 'گزارش هفتگی انتخاب شد.'),
            }} trigger={['click']}>
              <Button>گزینه‌های گزارش</Button>
            </Dropdown>
            <Tooltip title="واحد همهٔ مبالغ جدول ریال است." trigger={['hover', 'focus']}>
              <Button>واحد مبالغ</Button>
            </Tooltip>
            <Popover title="آستانهٔ سفارش" content="موجودی کمتر از ۲۰ واحد نیاز به بررسی دارد." trigger="click">
              <Button>راهنمای موجودی</Button>
            </Popover>
            <Button onClick={() => setDrawerOpen(true)}>جزئیات شعبه</Button>
          </div>
        </section>
      </div>

      <section className="lab-ant-card">
        <h3>کنترل‌های فرم</h3>
        <div className="lab-ant-fields">
          <div className="lab-ant-field">
            <label htmlFor="lab-ant-report-title">عنوان گزارش</label>
            <Input id="lab-ant-report-title" defaultValue="گزارش موجودی شیفت صبح" allowClear />
          </div>
          <div className="lab-ant-field">
            <label htmlFor="lab-ant-reference">شناسهٔ پیگیری</label>
            <Input
              id="lab-ant-reference"
              value={reference}
              onChange={(event) => setReference(event.target.value)}
              placeholder="ARK-04821"
              dir="ltr"
              status={validReference ? undefined : 'error'}
              aria-invalid={!validReference}
              aria-describedby={validReference ? undefined : 'lab-ant-reference-error'}
            />
            {!validReference && (
              <span id="lab-ant-reference-error" className="lab-ant-field-hint" data-status="error">
                <CloseCircleOutlined aria-hidden="true" />
                شناسه را با قالب نمونه وارد کنید.
              </span>
            )}
          </div>
          <div className="lab-ant-field">
            <label htmlFor="lab-ant-branch">شعبه</label>
            <Select
              id="lab-ant-branch"
              defaultValue="vanak"
              options={branchesLoading ? [] : branches}
              placeholder="شعبه را انتخاب کنید"
              showSearch={{ optionFilterProp: 'label' }}
              virtual={false}
              allowClear
              loading={branchesLoading}
              aria-busy={branchesLoading}
              notFoundContent={branchesLoading ? 'در حال بارگیری شعبه‌ها…' : 'شعبه‌ای پیدا نشد.'}
            />
          </div>
          <div className="lab-ant-field">
            <label htmlFor="lab-ant-order-level">حد سفارش</label>
            <InputNumber
              id="lab-ant-order-level"
              value={orderLevel}
              onChange={setOrderLevel}
              stringMode
              step="0.01"
              min="0"
              status={lowOrderLevel ? 'warning' : undefined}
              aria-describedby={lowOrderLevel ? 'lab-ant-order-warning' : undefined}
            />
            {lowOrderLevel && (
              <span id="lab-ant-order-warning" className="lab-ant-field-hint" data-status="warning">
                <ExclamationCircleOutlined aria-hidden="true" />
                حد سفارش کمتر از ۲۵ واحد است.
              </span>
            )}
          </div>
          <div className="lab-ant-field">
            <label htmlFor="lab-ant-date">تاریخ گزارش</label>
            <DatePicker id="lab-ant-date" />
          </div>
          <div className="lab-ant-field">
            <label htmlFor="lab-ant-warehouse">کد انبار</label>
            <Input id="lab-ant-warehouse" defaultValue="WH-03" disabled dir="ltr" />
          </div>
          <div className="lab-ant-field lab-ant-notes">
            <label htmlFor="lab-ant-notes">یادداشت سرپرست</label>
            <Input.TextArea id="lab-ant-notes" rows={2} defaultValue="موجودی قفسه با گزارش انبار مرکزی بررسی شد." />
          </div>
        </div>
        <div className="lab-ant-actions">
          <Checkbox checked={branchesLoading} onChange={(event) => setBranchesLoading(event.target.checked)}>
            بارگیری شعبه‌ها
          </Checkbox>
          <Checkbox checked={lowStockOnly} onChange={(event) => setLowStockOnly(event.target.checked)}>
            فقط کالاهای کم‌موجودی
          </Checkbox>
          <Radio.Group
            aria-label="شیفت گزارش"
            defaultValue="morning"
            options={[{ label: 'شیفت صبح', value: 'morning' }, { label: 'شیفت عصر', value: 'evening' }]}
          />
        </div>
      </section>

      <section className="lab-ant-card">
        <div className="lab-ant-table-header">
          <h3>موجودی و فروش شعب آرکا</h3>
          <div className="lab-ant-actions">
            <label><Switch checked={pending} onChange={setPending} /> حالت بارگیری</label>
            <label><Switch checked={empty} onChange={setEmpty} /> جدول خالی</label>
          </div>
        </div>
        {pending
          ? <div className="lab-ant-loading"><Spin /><Skeleton active title={false} paragraph={{ rows: 3 }} /></div>
          : <Table
              columns={columns}
              dataSource={rows}
              rowKey="sku"
              pagination={false}
              scroll={{ x: 620 }}
              locale={{ emptyText: <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} /> }}
            />
        }
      </section>

      <Drawer title="جزئیات شعبهٔ ونک" open={drawerOpen} onClose={() => setDrawerOpen(false)} size="default">
        <p>فهرست کالاهای شعبه با گزارش <bdi dir="ltr" lang="en">Stock Audit</bdi> مطابقت دارد.</p>
        <Alert type="success" showIcon title="کنترل موجودی انجام شد." />
      </Drawer>
    </section>
  )
}
