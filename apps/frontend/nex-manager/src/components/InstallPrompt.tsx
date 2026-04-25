import { useEffect, useState } from 'react'

interface BeforeInstallPromptEvent extends Event {
  prompt(): Promise<void>
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>
}

const DISMISS_KEY = 'nex-pwa-install-dismissed-at'
const DISMISS_COOLDOWN_MS = 24 * 60 * 60 * 1000 // 24h

function isRecentlyDismissed(): boolean {
  const ts = localStorage.getItem(DISMISS_KEY)
  if (!ts) return false
  return Date.now() - parseInt(ts, 10) < DISMISS_COOLDOWN_MS
}

export default function InstallPrompt() {
  const [deferredPrompt, setDeferredPrompt] = useState<BeforeInstallPromptEvent | null>(null)
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    const handler = (e: Event) => {
      e.preventDefault()
      if (isRecentlyDismissed()) return
      setDeferredPrompt(e as BeforeInstallPromptEvent)
      setVisible(true)
    }
    window.addEventListener('beforeinstallprompt', handler)
    return () => window.removeEventListener('beforeinstallprompt', handler)
  }, [])

  const handleInstall = async () => {
    if (!deferredPrompt) return
    await deferredPrompt.prompt()
    await deferredPrompt.userChoice
    setDeferredPrompt(null)
    setVisible(false)
  }

  const handleDismiss = () => {
    localStorage.setItem(DISMISS_KEY, String(Date.now()))
    setDeferredPrompt(null)
    setVisible(false)
  }

  if (!visible) return null

  return (
    <div
      role="dialog"
      aria-label="Inštalovať NEX Manager"
      className="fixed bottom-4 right-4 z-50 max-w-sm rounded-lg bg-slate-900 px-4 py-3 text-white shadow-xl"
    >
      <div className="mb-2 text-sm font-medium">Nainštalovať NEX Manager</div>
      <div className="mb-3 text-xs text-slate-300">
        Pridať do plochy ako aplikáciu pre rýchlejší prístup.
      </div>
      <div className="flex justify-end gap-2">
        <button
          onClick={handleDismiss}
          className="rounded px-3 py-1 text-xs text-slate-300 hover:text-white"
        >
          Neskôr
        </button>
        <button
          onClick={handleInstall}
          className="rounded bg-white px-3 py-1 text-xs font-medium text-slate-900 hover:bg-slate-100"
        >
          Inštalovať
        </button>
      </div>
    </div>
  )
}
