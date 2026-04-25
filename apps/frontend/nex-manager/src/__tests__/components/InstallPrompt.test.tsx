import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, act } from '@testing-library/react'
import InstallPrompt from '@renderer/components/InstallPrompt'

function fireBeforeInstallPrompt() {
  const event = new Event('beforeinstallprompt') as Event & {
    prompt: () => Promise<void>
    userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>
  }
  event.prompt = vi.fn().mockResolvedValue(undefined)
  event.userChoice = Promise.resolve({ outcome: 'accepted' as const })
  window.dispatchEvent(event)
  return event
}

describe('InstallPrompt', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it('renders nothing initially (no beforeinstallprompt fired)', () => {
    const { container } = render(<InstallPrompt />)
    expect(container).toBeEmptyDOMElement()
  })

  it('shows toast after beforeinstallprompt event', () => {
    render(<InstallPrompt />)
    act(() => {
      fireBeforeInstallPrompt()
    })
    expect(screen.getByRole('dialog')).toBeInTheDocument()
    expect(screen.getByText('Nainštalovať NEX Manager')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Inštalovať' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Neskôr' })).toBeInTheDocument()
  })

  it('dismisses and stores cooldown on Neskôr click', () => {
    render(<InstallPrompt />)
    act(() => {
      fireBeforeInstallPrompt()
    })
    fireEvent.click(screen.getByRole('button', { name: 'Neskôr' }))
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
    expect(localStorage.getItem('nex-pwa-install-dismissed-at')).not.toBeNull()
  })

  it('does not show toast if recently dismissed', () => {
    localStorage.setItem('nex-pwa-install-dismissed-at', String(Date.now()))
    render(<InstallPrompt />)
    act(() => {
      fireBeforeInstallPrompt()
    })
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
  })
})
