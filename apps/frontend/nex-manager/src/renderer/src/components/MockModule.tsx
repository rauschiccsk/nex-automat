import { type ReactElement } from 'react'
import { cn } from '@renderer/lib/utils'

interface MockModuleProps {
  title: string
  description?: string
  icon?: ReactElement
  className?: string
}

export default function MockModule({
  title,
  description,
  icon,
  className
}: MockModuleProps): ReactElement {
  return (
    <div
      className={cn(
        'rounded-xl border border-dashed border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-800/50 p-6 text-center',
        className
      )}
    >
      {icon && <div className="mb-3 flex justify-center text-gray-400 dark:text-gray-500">{icon}</div>}
      <h3 className="text-lg font-semibold text-gray-600 dark:text-gray-300">{title}</h3>
      {description && (
        <p className="mt-1 text-sm text-gray-400 dark:text-gray-500">{description}</p>
      )}
    </div>
  )
}
