import { useState, useEffect, useCallback } from 'react'
import { CaretLeft, CaretRight, X } from '@phosphor-icons/react'

interface Image {
  url?: string
  url_large?: string
  width?: number
  height?: number
  author?: string
  platform?: string
}

interface LightboxProps {
  images: Image[]
  initialIndex: number
  onClose: () => void
}

export default function Lightbox({ images, initialIndex, onClose }: LightboxProps) {
  const [index, setIndex] = useState(initialIndex)

  const goPrev = useCallback(() => setIndex(i => (i > 0 ? i - 1 : images.length - 1)), [images.length])
  const goNext = useCallback(() => setIndex(i => (i < images.length - 1 ? i + 1 : 0)), [images.length])

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
      if (e.key === 'ArrowLeft') goPrev()
      if (e.key === 'ArrowRight') goNext()
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [onClose, goPrev, goNext])

  const current = images[index]

  return (
    <div className="fixed inset-0 z-50 bg-black/95 flex items-center justify-center">
      <button onClick={onClose} className="absolute top-4 right-4 text-white/70 hover:text-white z-10">
        <X size={28} />
      </button>
      <button onClick={goPrev} className="absolute left-4 text-white/70 hover:text-white">
        <CaretLeft size={36} />
      </button>
      <div className="max-w-[90vw] max-h-[90vh] flex flex-col items-center">
        {current.url_large && (
          <img src={current.url_large} alt="" className="max-w-full max-h-[85vh] object-contain rounded-lg" />
        )}
        {current.author && (
          <span className="text-white/50 text-sm mt-3">
            @{current.author} · {current.platform}
          </span>
        )}
        <span className="text-white/30 text-xs mt-1">{index + 1} / {images.length}</span>
      </div>
      <button onClick={goNext} className="absolute right-4 text-white/70 hover:text-white">
        <CaretRight size={36} />
      </button>
    </div>
  )
}
