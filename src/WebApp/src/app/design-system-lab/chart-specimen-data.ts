import type { BranchObservation } from '../../shared/visualization/charts/BranchSalesChart'
import type { TrendObservation } from '../../shared/visualization/charts/SalesTrendChart'

export type SalesSpecimenData = {
  trend: readonly TrendObservation[]
  branches: readonly BranchObservation[]
  target: string | null
}

export const initialSalesData: SalesSpecimenData = {
  trend: [
    { id: 'sat', day: 'شنبه', current: '48.25', previous: '41.25' },
    { id: 'sun', day: 'یکشنبه', current: '53.75', previous: '47.50' },
    { id: 'mon', day: 'دوشنبه', current: '64.00', previous: '48.00' },
    { id: 'tue', day: 'سه‌شنبه', current: '39.25', previous: '50.50', anomaly: 'افت ثبت‌شده' },
    { id: 'wed', day: 'چهارشنبه', current: '58.50', previous: null },
    { id: 'thu', day: 'پنجشنبه', current: '63.75', previous: '56.75' },
    { id: 'fri', day: 'جمعه', current: '70.25', previous: '58.00' },
  ],
  branches: [
    { name: 'ونک', code: 'ARK-01', sales: '72.25' },
    { name: 'تهرانپارس', code: 'ARK-03', sales: '63.75' },
    { name: 'صادقیه', code: 'ARK-02', sales: '51.50' },
    { name: 'تجریش', code: 'ARK-04', sales: '46.00' },
  ],
  target: '60.00',
}

export const updatedSalesData: SalesSpecimenData = {
  trend: [
    { id: 'sat', day: 'شنبه', current: '60.50', previous: '46.75' },
    { id: 'sun', day: 'یکشنبه', current: '57.25', previous: '51.50' },
    { id: 'mon', day: 'دوشنبه', current: '73.75', previous: '52.25' },
    { id: 'tue', day: 'سه‌شنبه', current: '31.50', previous: '57.00', anomaly: 'افت ثبت‌شده' },
    { id: 'wed', day: 'چهارشنبه', current: '64.25', previous: null },
    { id: 'thu', day: 'پنجشنبه', current: '55.00', previous: '60.75' },
    { id: 'fri', day: 'جمعه', current: '76.50', previous: '65.50' },
  ],
  branches: [
    { name: 'ونک', code: 'ARK-01', sales: '64.50' },
    { name: 'تهرانپارس', code: 'ARK-03', sales: '74.75' },
    { name: 'صادقیه', code: 'ARK-02', sales: '60.25' },
    { name: 'تجریش', code: 'ARK-04', sales: '38.50' },
  ],
  target: '60.00',
}
