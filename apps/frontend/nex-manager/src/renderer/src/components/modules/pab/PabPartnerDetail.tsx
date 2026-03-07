import { useState, useEffect, useCallback, type ReactElement } from 'react'
import { ArrowLeft, Loader2, AlertCircle } from 'lucide-react'
import { cn } from '@renderer/lib/utils'
import { api, type ApiError } from '@renderer/lib/api'
import { useToastStore } from '@renderer/stores/toastStore'
import { usePartnerCatalogStore, type PabTabId } from '@renderer/stores/partnerCatalogStore'
import type { PartnerCatalog } from '@renderer/types/pab'
import PabBasicTab from './tabs/PabBasicTab'
import PabExtensionsTab from './tabs/PabExtensionsTab'
import PabAddressesTab from './tabs/PabAddressesTab'
import PabContactsTab from './tabs/PabContactsTab'
import PabBankAccountsTab from './tabs/PabBankAccountsTab'
import PabCategoriesTab from './tabs/PabCategoriesTab'
import PabTextsTab from './tabs/PabTextsTab'
import PabFacilitiesTab from './tabs/PabFacilitiesTab'
import PabHistoryTab from './tabs/PabHistoryTab'

const TABS: { id: PabTabId; label: string }[] = [
  { id: 'basic', label: 'Základné' },
  { id: 'extensions', label: 'Rozšírené' },
  { id: 'addresses', label: 'Adresy' },
  { id: 'contacts', label: 'Kontakty' },
  { id: 'bank-accounts', label: 'Bankové účty' },
  { id: 'categories', label: 'Skupiny' },
  { id: 'texts', label: 'Texty' },
  { id: 'facilities', label: 'Prevádzkarne' },
  { id: 'history', label: 'História' }
]

export default function PabPartnerDetail(): ReactElement {
  const { addToast } = useToastStore()
  const { selectedPartnerId, activeTab, setActiveTab, closeDetail } = usePartnerCatalogStore()

  const [partner, setPartner] = useState<PartnerCatalog | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchPartner = useCallback(async (): Promise<void> => {
    if (selectedPartnerId === null) return
    setLoading(true)
    setError(null)
    try {
      const p = await api.getPabPartner(selectedPartnerId)
      setPartner(p)
    } catch (err) {
      const e = err as ApiError
      const msg = e.message || 'Nepodarilo sa načítať partnera'
      setError(msg)
      addToast(msg, 'error')
    } finally {
      setLoading(false)
    }
  }, [selectedPartnerId, addToast])

  useEffect(() => {
    void fetchPartner()
  }, [fetchPartner])

  const handlePartnerUpdated = useCallback((): void => {
    void fetchPartner()
  }, [fetchPartner])

  if (loading) {
    return (
      <div className="flex items-center justify-center py-16">
        <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
        <span className="ml-3 text-gray-500 dark:text-gray-400">Načítavam...</span>
      </div>
    )
  }

  if (error || !partner) {
    return (
      <div className="flex flex-col items-center justify-center py-16 gap-4">
        <AlertCircle className="h-8 w-8 text-red-500" />
        <p className="text-sm text-red-700 dark:text-red-400">{error || 'Partner nenájdený'}</p>
        <button
          onClick={closeDetail}
          className="px-4 py-2 rounded-lg text-sm font-medium bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
        >
          Späť na zoznam
        </button>
      </div>
    )
  }

  const renderTab = (): ReactElement => {
    switch (activeTab) {
      case 'basic':
        return <PabBasicTab partner={partner} onUpdated={handlePartnerUpdated} onDeleted={closeDetail} />
      case 'extensions':
        return <PabExtensionsTab partnerId={partner.partner_id} />
      case 'addresses':
        return <PabAddressesTab partnerId={partner.partner_id} />
      case 'contacts':
        return <PabContactsTab partnerId={partner.partner_id} />
      case 'bank-accounts':
        return <PabBankAccountsTab partnerId={partner.partner_id} />
      case 'categories':
        return <PabCategoriesTab partnerId={partner.partner_id} />
      case 'texts':
        return <PabTextsTab partnerId={partner.partner_id} />
      case 'facilities':
        return <PabFacilitiesTab partnerId={partner.partner_id} />
      case 'history':
        return <PabHistoryTab partnerId={partner.partner_id} />
    }
  }

  return (
    <div className="flex flex-col h-full gap-3">
      {/* Header */}
      <div className="flex items-center gap-3 shrink-0">
        <button
          onClick={closeDetail}
          className="p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
          title="Späť na zoznam"
        >
          <ArrowLeft className="h-5 w-5" />
        </button>
        <div>
          <h1 className="text-xl font-semibold text-gray-900 dark:text-white">
            Partner: {partner.partner_name}
          </h1>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            ID: {partner.partner_id} | Verzia: {partner.modify_id}
          </p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-gray-200 dark:border-gray-700 shrink-0 overflow-x-auto">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={cn(
              'px-4 py-2.5 text-sm font-medium border-b-2 transition-colors whitespace-nowrap',
              activeTab === tab.id
                ? 'border-blue-600 text-blue-600 dark:text-blue-400 dark:border-blue-400'
                : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
            )}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab content */}
      <div className="flex-1 overflow-auto">
        {renderTab()}
      </div>
    </div>
  )
}
