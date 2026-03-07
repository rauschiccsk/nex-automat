import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react'
import type { User } from '@renderer/types/users'

// --- Mock API with vi.hoisted ---
const mockApi = vi.hoisted(() => ({
  getUsers: vi.fn(),
  createUser: vi.fn(),
  updateUser: vi.fn(),
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

import UserFormDialog from '@renderer/components/modules/users/UserFormDialog'

const mockOnClose = vi.fn()

const existingUser: User = {
  user_id: 1,
  login_name: 'admin',
  full_name: 'Administrator',
  email: 'admin@icc.sk',
  is_active: true,
  last_login_at: '2025-06-01T10:00:00Z',
  created_at: '2025-01-01T00:00:00Z',
  updated_at: null,
  groups: [{ group_id: 1, group_name: 'Administrators' }],
}

beforeEach(() => {
  vi.clearAllMocks()
  mockApi.getUsers.mockResolvedValue({
    users: [existingUser],
    total: 1,
  })
  mockApi.createUser.mockResolvedValue({
    user_id: 10,
    login_name: 'newuser',
    full_name: 'New User',
    email: 'new@icc.sk',
    is_active: true,
    last_login_at: null,
    created_at: '2025-06-01T00:00:00Z',
    updated_at: null,
    groups: [],
  })
  mockApi.updateUser.mockResolvedValue({
    ...existingUser,
    full_name: 'Updated Admin',
  })
})

describe('UserFormDialog — Create mode', () => {
  it('renders "Nový používateľ" heading', async () => {
    await act(async () => {
      render(<UserFormDialog user={null} onClose={mockOnClose} />)
    })
    expect(screen.getByText('Nový používateľ')).toBeInTheDocument()
  })

  it('renders username, full name, email, and password fields', async () => {
    await act(async () => {
      render(<UserFormDialog user={null} onClose={mockOnClose} />)
    })
    expect(screen.getByText('Používateľské meno')).toBeInTheDocument()
    expect(screen.getByText('Celé meno')).toBeInTheDocument()
    expect(screen.getByText('E-mail')).toBeInTheDocument()
    expect(screen.getByText('Heslo')).toBeInTheDocument()
  })

  it('shows Vytvoriť button', async () => {
    await act(async () => {
      render(<UserFormDialog user={null} onClose={mockOnClose} />)
    })
    expect(screen.getByText('Vytvoriť')).toBeInTheDocument()
  })

  it('shows validation errors for empty required fields', async () => {
    await act(async () => {
      render(<UserFormDialog user={null} onClose={mockOnClose} />)
    })
    await act(async () => {
      fireEvent.click(screen.getByText('Vytvoriť'))
    })
    await waitFor(() => {
      // Should show at least one "Povinné pole" error
      const errors = screen.getAllByText('Povinné pole')
      expect(errors.length).toBeGreaterThanOrEqual(3)
    })
  })

  it('shows email validation error for invalid format', async () => {
    await act(async () => {
      render(<UserFormDialog user={null} onClose={mockOnClose} />)
    })
    // Fill email with invalid value
    const emailInput = screen
      .getByText('E-mail')
      .closest('div')!
      .querySelector('input')!
    fireEvent.change(emailInput, { target: { value: 'notanemail' } })
    // Fill other required fields
    const usernameInput = screen
      .getByText('Používateľské meno')
      .closest('div')!
      .querySelector('input')!
    const fullNameInput = screen
      .getByText('Celé meno')
      .closest('div')!
      .querySelector('input')!
    const passwordInput = screen
      .getByText('Heslo')
      .closest('div')!
      .querySelector('input')!
    fireEvent.change(usernameInput, { target: { value: 'test' } })
    fireEvent.change(fullNameInput, { target: { value: 'Test User' } })
    fireEvent.change(passwordInput, { target: { value: 'password123' } })
    await act(async () => {
      fireEvent.click(screen.getByText('Vytvoriť'))
    })
    await waitFor(() => {
      expect(
        screen.getByText('Neplatný formát e-mailu')
      ).toBeInTheDocument()
    })
  })

  it('shows password minimum length validation', async () => {
    await act(async () => {
      render(<UserFormDialog user={null} onClose={mockOnClose} />)
    })
    const usernameInput = screen
      .getByText('Používateľské meno')
      .closest('div')!
      .querySelector('input')!
    const fullNameInput = screen
      .getByText('Celé meno')
      .closest('div')!
      .querySelector('input')!
    const emailInput = screen
      .getByText('E-mail')
      .closest('div')!
      .querySelector('input')!
    const passwordInput = screen
      .getByText('Heslo')
      .closest('div')!
      .querySelector('input')!
    fireEvent.change(usernameInput, { target: { value: 'test' } })
    fireEvent.change(fullNameInput, { target: { value: 'Test' } })
    fireEvent.change(emailInput, { target: { value: 'test@icc.sk' } })
    fireEvent.change(passwordInput, { target: { value: '12345' } })
    await act(async () => {
      fireEvent.click(screen.getByText('Vytvoriť'))
    })
    await waitFor(() => {
      expect(screen.getByText('Minimálne 6 znakov')).toBeInTheDocument()
    })
  })

  it('calls createUser on valid submit', async () => {
    await act(async () => {
      render(<UserFormDialog user={null} onClose={mockOnClose} />)
    })
    const usernameInput = screen
      .getByText('Používateľské meno')
      .closest('div')!
      .querySelector('input')!
    const fullNameInput = screen
      .getByText('Celé meno')
      .closest('div')!
      .querySelector('input')!
    const emailInput = screen
      .getByText('E-mail')
      .closest('div')!
      .querySelector('input')!
    const passwordInput = screen
      .getByText('Heslo')
      .closest('div')!
      .querySelector('input')!
    fireEvent.change(usernameInput, { target: { value: 'newuser' } })
    fireEvent.change(fullNameInput, { target: { value: 'New User' } })
    fireEvent.change(emailInput, { target: { value: 'new@icc.sk' } })
    fireEvent.change(passwordInput, { target: { value: 'password123' } })
    await act(async () => {
      fireEvent.click(screen.getByText('Vytvoriť'))
    })
    await waitFor(() => {
      expect(mockApi.createUser).toHaveBeenCalledWith(
        expect.objectContaining({
          username: 'newuser',
          full_name: 'New User',
          email: 'new@icc.sk',
          password: 'password123',
        })
      )
    })
    expect(mockOnClose).toHaveBeenCalledWith(true)
  })

  it('handles 409 duplicate username error', async () => {
    mockApi.createUser.mockRejectedValue(
      Object.assign(new Error('Duplicate'), { status: 409 })
    )
    await act(async () => {
      render(<UserFormDialog user={null} onClose={mockOnClose} />)
    })
    const usernameInput = screen
      .getByText('Používateľské meno')
      .closest('div')!
      .querySelector('input')!
    const fullNameInput = screen
      .getByText('Celé meno')
      .closest('div')!
      .querySelector('input')!
    const emailInput = screen
      .getByText('E-mail')
      .closest('div')!
      .querySelector('input')!
    const passwordInput = screen
      .getByText('Heslo')
      .closest('div')!
      .querySelector('input')!
    fireEvent.change(usernameInput, { target: { value: 'admin' } })
    fireEvent.change(fullNameInput, { target: { value: 'Admin' } })
    fireEvent.change(emailInput, { target: { value: 'a@b.sk' } })
    fireEvent.change(passwordInput, { target: { value: 'password' } })
    await act(async () => {
      fireEvent.click(screen.getByText('Vytvoriť'))
    })
    await waitFor(() => {
      expect(mockAddToast).toHaveBeenCalledWith(
        'Používateľské meno už existuje',
        'error'
      )
    })
  })

  it('calls onClose(false) when Zrušiť clicked', async () => {
    await act(async () => {
      render(<UserFormDialog user={null} onClose={mockOnClose} />)
    })
    fireEvent.click(screen.getByText('Zrušiť'))
    expect(mockOnClose).toHaveBeenCalledWith(false)
  })
})

describe('UserFormDialog — Edit mode', () => {
  it('renders "Upraviť používateľa" heading', async () => {
    await act(async () => {
      render(<UserFormDialog user={existingUser} onClose={mockOnClose} />)
    })
    expect(screen.getByText('Upraviť používateľa')).toBeInTheDocument()
  })

  it('shows Uložiť button instead of Vytvoriť', async () => {
    await act(async () => {
      render(<UserFormDialog user={existingUser} onClose={mockOnClose} />)
    })
    expect(screen.getByText('Uložiť')).toBeInTheDocument()
    expect(screen.queryByText('Vytvoriť')).not.toBeInTheDocument()
  })

  it('does not show password field in edit mode', async () => {
    await act(async () => {
      render(<UserFormDialog user={existingUser} onClose={mockOnClose} />)
    })
    expect(screen.queryByText('Heslo')).not.toBeInTheDocument()
  })

  it('shows readonly username in edit mode', async () => {
    await act(async () => {
      render(<UserFormDialog user={existingUser} onClose={mockOnClose} />)
    })
    // Username field should be displayed as read-only text, not an input
    expect(screen.getByText('admin')).toBeInTheDocument()
  })

  it('calls updateUser on submit in edit mode', async () => {
    await act(async () => {
      render(<UserFormDialog user={existingUser} onClose={mockOnClose} />)
    })
    // Change full name
    const fullNameInput = screen
      .getByText('Celé meno')
      .closest('div')!
      .querySelector('input')!
    fireEvent.change(fullNameInput, { target: { value: 'Updated Admin' } })
    await act(async () => {
      fireEvent.click(screen.getByText('Uložiť'))
    })
    await waitFor(() => {
      expect(mockApi.updateUser).toHaveBeenCalledWith(
        1,
        expect.objectContaining({
          full_name: 'Updated Admin',
        })
      )
    })
    expect(mockOnClose).toHaveBeenCalledWith(true)
  })
})
