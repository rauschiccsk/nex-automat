import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react'

// --- Mock API with vi.hoisted ---
const mockApi = vi.hoisted(() => ({
  changeUserPassword: vi.fn(),
  changeSelfPassword: vi.fn(),
}))

vi.mock('@renderer/lib/api', () => ({
  api: mockApi,
  ApiError: class ApiError extends Error {
    status: number
    constructor(msg: string, status = 500) {
      super(msg)
      this.status = status
    }
  },
}))

const mockAddToast = vi.fn()
vi.mock('@renderer/stores/toastStore', () => ({
  useToastStore: () => ({
    addToast: mockAddToast,
  }),
}))

import ChangePasswordDialog from '@renderer/components/modules/users/ChangePasswordDialog'

const mockOnClose = vi.fn()

beforeEach(() => {
  vi.clearAllMocks()
  mockApi.changeUserPassword.mockResolvedValue({ message: 'OK' })
  mockApi.changeSelfPassword.mockResolvedValue({ message: 'OK' })
})

describe('ChangePasswordDialog — Admin mode', () => {
  it('renders heading with username', async () => {
    await act(async () => {
      render(
        <ChangePasswordDialog
          userId={1}
          username="admin"
          onClose={mockOnClose}
        />
      )
    })
    expect(screen.getByText(/Zmena hesla.*admin/)).toBeInTheDocument()
  })

  it('does not show current password field in admin mode', async () => {
    await act(async () => {
      render(
        <ChangePasswordDialog
          userId={1}
          username="admin"
          onClose={mockOnClose}
        />
      )
    })
    expect(screen.queryByText('Aktuálne heslo')).not.toBeInTheDocument()
  })

  it('shows new password and confirm password fields', async () => {
    await act(async () => {
      render(
        <ChangePasswordDialog
          userId={1}
          username="admin"
          onClose={mockOnClose}
        />
      )
    })
    expect(screen.getByText('Nové heslo')).toBeInTheDocument()
    expect(screen.getByText('Potvrdiť nové heslo')).toBeInTheDocument()
  })

  it('shows validation error for empty new password', async () => {
    await act(async () => {
      render(
        <ChangePasswordDialog
          userId={1}
          username="admin"
          onClose={mockOnClose}
        />
      )
    })
    await act(async () => {
      fireEvent.click(screen.getByText('Zmeniť heslo'))
    })
    await waitFor(() => {
      const errors = screen.getAllByText('Povinné pole')
      expect(errors.length).toBeGreaterThanOrEqual(2)
    })
  })

  it('shows validation error for short password', async () => {
    await act(async () => {
      render(
        <ChangePasswordDialog
          userId={1}
          username="admin"
          onClose={mockOnClose}
        />
      )
    })
    const newPwdInput = screen
      .getByText('Nové heslo')
      .closest('div')!
      .querySelector('input')!
    const confirmPwdInput = screen
      .getByText('Potvrdiť nové heslo')
      .closest('div')!
      .querySelector('input')!
    fireEvent.change(newPwdInput, { target: { value: '123' } })
    fireEvent.change(confirmPwdInput, { target: { value: '123' } })
    await act(async () => {
      fireEvent.click(screen.getByText('Zmeniť heslo'))
    })
    await waitFor(() => {
      expect(screen.getByText('Minimálne 6 znakov')).toBeInTheDocument()
    })
  })

  it('shows validation error when passwords do not match', async () => {
    await act(async () => {
      render(
        <ChangePasswordDialog
          userId={1}
          username="admin"
          onClose={mockOnClose}
        />
      )
    })
    const newPwdInput = screen
      .getByText('Nové heslo')
      .closest('div')!
      .querySelector('input')!
    const confirmPwdInput = screen
      .getByText('Potvrdiť nové heslo')
      .closest('div')!
      .querySelector('input')!
    fireEvent.change(newPwdInput, { target: { value: 'password123' } })
    fireEvent.change(confirmPwdInput, { target: { value: 'different' } })
    await act(async () => {
      fireEvent.click(screen.getByText('Zmeniť heslo'))
    })
    await waitFor(() => {
      expect(screen.getByText('Heslá sa nezhodujú')).toBeInTheDocument()
    })
  })

  it('calls changeUserPassword on valid submit', async () => {
    await act(async () => {
      render(
        <ChangePasswordDialog
          userId={1}
          username="admin"
          onClose={mockOnClose}
        />
      )
    })
    const newPwdInput = screen
      .getByText('Nové heslo')
      .closest('div')!
      .querySelector('input')!
    const confirmPwdInput = screen
      .getByText('Potvrdiť nové heslo')
      .closest('div')!
      .querySelector('input')!
    fireEvent.change(newPwdInput, { target: { value: 'newpass123' } })
    fireEvent.change(confirmPwdInput, { target: { value: 'newpass123' } })
    await act(async () => {
      fireEvent.click(screen.getByText('Zmeniť heslo'))
    })
    await waitFor(() => {
      expect(mockApi.changeUserPassword).toHaveBeenCalledWith(1, 'newpass123')
    })
    expect(mockAddToast).toHaveBeenCalledWith('Heslo bolo zmenené', 'success')
    expect(mockOnClose).toHaveBeenCalled()
  })

  it('calls onClose when Zrušiť clicked', async () => {
    await act(async () => {
      render(
        <ChangePasswordDialog
          userId={1}
          username="admin"
          onClose={mockOnClose}
        />
      )
    })
    fireEvent.click(screen.getByText('Zrušiť'))
    expect(mockOnClose).toHaveBeenCalled()
  })
})

