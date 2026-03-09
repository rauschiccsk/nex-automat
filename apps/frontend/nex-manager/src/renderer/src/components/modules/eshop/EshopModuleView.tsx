import { type ReactElement } from 'react'
import { useEshopStore } from '@renderer/stores/eshopStore'
import EshopOrderList from './EshopOrderList'
import EshopOrderDetail from './EshopOrderDetail'
import EshopProductList from './EshopProductList'
import EshopProductForm from './EshopProductForm'
import EshopTenantList from './EshopTenantList'

type EshopTab = 'orders' | 'products' | 'tenants'

const TABS: { id: EshopTab; label: string }[] = [
  { id: 'orders', label: 'Objednávky' },
  { id: 'products', label: 'Produkty' },
  { id: 'tenants', label: 'Tenanty' }
]

function getActiveTab(view: string): EshopTab {
  if (view === 'products' || view === 'product-edit') return 'products'
  if (view === 'tenants') return 'tenants'
  return 'orders'
}

/**
 * Main ESHOP module view — sub-navigation tabs + content routing based on store state.
 */
export default function EshopModuleView(): ReactElement {
  const { view, setView } = useEshopStore()
  const activeTab = getActiveTab(view)

  const handleTabClick = (tab: EshopTab): void => {
    setView(tab)
  }

  const renderContent = (): ReactElement => {
    switch (view) {
      case 'order-detail':
        return <EshopOrderDetail />
      case 'products':
        return <EshopProductList />
      case 'product-edit':
        return <EshopProductForm />
      case 'tenants':
        return <EshopTenantList />
      default:
        return <EshopOrderList />
    }
  }

  return (
    <div data-testid="eshop-module" className="flex flex-col h-full">
      {/* Sub-navigation tabs */}
      {view !== 'order-detail' && view !== 'product-edit' && (
        <div className="flex border-b border-gray-200 dark:border-gray-700 shrink-0 mb-3">
          {TABS.map((tab) => (
            <button
              key={tab.id}
              data-testid={`eshop-tab-${tab.id}`}
              onClick={() => handleTabClick(tab.id)}
              className={
                'px-4 py-2.5 text-sm font-medium border-b-2 transition-colors whitespace-nowrap ' +
                (activeTab === tab.id
                  ? 'border-blue-600 text-blue-600 dark:text-blue-400 dark:border-blue-400'
                  : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300')
              }
            >
              {tab.label}
            </button>
          ))}
        </div>
      )}

      {/* Content */}
      <div className="flex-1 overflow-auto">
        {renderContent()}
      </div>
    </div>
  )
}
