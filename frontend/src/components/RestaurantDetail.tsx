import type { Restaurant } from '../types'

interface RestaurantDetailProps {
  restaurant: Restaurant
}

export default function RestaurantDetail({ restaurant }: RestaurantDetailProps) {
  return (
    <div className="space-y-4">
      {restaurant.cover_image && (
        <img src={restaurant.cover_image} alt={restaurant.name} className="w-full h-48 object-cover rounded-xl" />
      )}
      <div>
        <h3 className="text-lg font-semibold text-[var(--text-primary)]">{restaurant.name}</h3>
        {restaurant.cuisine && <p className="text-sm text-[var(--accent)]">{restaurant.cuisine}</p>}
      </div>
      <div className="flex gap-4 text-sm text-[var(--text-secondary)]">
        {restaurant.rating && <span>⭐ {restaurant.rating}</span>}
        {restaurant.avg_price && <span>人均 ¥{restaurant.avg_price}</span>}
      </div>
      {restaurant.address && <p className="text-sm text-[var(--text-secondary)]">📍 {restaurant.address}</p>}
      {restaurant.dishes && restaurant.dishes.length > 0 && (
        <div>
          <h4 className="text-sm font-medium text-[var(--text-primary)] mb-2">推荐菜品</h4>
          <div className="flex gap-3 overflow-x-auto pb-2">
            {restaurant.dishes.map(dish => (
              <div key={dish.id} className="shrink-0 bg-[var(--canvas)] rounded-xl p-3 min-w-[120px]">
                <div className="text-sm font-medium text-[var(--text-primary)]">{dish.name}</div>
                {dish.price && <div className="text-xs text-[var(--text-secondary)]">¥{dish.price}</div>}
                {dish.is_signature && <span className="text-xs text-[var(--accent)]">招牌</span>}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
