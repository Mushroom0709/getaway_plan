import type { Day, RouteSegment, BudgetItem } from '../types'

interface OverviewProps {
    days: Day[]
    routes: RouteSegment[]
    budget: BudgetItem[]
    weather: { city: string; high_temp?: string; low_temp?: string; advice?: string }[]
}

const iconMap: Record<number, string> = { 0: '✈️', 1: '🚗', 2: '🚗', 3: '🚗', 4: '🚗', 5: '🚗', 6: '🚗' }

const cityNameMap: Record<string, string> = {
    xining: '西宁', qilian: '祁连', zhangye: '张掖', dunhuang: '敦煌', jiuquan: '酒泉'
}

export default function Overview({ days, routes, budget, weather }: OverviewProps) {
    // Calculate per-day route totals
    const dayRouteMap = new Map<number, { km: number; min: number }>()
    routes.forEach(r => {
        const dn = r.day_number ?? 0
        if (!dayRouteMap.has(dn)) dayRouteMap.set(dn, { km: 0, min: 0 })
        const cur = dayRouteMap.get(dn)!
        cur.km += r.distance_km || 0
        cur.min += r.duration_min || 0
    })

    const budgetTotal = budget.reduce((s, i) => s + (i.subtotal || 0), 0)
    const driveDays = days.filter(d => (d.drive_hours || 0) > 0)

    return (
        <div className="space-y-6">
            <h3 className="text-lg font-semibold text-[var(--text-primary)]">📊 行程总览</h3>

            {/* Route Table */}
            <div className="overflow-x-auto">
                <table className="w-full text-sm border-collapse">
                    <thead>
                        <tr className="border-b border-[var(--border)]">
                            <th className="text-left py-2 px-2 font-medium text-[var(--text-secondary)]">天</th>
                            <th className="text-left py-2 px-2 font-medium text-[var(--text-secondary)]">路线</th>
                            <th className="text-left py-2 px-2 font-medium text-[var(--text-secondary)]">方式</th>
                            <th className="text-right py-2 px-2 font-medium text-[var(--text-secondary)]">里程</th>
                            <th className="text-right py-2 px-2 font-medium text-[var(--text-secondary)]">用时</th>
                            <th className="text-left py-2 px-2 font-medium text-[var(--text-secondary)]">住宿</th>
                        </tr>
                    </thead>
                    <tbody>
                        {[...days].sort((a, b) => (a.sort_order ?? a.day_number) - (b.sort_order ?? b.day_number)).map(day => {
                            const rt = dayRouteMap.get(day.day_number)
                            const isTransit = day.day_number === 0 || day.day_number === 6
                            return (
                                <tr key={day.id} className="border-b border-[var(--border)] hover:bg-[var(--canvas)]">
                                    <td className="py-2 px-2">
                                        <span className="font-medium">D{day.day_number}</span>
                                    </td>
                                    <td className="py-2 px-2 text-xs">{day.title}</td>
                                    <td className="py-2 px-2">
                                        <span className="text-xs px-1.5 py-0.5 rounded bg-[var(--canvas)]">
                                            {isTransit ? '✈️ 飞行' : '🚗 自驾'}
                                        </span>
                                    </td>
                                    <td className="py-2 px-2 text-right text-xs">
                                        {rt ? `${Math.round(rt.km)}km` : '—'}
                                    </td>
                                    <td className="py-2 px-2 text-right text-xs">
                                        {rt ? `${Math.round(rt.min / 60)}h${Math.round(rt.min % 60)}m` : day.drive_hours ? `${day.drive_hours}h` : '—'}
                                    </td>
                                    <td className="py-2 px-2 text-xs">{cityNameMap[day.hotel_city || ''] || day.hotel_city || '—'}</td>
                                </tr>
                            )
                        })}
                    </tbody>
                </table>
            </div>

            {/* Summary Cards */}
            <div className="grid grid-cols-2 gap-3">
                <div className="bg-[var(--canvas)] rounded-xl p-4">
                    <div className="text-xs text-[var(--text-secondary)] mb-1">总里程</div>
                    <div className="text-xl font-semibold">
                        {Math.round(Array.from(dayRouteMap.values()).reduce((s, v) => s + v.km, 0)).toLocaleString()} km
                    </div>
                </div>
                <div className="bg-[var(--canvas)] rounded-xl p-4">
                    <div className="text-xs text-[var(--text-secondary)] mb-1">驾驶天数</div>
                    <div className="text-xl font-semibold">{driveDays.length} 天</div>
                </div>
                <div className="bg-[var(--canvas)] rounded-xl p-4">
                    <div className="text-xs text-[var(--text-secondary)] mb-1">驾驶总时长</div>
                    <div className="text-xl font-semibold">
                        {Math.round(Array.from(dayRouteMap.values()).reduce((s, v) => s + v.min, 0) / 60)}h
                    </div>
                </div>
                <div className="bg-[var(--canvas)] rounded-xl p-4">
                    <div className="text-xs text-[var(--text-secondary)] mb-1">全程天数</div>
                    <div className="text-xl font-semibold">{days.length} 天</div>
                </div>
            </div>

            {/* Budget */}
            <div>
                <h4 className="font-medium text-sm mb-3 text-[var(--text-secondary)]">💰 费用预估</h4>
                <div className="space-y-2">
                    {budget.map(item => (
                        <div key={item.id} className="flex justify-between text-sm">
                            <span className="text-[var(--text-secondary)]">{item.item}{item.quantity > 1 ? ` ×${item.quantity}` : ''}</span>
                            <span className="font-medium">¥{item.subtotal?.toLocaleString() || 0}</span>
                        </div>
                    ))}
                    <div className="border-t border-[var(--border)] pt-2 flex justify-between font-semibold">
                        <span>合计</span>
                        <span>¥{budgetTotal.toLocaleString()}</span>
                    </div>
                </div>
            </div>

            {/* Weather */}
            {weather.length > 0 && (
                <div>
                    <h4 className="font-medium text-sm mb-2 text-[var(--text-secondary)]">🌤️ 天气参考（8月下旬）</h4>
                    <div className="space-y-2">
                        {weather.map((w, i) => (
                            <div key={i} className="flex items-center gap-2 text-sm bg-[var(--canvas)] rounded-lg p-2">
                                <span className="font-medium min-w-[60px]">{w.city}</span>
                                <span className="text-xs text-[var(--text-secondary)]">{w.high_temp} / {w.low_temp}</span>
                                <span className="text-xs text-[var(--text-secondary)] ml-auto">{w.advice}</span>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    )
}