describe('ChangePasswordDialog — Self mode', () => {
  it('renders "Zmena vlastného hesla" heading', async () => {
    await act(async () => {
      render(<ChangePasswordDialog onClose={mockOnClose} />)
    })
    expect(screen.getByText('Zmena vlastného hesla')).toBeInTheDocument()
  })

  it('shows current password field in self mode', async () => {
    await act(async () => {
      render(<ChangePasswordDialog onClose={mockOnClose} />)
    })
    expect(screen.getByText('Aktuálne heslo')).toBeInTheDocument()
  })

  it('calls changeSelfPassword on valid submit', async () => {
    await act(async () => {
      render(<ChangePasswordDialog onClose={mockOnClose} />)
    })
    const currentPwdInput = screen
      .getByText('Aktuálne heslo')
      .closest('div')!
      .querySelector('input')!
    const newPwdInput = screen
      .getByText('Nové heslo')
      .closest('div')!
      .querySelector('input')!
    const confirmPwdInput = screen
      .getByText('Potvrdiť nové heslo')
      .closest('div')!
      .querySelector('input')!
    fireEvent.change(currentPwdInput, { target: { value: 'oldpass' } })
    fireEvent.change(newPwdInput, { target: { value: 'newpass123' } })
    fireEvent.change(confirmPwdInput, { target: { value: 'newpass123' } })
    await act(async () => {
      fireEvent.click(screen.getByText('Zmeniť heslo'))
    })
    await waitFor(() => {
      expect(mockApi.changeSelfPassword).toHaveBeenCalledWith(
        'oldpass',
        'newpass123'
      )
    })
    expect(mockOnClose).toHaveBeenCalled()
  })

  it('shows error on wrong current password (401)', async () => {
    mockApi.changeSelfPassword.mockRejectedValue(
      Object.assign(new Error('Wrong password'), { status: 401 })
    )
    await act(async () => {
      render(<ChangePasswordDialog onClose={mockOnClose} />)
    })
    const currentPwdInput = screen
      .getByText('Aktuálne heslo')
      .closest('div')!
      .querySelector('input')!
    const newPwdInput = screen
      .getByText('Nové heslo')
      .closest('div')!
      .querySelector('input')!
    const confirmPwdInput = screen
      .getByText('Potvrdiť nové heslo')
      .closest('div')!
      .querySelector('input')!
    fireEvent.change(currentPwdInput, { target: { value: 'wrongpass' } })
    fireEvent.change(newPwdInput, { target: { value: 'newpass123' } })
    fireEvent.change(confirmPwdInput, { target: { value: 'newpass123' } })
    await act(async () => {
      fireEvent.click(screen.getByText('Zmeniť heslo'))
    })
    await waitFor(() => {
      expect(mockAddToast).toHaveBeenCalledWith(
        'Nesprávne aktuálne heslo',
        'error'
      )
    })
  })
})
