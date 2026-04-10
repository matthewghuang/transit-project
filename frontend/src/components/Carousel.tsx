import React, { useCallback, useEffect, useState } from 'react'
import useEmblaCarousel from 'embla-carousel-react'

interface CarouselProps {
  children: React.ReactNode[]
}

export const Carousel: React.FC<CarouselProps> = ({ children }) => {
  const [emblaRef, emblaApi] = useEmblaCarousel({
    align: 'start',
    containScroll: 'trimSnaps',
    slidesToScroll: 1,
  })

  const [prevBtnEnabled, setPrevBtnEnabled] = useState(false)
  const [nextBtnEnabled, setNextBtnEnabled] = useState(false)

  const scrollPrev = useCallback(() => emblaApi && emblaApi.scrollPrev(), [emblaApi])
  const scrollNext = useCallback(() => emblaApi && emblaApi.scrollNext(), [emblaApi])

  const onSelect = useCallback(() => {
    if (!emblaApi) return
    setPrevBtnEnabled(emblaApi.canScrollPrev())
    setNextBtnEnabled(emblaApi.canScrollNext())
  }, [emblaApi])

  useEffect(() => {
    if (!emblaApi) return
    onSelect()
    emblaApi.on('select', onSelect)
    emblaApi.on('reInit', onSelect)
  }, [emblaApi, onSelect])

  return (
    <div className="embla">
      <div className="embla__viewport" ref={emblaRef}>
        <div className="embla__container">
          {children.map((child, index) => (
            <div className="embla__slide" key={index}>
              {child}
            </div>
          ))}
        </div>
      </div>
      
      <button 
        className="embla__prev" 
        onClick={scrollPrev} 
        disabled={!prevBtnEnabled}
        aria-label="Previous slide"
      >
        &lsaquo;
      </button>
      <button 
        className="embla__next" 
        onClick={scrollNext} 
        disabled={!nextBtnEnabled}
        aria-label="Next slide"
      >
        &rsaquo;
      </button>
    </div>
  )
}
