import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react'

// --- Mock stores with vi.hoisted ---
const mockLogin = vi.hoisted(() => vi.fn())
const mockLoadModules = vi.hoisted(() => vi.fn())
const mockSetTheme = vi.hoisted(() => vi.fn())

vi.mock('@renderer/stores/authStore', () => ({
  useAuthStore: () => ({
    login: mockLogin,
  }),
}))

vi.mock('@renderer/stores/moduleStore', () => ({
  useModuleStore: () => ({
    loadModules: mockLoadModules,
  }),
}))

vi.mock('@renderer/stores/uiStore', () => ({
  useUiStore: () => ({
    theme: 'light',
    setTheme: mockSetTheme,
  }),
}))

import LoginScreen from '@renderer/components/LoginScreen'

beforeEach(() => {
  vi.clearAllMocks()
  mockLogin.mockResolvedValue(undefined)
  mockLoadModules.mockResolvedValue(undefined)
})

describe('LoginScreen', () => {
  it('renders login form with title', () => {
    render(<LoginScreen />)
    expect(screen.getByText('NEX Automat')).toBeInTheDocument()
    expect(screen.getByText('Prihlásenie do systému')).toBeInTheDocument()
  })

  it('renders username input field', () => {
    render(<LoginScreen />)
    expect(screen.getByTestId('username')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Zadajte meno')).toBeInTheDocument()
  })

  it('renders password input field with type="password"', () => {
    render(<LoginScreen />)
    const passwordInput = screen.getByTestId('password')
    expect(passwordInput).toBeInTheDocument()
    expect(passwordInput).toHaveAttribute('type', 'password')
  })

  it('renders submit button', () => {
    render(<LoginScreen />)
    expect(screen.getByTestId('login-button')).toBeInTheDocument()
    expect(screen.getByText('Prihlásiť sa')).toBeInTheDocument()
  })

  it('submit button is disabled when fields are empty', () => {
    render(<LoginScreen />)
    const button = screen.getByTestId('login-button')
    expect(button).toBeDisabled()
  })

  it('submit button enables when both fields filled', () => {
    render(<LoginScreen />)
    fireEvent.change(screen.getByTestId('username'), {
      target: { value: 'admin' },
    })
    fireEvent.change(screen.getByTestId('password'), {
      target: { value: 'password123' },
    })
    const button = screen.getByTestId('login-button')
    expect(button).not.toBeDisabled()
  })

  it('calls login on form submit', async () => {
    render(<LoginScreen />)
    fireEvent.change(screen.getByTestId('username'), {
      target: { value: 'admin' },
    })
    fireEvent.change(screen.getByTestId('password'), {
      target: { value: 'password123' },
    })
    await act(async () => {
      fireEvent.click(screen.getByTestId('login-button'))
    })
    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith('admin', 'password123')
    })
  })

  it('shows error on 401 (invalid credentials)', async () => {
    mockLogin.mockRejectedValue({ status: 401, message: 'Unauthorized' })
    render(<LoginScreen />)
    fireEvent.change(screen.getByTestId('username'), {
      target: { value: 'admin' },
    })
    fireEvent.change(screen.getByTestId('password'), {
      target: { value: 'wrong' },
    })
    await act(async () => {
      fireEvent.click(screen.getByTestId('login-button'))
    })
    await waitFor(() => {
      expect(
        screen.getByText('Nesprávne prihlasovacie údaje')
      ).toBeInTheDocument()
    })
  })

  it('shows server unavailable error on status 0', async () => {
    mockLogin.mockRejectedValue({ status: 0, message: '' })
    render(<LoginScreen />)
    fireEvent.change(screen.getByTestId('username'), {
      target: { value: 'admin' },
    })
    fireEvent.change(screen.getByTestId('password'), {
      target: { value: 'test' },
    })
    await act(async () => {
      fireEvent.click(screen.getByTestId('login-button'))
    })
    await waitFor(() => {
      expect(
        screen.getByText(/Server nie je dostupný/)
      ).toBeInTheDocument()
    })
  })

  it('shows loading state during login', async () => {
    mockLogin.mockReturnValue(new Promise(() => {}))
    render(<LoginScreen />)
    fireEvent.change(screen.getByTestId('username'), {
      target: { value: 'admin' },
    })
    fireEvent.change(screen.getByTestId('password'), {
      target: { value: 'password' },
    })
    await act(async () => {
      fireEvent.click(screen.getByTestId('login-button'))
    })
    expect(screen.getByText('Prihlasovanie...')).toBeInTheDocument()
  })

  it('toggles password visibility', () => {
    render(<LoginScreen />)
    const passwordInput = screen.getByTestId('password')
    expect(passwordInput).toHaveAttribute('type', 'password')
    // Click the show/hide button (aria-label)
    const toggleBtn = screen.getByLabelText('Zobraziť heslo')
    fireEvent.click(toggleBtn)
    expect(passwordInput).toHaveAttribute('type', 'text')
  })

  it('renders theme toggle button', () => {
    render(<LoginScreen />)
    expect(screen.getByLabelText('Prepnúť tému')).toBeInTheDocument()
  })

  it('calls loadModules after successful login', async () => {
    render(<LoginScreen />)
    fireEvent.change(screen.getByTestId('username'), {
      target: { value: 'admin' },
    })
    fireEvent.change(screen.getByTestId('password'), {
      target: { value: 'password123' },
    })
    await act(async () => {
      fireEvent.click(screen.getByTestId('login-button'))
    })
    await waitFor(() => {
      expect(mockLoadModules).toHaveBeenCalled()
    })
  })
})
