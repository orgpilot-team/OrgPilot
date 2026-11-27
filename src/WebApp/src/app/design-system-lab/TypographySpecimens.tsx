import type { ReactNode } from 'react'
import { fontWeights, typography } from '../../shared/design-system/tokens/typography'
import type { TypographyRole } from '../../shared/design-system/tokens/typography'
import './typography-specimens.css'

const headingSamples = [
  ['heading-1', 'عملکرد فروشگاه‌های آرکا'],
  ['heading-2', 'مرور فروش و موجودی شعب'],
  ['heading-3', 'کالاهای نزدیک به نقطهٔ سفارش'],
] as const

const bodySamples = [
  ['secondary', 'فروش ثبت‌شدهٔ شعبهٔ ونک در پایان شیفت عصر.'],
  ['body', 'در پایان شیفت عصر، فروش و موجودی کالاهای پرفروش شعبهٔ ونک را با گزارش روزانه مقایسه کنید.'],
  ['body-large', 'برای آماده‌سازی شعبهٔ صادقیه پیش از شروع شیفت صبح، موجودی کالاهای ضروری را با فهرست سفارش انبار مرکزی مقایسه کنید.'],
] as const

const controlSamples = [
  ['action', 'ثبت گزارش'],
  ['label', 'عنوان گزارش'],
  ['caption', 'آخرین به‌روزرسانی'],
  ['technical', <bdi lang="en" dir="ltr">ARK-OPS/1405-0905</bdi>],
] as const

const storeSamples = [
  { store: 'ونک', sku: 'SKU-ARK-04821', quantity: '12,480', sales: '58,240,750.25', stock: '97.50%', density: 'table' },
  { store: 'صادقیه', sku: 'SKU-ARK-10236', quantity: '7,624', sales: '43,701,056.75', stock: '92.75%', density: 'table' },
  { store: 'ستارخان', sku: 'SKU-ARK-00018', quantity: '810', sales: '5,827,510.00', stock: '88.00%', density: 'table-compact' },
  { store: 'تهرانپارس', sku: 'SKU-ARK-23107', quantity: '1,864', sales: '12,670,280.50', stock: '94.25%', density: 'table-compact' },
] as const

function TypeSample({ role, children }: { role: TypographyRole; children: ReactNode }) {
  const { size, weight, lineHeight } = typography.roles[role]

  return (
    <div className="lab-type-sample">
      <span data-typography-role={role} style={{ font: `var(--didrah-type-${role})` }}>
        {children}
      </span>
      <bdi className="lab-type-meta" dir="ltr">{Number.parseFloat(size) * 16}px / {weight} / {lineHeight}</bdi>
    </div>
  )
}

export function TypographySpecimens() {
  return (
    <section className="lab-panel lab-typography" aria-labelledby="lab-typography-heading">
      <div className="lab-typography-header">
        <h2 id="lab-typography-heading">تایپوگرافی</h2>
        <bdi className="lab-type-meta" lang="en" dir="ltr">Dastkhat Variable v1.220</bdi>
      </div>

      <div className="lab-typography-grid">
        <section className="lab-type-card">
          <h3>عنوان‌ها و متن فارسی</h3>
          {headingSamples.map(([role, sample]) => <TypeSample key={role} role={role}>{sample}</TypeSample>)}
          <div className="lab-body-samples">
            {bodySamples.map(([role, sample]) => <TypeSample key={role} role={role}>{sample}</TypeSample>)}
          </div>
          <div className="lab-body-samples">
            {controlSamples.map(([role, sample]) => <TypeSample key={role} role={role}>{sample}</TypeSample>)}
          </div>
        </section>

        <section className="lab-type-card">
          <h3>اعداد و متن ترکیبی</h3>
          <div className="lab-kpi-sample">
            <span className="lab-type-meta">فروش خالص شعب آرکا</span>
            <bdi className="lab-kpi-value lab-numeric" dir="ltr">1,284,560,750.25</bdi>
            <span>ریال · رشد فروش <bdi className="lab-numeric" dir="ltr">+12.75%</bdi></span>
          </div>
          <div className="lab-bidi-samples">
            <p>گزارش موجودی <bdi lang="en" dir="ltr">Central Warehouse</bdi> برای شعبهٔ ونک</p>
            <p>
              تاریخ ثبت <bdi className="lab-technical" dir="ltr">۱۴۰۵/۰۹/۰۵</bdi>
              {' · شناسهٔ گزارش '}
              <bdi className="lab-technical" lang="en" dir="ltr">ARK-OPS/1405-0905</bdi>
            </p>
          </div>
          <div className="lab-weight-grid">
            {Object.entries(fontWeights).map(([name, weight]) => (
              <div key={name} className="lab-weight-sample">
                <span data-weight={weight} style={{ fontWeight: weight }}>فروش شعب</span>
                <bdi className="lab-type-meta" dir="ltr">{weight}</bdi>
              </div>
            ))}
          </div>
        </section>
      </div>

      <div className="lab-type-card lab-retail-table">
        <div className="lab-table-scroll">
          <table>
            <caption>نمونهٔ جدول فروش شعب <bdi className="lab-type-meta" dir="ltr">14px / 13px</bdi></caption>
            <thead>
              <tr>
                <th scope="col">شعبه</th>
                <th scope="col">شناسهٔ کالا</th>
                <th scope="col">تعداد فروش</th>
                <th scope="col">فروش خالص (ریال)</th>
                <th scope="col">موجودی قابل‌فروش</th>
              </tr>
            </thead>
            <tbody>
              {storeSamples.map(({ store, sku, quantity, sales, stock, density }) => (
                <tr key={sku} data-typography-role={density} style={{ font: `var(--didrah-type-${density})` }}>
                  <th scope="row">{store}</th>
                  <td><bdi className="lab-table-id" lang="en" dir="ltr">{sku}</bdi></td>
                  <td><bdi className="lab-numeric" dir="ltr">{quantity}</bdi></td>
                  <td><bdi className="lab-numeric" dir="ltr">{sales}</bdi></td>
                  <td><bdi className="lab-numeric" dir="ltr">{stock}</bdi></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <section className="lab-chart-labels">
        <h3>برچسب‌های نمونهٔ نمودار</h3>
        <div className="lab-chart-label-row">
          <span>محور زمان · ۵ آذر</span>
          <span>محور فروش · <bdi className="lab-numeric" dir="ltr">25,000,000</bdi> ریال</span>
          <span className="lab-chart-series">راهنما · فروش خالص</span>
        </div>
      </section>
    </section>
  )
}
