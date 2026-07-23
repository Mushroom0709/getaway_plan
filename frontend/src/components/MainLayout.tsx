import { useIsMobile } from '../hooks/useIsMobile'

interface MainLayoutProps {
  mapPanel: React.ReactNode
  contentPanel: React.ReactNode
  slidePanel?: React.ReactNode
}

export default function MainLayout({ mapPanel, contentPanel, slidePanel }: MainLayoutProps) {
  const isMobile = useIsMobile()

  if (isMobile) {
    return (
      <div className="flex flex-col min-h-screen">
        <div className="h-[40vh] relative">{mapPanel}</div>
        <div className="flex-1 overflow-auto px-4 py-3">{contentPanel}</div>
        {slidePanel}
      </div>
    )
  }

  return (
    <div className="h-screen grid grid-cols-[55%_45%]">
      <div className="relative h-full">{mapPanel}</div>
      <div className="overflow-auto p-6">{contentPanel}</div>
      {slidePanel}
    </div>
  )
}
