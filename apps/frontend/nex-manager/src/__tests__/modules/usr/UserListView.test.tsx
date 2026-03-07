import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react'
import type { User, UserListResponse } from '@renderer/types/users'

// --- Mock API with vi.hoisted ---
const mockApi = vi.hoisted(() => ({
  getUsers: vi.fn(),
  getUser: vi.fn(),
  createUser: vi.fn(),
  updateUser: vi.fn(),
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

// --- Mock stores ---
vi.mock('@renderer/stores/authStore', () => ({
  useAuthStore: () => ({
    checkPermission: vi.fn().mockReturnValue(true),
  }),
}))

const mockAddToast = vi.fn()
vi.mock('@renderer/stores/toastStore', () => ({
  useToastStore: () => ({
    addToast: mockAddToast,
  }),
}))

import UserListView from '@renderer/components/modules/users/UserListView'

// --- Mock users ---
const mockUsers: User[] = [
  {
    user_id: 1,
    login_name: 'admin',
    full_name: 'Administrator',
    email: 'admin@icc.sk',
    is_active: true,
    last_login_at: '2025-06-01T10:00:00Z',
    created_at: '2025-01-01T00:00:00Z',
    updated_at: '2025-06-01T10:00:00Z',
    groups: [{ group_id: 1, group_name: 'Administrators' }],
  },
  {
    user_id: 2,
    login_name: 'jnovak',
    full_name: 'Jan Novak',
    email: 'jan.novak@icc.sk',
    is_active: true,
    last_login_at: null,
    created_at: '2025-03-01T00:00:00Z',
    updated_at: null,
    groups: [{ group_id: 2, group_name: 'Users' }],
  },
  {
    user_id: 3,
    login_name: 'pkoval',
    full_name: 'Peter Koval',
    email: null,
    is_active: false,
    last_login_at: null,
    created_at: '2025-02-01T00:00:00Z',
    updated_at: null,
    groups: [],
  },
]

const mockUserListResponse: UserListResponse = {
  users: mockUsers,
  total: 3,
}

beforeEach(() => {
  vi.clearAllMocks()
  localStorage.clear()
  mockApi.getUsers.mockResolvedValue(mockUserListResponse)
  mockApi.updateUser.mockResolvedValue(mockUsers[0])
})

describe('UserListView', () => {
  it('renders heading "Používatelia"', async () => {
    render(<UserListView />)
    expect(screen.getByText('Používatelia')).toBeInTheDocument()
  })

  it('shows loading state initially', () => {
    mockApi.getUsers.mockReturnValue(new Promise(() => {}))
    render(<UserListView />)
    // Loading spinner visible, no table
    expect(screen.queryByTestId('user-table')).not.toBeInTheDocument()
  })

  it('fetches and displays user data in table', async () => {
    render(<UserListView />)
    await waitFor(() => {
      expect(screen.getByTestId('user-table')).toBeInTheDocument()
    })
    expect(screen.getByText('admin')).toBeInTheDocument()
    expect(screen.getByText('Administrator')).toBeInTheDocument()
    expect(screen.getByText('admin@icc.sk')).toBeInTheDocument()
    expect(screen.getByText('jnovak')).toBeInTheDocument()
    expect(screen.getByText('Jan Novak')).toBeInTheDocument()
  })

  it('shows active/inactive status badges', async () => {
    render(<UserListView />)
    await waitFor(() => {
      expect(screen.getByTestId('user-table')).toBeInTheDocument()
    })
    // "Aktívny" appears as badge for each active user + column header
    const activeBadges = screen.getAllByText('Aktívny')
    expect(activeBadges.length).toBeGreaterThanOrEqual(2) // at least 2 active user badges
    const inactiveBadges = screen.getAllByText('Neaktívny')
    expect(inactiveBadges.length).toBeGreaterThanOrEqual(1) // at least 1 inactive
  })

  it('shows group names in table', async () => {
    render(<UserListView />)
    await waitFor(() => {
      // "Administrators" appears in both group filter <select> and table cell
      expect(screen.getAllByText('Administrators').length).toBeGreaterThanOrEqual(1)
    })
    // "Users" appears in both filter select and table cell
    expect(screen.getAllByText('Users').length).toBeGreaterThanOrEqual(1)
  })

  it('renders search input', async () => {
    render(<UserListView />)
    expect(
      screen.getByPlaceholderText('Hľadať meno, login, email…')
    ).toBeInTheDocument()
  })

  it('renders "Nový používateľ" create button', async () => {
    render(<UserListView />)
    expect(screen.getByText('Nový používateľ')).toBeInTheDocument()
  })

  it('renders active/inactive filter buttons', async () => {
    render(<UserListView />)
    expect(screen.getByText('Všetci')).toBeInTheDocument()
    expect(screen.getByText('Aktívni')).toBeInTheDocument()
    expect(screen.getByText('Neaktívni')).toBeInTheDocument()
  })

  it('shows error toast on API failure', async () => {
    mockApi.getUsers.mockRejectedValue({ message: 'Network error' })
    render(<UserListView />)
    await waitFor(() => {
      expect(mockAddToast).toHaveBeenCalledWith(
        expect.any(String),
        'error'
      )
    })
  })

  it('shows empty state when no users', async () => {
    mockApi.getUsers.mockResolvedValue({ users: [], total: 0 })
    render(<UserListView />)
    await waitFor(() => {
      expect(screen.getByText('Žiadni používatelia')).toBeInTheDocument()
    })
  })

  it('opens create dialog on "Nový používateľ" click', async () => {
    render(<UserListView />)
    await waitFor(() => {
      expect(screen.getByTestId('user-table')).toBeInTheDocument()
    })
    fireEvent.click(screen.getByText('Nový používateľ'))
    await waitFor(() => {
      // Dialog should have "Používateľské meno" label — this is unique to the dialog
      expect(screen.getByText('Používateľské meno')).toBeInTheDocument()
      expect(screen.getByText('Celé meno')).toBeInTheDocument()
    })
  })

  it('renders table headers correctly', async () => {
    render(<UserListView />)
    await waitFor(() => {
      expect(screen.getByTestId('user-table')).toBeInTheDocument()
    })
    expect(screen.getByText('Username')).toBeInTheDocument()
    expect(screen.getByText('Meno')).toBeInTheDocument()
    expect(screen.getByText('Email')).toBeInTheDocument()
    expect(screen.getByText('Skupiny')).toBeInTheDocument()
    // "Aktívny" column header exists
    const headers = screen.getAllByRole('columnheader')
    expect(headers.length).toBeGreaterThanOrEqual(6)
  })

  it('renders edit buttons for users', async () => {
    render(<UserListView />)
    await waitFor(() => {
      expect(screen.getByTestId('user-table')).toBeInTheDocument()
    })
    const editButtons = screen.getAllByTitle('Upraviť')
    expect(editButtons.length).toBe(3)
  })

  it('renders change password buttons for users', async () => {
    render(<UserListView />)
    await waitFor(() => {
      expect(screen.getByTestId('user-table')).toBeInTheDocument()
    })
    const pwdButtons = screen.getAllByTitle('Zmeniť heslo')
    expect(pwdButtons.length).toBe(3)
  })
})
