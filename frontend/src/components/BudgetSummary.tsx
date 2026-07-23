import type { BudgetItem } from '../types'

interface BudgetSummaryProps {
  items: BudgetItem[]
}

const categoryLabels: Record<string, string> = {
  flight: '✈ 机票', hotel: '🏠 住宿', car: '🚗 租车',
  food: '🍴 餐饮', ticket: '🎫 门票', rail: '🚄 高铁', other: '📦 其他'
}

export default function BudgetSummary({ items }: BudgetSummaryProps) {
  const grouped = items.reduce((acc, item) => {
    if (!acc[item.category]) acc[item.category] = []
    acc[item.category].push(item)
    return acc
  }, {} as Record<string, BudgetItem[]>)

  const total = items.reduce((sum, item) => sum + (item.subtotal || 0), 0)

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-[var(--text-primary)]">费用估算</h3>
      {Object.entries(grouped).map(([cat, catItems]) => (
        <div key={cat}>
          <div className="text-sm font-medium text-[var(--text-secondary)] mb-1.5">
            {categoryLabels[cat] || cat}
          </div>
          {catItems.map(item => (
            <div key={item.id} className="flex justify-between text-sm py-1 text-[var(--text-primary)]">
              <span>{item.item}{item.quantity > 1 ? ` ×${item.quantity}` : ''}</span>
              <span className="font-medium">¥{item.subtotal?.toLocaleString() || 0}</span>
            </div>
          ))}
        </div>
      ))}
      <div className="border-t border-[var(--border)] pt-3 flex justify-between font-semibold text-[var(--text-primary)]">
        <span>总计</span>
        <span>¥{total.toLocaleString()}</span>
      </div>
    </div>
  )
}
