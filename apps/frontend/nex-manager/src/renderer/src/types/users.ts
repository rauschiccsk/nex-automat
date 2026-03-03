/**
 * Types for user management module (USR).
 * Matches API schemas from nex-manager-api/users/schemas.py
 */

export interface UserGroup {
  group_id: number
  group_name: string
}

export interface User {
  user_id: number
  login_name: string
  full_name: string
  email: string | null
  is_active: boolean
  last_login_at: string | null
  created_at: string
  updated_at: string | null
  groups: UserGroup[]
}

export interface UserListResponse {
  users: User[]
  total: number
}

export interface CreateUserPayload {
  username: string
  full_name: string
  email: string
  password: string
  is_active?: boolean
  group_ids?: number[]
}

export interface UpdateUserPayload {
  full_name?: string
  email?: string
  is_active?: boolean
  group_ids?: number[]
}

export interface ChangePasswordPayload {
  new_password: string
}

export interface SelfChangePasswordPayload {
  current_password: string
  new_password: string
}
