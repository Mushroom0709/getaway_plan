import { useState } from 'react'
import type { SocialNote } from '../types'
import Lightbox from './Lightbox'

interface PhotoGalleryProps {
  notes: SocialNote[]
}

export default function PhotoGallery({ notes }: PhotoGalleryProps) {
  const [lightboxIndex, setLightboxIndex] = useState<{ noteIdx: number; imgIdx: number } | null>(null)

  const allImages = notes.flatMap((n, ni) =>
    n.images.map((img, ii) => ({ ...img, noteIdx: ni, imgIdx: ii, author: n.author, platform: n.platform }))
  )

  return (
    <div className="space-y-6">
      {notes.map((note, ni) => (
        <div key={note.id}>
          <div className="flex items-center gap-2 mb-2">
            <span className="text-xs font-medium text-[var(--accent)] uppercase">{note.platform}</span>
            <span className="text-sm text-[var(--text-secondary)]">{note.author}</span>
          </div>
          {note.title && <p className="text-sm text-[var(--text-primary)] mb-2">{note.title}</p>}
          <div className="grid grid-cols-3 max-sm:grid-cols-2 gap-2">
            {note.images.map((img, ii) => (
              <button
                key={img.id}
                onClick={() => setLightboxIndex({ noteIdx: ni, imgIdx: ii })}
                className="aspect-square bg-[var(--canvas)] rounded-lg overflow-hidden"
              >
                {img.url && <img src={img.url} alt="" className="w-full h-full object-cover" loading="lazy" />}
              </button>
            ))}
          </div>
        </div>
      ))}
      {lightboxIndex && (
        <Lightbox
          images={allImages}
          initialIndex={allImages.findIndex(
            img => img.noteIdx === lightboxIndex.noteIdx && img.imgIdx === lightboxIndex.imgIdx
          )}
          onClose={() => setLightboxIndex(null)}
        />
      )}
    </div>
  )
}
