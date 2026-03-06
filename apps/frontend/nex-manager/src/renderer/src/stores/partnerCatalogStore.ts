/**
 * Zustand store for PAB (Partner Catalog) module UI state.
 */
import { create } from 'zustand'
import type { PartnerClass } from '@renderer/types/pab'

export type PabTabId =
  | 'basic'
  | 'extensions'
  | 'addresses'
  | 'contacts'
  | 'bank-accounts'
  | 'categories'
  | 'texts'
  | 'facilities'
  | 'history'

interface PartnerCatalogState {
  // View mode
  view: 'list' | 'detail'

  // Selected partner
  selectedPartnerId: number | null

  // Detail tab
  activeTab: PabTabId

  // List filters
  searchQuery: string
  filterPartnerClass: PartnerClass
  filterIsActive: boolean | null
  filterIsSupplier: boolean | null
  filterIsCustomer: boolean | null

  // Actions
  setView: (view: 'list' | 'detail') => void
  setSelectedPartnerId: (id: number | null) => void
  setActiveTab: (tab: PabTabId) => void
  setSearchQuery: (query: string) => void
  setFilterPartnerClass: (cls: PartnerClass) => void
  setFilterIsActive: (active: boolean | null) => void
  setFilterIsSupplier: (supplier: boolean | null) => void
  setFilterIsCustomer: (customer: boolean | null) => void
  resetFilters: () => void
  openDetail: (partnerId: number) => void
  closeDetail: () => void
}

export const usePartnerCatalogStore = create<PartnerCatalogState>((set) => ({
  view: 'list',
  selectedPartnerId: null,
  activeTab: 'basic',

  searchQuery: '',
  filterPartnerClass: 'business',
  filterIsActive: null,
  filterIsSupplier: null,
  filterIsCustomer: null,

  setView: (view): void => set({ view }),
  setSelectedPartnerId: (id): void => set({ selectedPartnerId: id }),
  setActiveTab: (tab): void => set({ activeTab: tab }),
  setSearchQuery: (query): void => set({ searchQuery: query }),
  setFilterPartnerClass: (cls): void => set({ filterPartnerClass: cls }),
  setFilterIsActive: (active): void => set({ filterIsActive: active }),
  setFilterIsSupplier: (supplier): void => set({ filterIsSupplier: supplier }),
  setFilterIsCustomer: (customer): void => set({ filterIsCustomer: customer }),

  resetFilters: (): void =>
    set({
      searchQuery: '',
      filterPartnerClass: 'business',
      filterIsActive: null,
      filterIsSupplier: null,
      filterIsCustomer: null
    }),

  openDetail: (partnerId): void =>
    set({
      view: 'detail',
      selectedPartnerId: partnerId,
      activeTab: 'basic'
    }),

  closeDetail: (): void =>
    set({
      view: 'list',
      selectedPartnerId: null,
      activeTab: 'basic'
    })
}))
