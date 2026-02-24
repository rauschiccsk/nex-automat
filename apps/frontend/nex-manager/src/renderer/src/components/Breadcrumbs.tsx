import { type ReactElement } from 'react'
import { ChevronRight } from 'lucide-react'
import { cn } from '@renderer/lib/utils'

export interface BreadcrumbItem {
  label: string
  onClick?: () => void
}

interface BreadcrumbsProps {
  items: BreadcrumbItem[]
  className?: string
}

export default function Breadcrumbs({ items, className }: BreadcrumbsProps): ReactElement {
  return (
    <nav className={cn('flex items-center gap-1 text-sm text-gray-500', className)}>
      {items.map((item, index) => {
        const isLast = index === items.length - 1
        return (
          <span key={index} className="flex items-center gap-1">
            {item.onClick && !isLast ? (
              <button
                onClick={item.onClick}
                className="hover:text-gray-700 hover:underline transition-colors"
              >
                {item.label}
              </button>
            ) : (
              <span className={cn(isLast && 'font-medium text-gray-900')}>
                {item.label}
              </span>
            )}
            {!isLast && <ChevronRight className="h-4 w-4 text-gray-400" />}
          </span>
        )
      })}
    </nav>
  )
}
