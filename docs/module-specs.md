# Module Specifications — getaway_plan

## Backend Modules

### 1. auth — 认证模块

**router: `POST /api/auth/login`, `GET /api/auth/verify`**

```python
# services/auth_service.py
def verify_password(plain: str, hashed: str) -> bool
def create_access_token(device_id: str, expires_delta: timedelta = 7 days) -> str
def decode_token(token: str) -> dict | None

# deps.py
async def get_current_device(request: Request) -> str  # 从 Bearer token 提取 device_id
```

**中间件**: 除 `/api/auth/login` 外所有路由校验 JWT

### 2. trips — 旅行管理

**router: `GET/POST /api/trips`, `GET/PUT/DELETE /api/trips/{id}`**

```python
# schemas/trip.py
class TripCreate(BaseModel):
    name: str
    description: str | None
    start_date: date | None
    end_date: date | None

class TripResponse(BaseModel):
    id: int
    name: str
    ...
    days: list[DayResponse]
    flights: list[FlightResponse]
    ...

# routers/trips.py
async def list_trips(db: AsyncSession) -> list[TripResponse]
async def get_trip(id: int, db: AsyncSession) -> TripResponse  # 含嵌套
async def create_trip(data: TripCreate, db: AsyncSession) -> TripResponse
async def update_trip(id: int, data: TripUpdate, db: AsyncSession) -> TripResponse
async def delete_trip(id: int, db: AsyncSession) -> None
```

### 3. spots — 坐标点管理

**router: `GET/POST /api/trips/{trip_id}/spots`, `PUT/DELETE /api/spots/{id}`, `PUT /api/trips/{trip_id}/spots/reorder`**

```python
# schemas/spot.py
class SpotCreate(BaseModel):
    day_id: int | None
    name: str
    lng: float
    lat: float
    category: Literal["airport","highspeed_rail","train","scenic","photo","hotel","restaurant","other"]
    is_nav_point: bool = False
    nav_order: int | None = None
    arrival_time: time | None
    description: str | None
    intro: str | None

class SpotReorder(BaseModel):
    id: int
    nav_order: int

# routers/spots.py
async def list_spots(trip_id: int, day_id: int | None, category: str | None, 
                     is_nav_point: bool | None, db: AsyncSession) -> list[SpotResponse]
async def batch_reorder(trip_id: int, items: list[SpotReorder], db: AsyncSession) -> list[SpotResponse]
```

### 4. route_service — 高德路线规划

**router: `GET /api/trips/{trip_id}/routes`, `POST /api/trips/{trip_id}/routes/plan`, `DELETE /api/routes/{id}`**

```python
# services/route_service.py
async def plan_route(origin_spot: Spot, dest_spot: Spot, amap_key: str) -> RouteResult:
    """
    调用高德 REST API: restapi.amap.com/v3/direction/driving
    返回: { distance_km, duration_min, polyline }
    """
    url = f"https://restapi.amap.com/v3/direction/driving"
    params = {
        "origin": f"{origin_spot.lng},{origin_spot.lat}",
        "destination": f"{dest_spot.lng},{dest_spot.lat}",
        "strategy": 0, "extensions": "all", "key": amap_key
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        data = resp.json()
        path = data["route"]["paths"][0]
        return RouteResult(
            distance_km=float(path["distance"]) / 1000,
            duration_min=int(path["duration"]) / 60,
            polyline=extract_polyline(path["steps"])
        )
```

### 5. CRUD 模块（标准模式）

以下模块均遵循统一模式：

```
flights, highspeed_rails, rental_cars, hotels, restaurants, dishes,
daily_meals, attractions, social_notes, social_images, budget_items, weather
```

每个模块包含：
- `models/xxx.py` — SQLAlchemy ORM 模型
- `schemas/xxx.py` — Pydantic Create / Update / Response
- `routers/xxx.py` — `GET list / POST / PUT / DELETE`

**统一模式**：
```python
# list: GET /api/{parent}/{parent_id}/{resource}
# create: POST /api/{parent}/{parent_id}/{resource}
# update: PUT /api/{resource}/{id}
# delete: DELETE /api/{resource}/{id}
```

### 6. social_notes — 社交媒体笔记（特殊处理）

创建笔记时同时创建关联的 images：

```python
# routers/social_notes.py
async def create_note(spot_id: int, data: NoteCreate, db: AsyncSession):
    note = SocialNote(spot_id=spot_id, **data.dict(exclude={"images"}))
    db.add(note)
    await db.flush()  # 获取 note.id
    for img in data.images:
        db.add(SocialImage(note_id=note.id, **img.dict()))
    await db.commit()
    return note
```

---

## Frontend Components

### 页面布局

