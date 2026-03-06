import { type ReactElement } from 'react'
import { usePartnerCatalogStore } from '@renderer/stores/partnerCatalogStore'
import PabPartnerList from './PabPartnerList'
import PabPartnerDetail from './PabPartnerDetail'

/**
 * Main PAB module view — switches between list and detail based on store state.
 */
export default function PabModuleView(): ReactElement {
  const { view } = usePartnerCatalogStore()

  if (view === 'detail') {
    return <PabPartnerDetail />
  }

  return <PabPartnerList />
}
