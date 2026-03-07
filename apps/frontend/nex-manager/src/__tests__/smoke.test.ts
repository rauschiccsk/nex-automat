import { describe, it, expect, vi } from 'vitest'

describe('Test infrastructure smoke test', () => {
  it('vitest is configured and running', () => {
    expect(true).toBe(true)
  })

  it('jsdom environment is available', () => {
    expect(document).toBeDefined()
    expect(window).toBeDefined()
  })

  it('testing-library jest-dom matchers work', () => {
    const div = document.createElement('div')
    div.textContent = 'NEX Automat'
    document.body.appendChild(div)
    expect(div).toBeInTheDocument()
    expect(div).toHaveTextContent('NEX Automat')
    document.body.removeChild(div)
  })

  it('mock fetch is available via helper', async () => {
    const { mockFetch } = await import('./helpers/mockApi')
    const fetchMock = mockFetch({
      'GET /api/test': { data: { status: 'ok' } }
    })
    vi.stubGlobal('fetch', fetchMock)

    const response = await fetch('/api/test')
    const data = await response.json()

    expect(data).toEqual({ status: 'ok' })
    expect(fetchMock).toHaveBeenCalledTimes(1)
  })

  it('electron mock is available', () => {
    expect(window.electron).toBeDefined()
    expect(window.electron.ipcRenderer.send).toBeDefined()
  })

  it('ResizeObserver mock works (for TanStack virtualizer)', () => {
    const observer = new ResizeObserver(() => {})
    expect(observer.observe).toBeDefined()
    observer.observe(document.createElement('div'))
    expect(observer.observe).toHaveBeenCalled()
  })
})