```
App (响应式: PC 两栏 / 移动端单栏)
├── AuthGuard          ← 检查 JWT，未登录显示 LoginPage
├── LoginPage          ← 密码输入 → 获取 token
├── TripSelector       ← 下拉选择旅行计划
└── MainLayout         ← 主页面
    ├── TopNav          ← 顶部导航：D0-D6 + 💰费用 按钮
    ├── MapPanel        ← 高德地图容器（PC: 左 55% / 移动: 40vh）
    │   ├── SpotMarkers ← 3 类标记渲染
    │   └── RouteLines  ← Polyline 渲染（showDir: true）
    ├── DayContent      ← 当天行程详情
    └── SlidePanel      ← 右侧滑出面板（点击标记触发）
        ├── HotelDetail
        ├── RestaurantDetail
        ├── AttractionDetail
        ├── PhotoGallery
        ├── NoteGallery
        └── BudgetSummary
```

### 组件规格

#### AuthGuard
```tsx
// 检查 localStorage token，无则显示 LoginPage
// API: GET /api/auth/verify
// 401 时清除 token 并跳转登录
interface AuthGuardProps {
  children: React.ReactNode;
}
```

#### LoginPage
```tsx
// 密码输入框 + 提交按钮
// API: POST /api/auth/login
// 成功: 存 token 到 localStorage，跳转主页
// 失败: 显示错误提示
```

#### TripSelector
```tsx
// 下拉选择旅行计划
// API: GET /api/trips
// 选中后加载该 trip 的全部数据
interface TripSelectorProps {
  onSelect: (tripId: number) => void;
}
```

#### MainLayout
```tsx
// 响应式布局
// PC: grid-cols-[55%_45%]，左侧地图，右侧内容
// 移动端: 地图 40vh，下方卡片流
interface MainLayoutProps {
  tripId: number;
}
```

#### MapPanel
```tsx
// 高德地图容器
// 接收 spots + route_segments 数据
// 渲染标记和路线
// 点击标记 → 触发 SlidePanel 打开
interface MapPanelProps {
  spots: Spot[];
  routes: RouteSegment[];
  onSpotClick: (spot: Spot) => void;
  activeDay: string;
}
```

#### TopNav
```tsx
// 横向滚动按钮组: D0, D1, D2, ..., D6, 💰费用
// 移动端: 紧凑模式，减小编号+标签
interface TopNavProps {
  days: Day[];
  activeDay: string;
  onChange: (day: string) => void;
}
```

#### SlidePanel
```tsx
// 从右侧滑出，宽度 PC: 45% / 移动端: 100%
// 根据 spot.category 渲染不同内容
// 包含关闭按钮
interface SlidePanelProps {
  spot: Spot | null;
  onClose: () => void;
}
```

#### HotelDetail
```tsx
// 酒店名称、品牌、评分、价格、房型
// 特色标签（features）
// 开业年份、电话
// 封面图片
interface HotelDetailProps {
  hotel: Hotel;
}
```

#### RestaurantDetail
```tsx
// 餐厅名称、地址、评分、人均、菜系
// 菜品列表（横滑卡片）
// 高德导航链接
interface RestaurantDetailProps {
  restaurant: Restaurant & { dishes: Dish[] };
}
```

#### AttractionDetail
```tsx
// 景区名称、票价、营业时间、海拔、建议游玩时长
// 游玩建议、亮点标签
// 关联小红书/抖音笔记入口
interface AttractionDetailProps {
  attraction: Attraction;
  notes: SocialNote[];
}
```

#### PhotoGallery
```tsx
// 按笔记分组展示图片
// 点击图片 → 全屏 Lightbox
// 左右切换、关闭按钮
// 移动端: 双列网格
// PC: 三列网格
interface PhotoGalleryProps {
  notes: SocialNote[];
}
```

#### Lightbox
```tsx
// 全屏图片查看器
// 左/右箭头切换
// 键盘: ← → 切换，Esc 关闭
// 移动端: 左右滑动
interface LightboxProps {
  images: SocialImage[];
  initialIndex: number;
  onClose: () => void;
}
```

#### BudgetSummary
```tsx
// 费用表格
// 按 category 分组
// 总计行
interface BudgetSummaryProps {
  items: BudgetItem[];
}
```

#### DayContent
```tsx
// 当日行程时间线
// 天气信息
// 驾驶时长
interface DayContentProps {
  day: Day;
  weather: Weather[];
  spots: Spot[];
}
```

---

## Hooks

### useAuth
```tsx
function useAuth(): {
  token: string | null;
  isLoading: boolean;
  login: (password: string) => Promise<void>;
  logout: () => void;
}
```

### useTrip
```tsx
function useTrip(tripId: number): {
  trip: Trip | null;
  isLoading: boolean;
  error: string | null;
}
```

### useAmap
```tsx
function useAmap(containerId: string, key: string): {
  map: AMap.Map | null;
  isLoaded: boolean;
}
```

### useIsMobile
```tsx
function useIsMobile(breakpoint?: number): boolean
// 默认 768px
```

---

## 响应式断点

| 断点 | 布局 |
|------|------|
| ≥768px (PC) | 地图左 55% + 内容右 45%，SlidePanel 覆盖右侧 |
| <768px (移动端) | 地图 40vh，下方卡片流，SlidePanel 全屏覆盖 |