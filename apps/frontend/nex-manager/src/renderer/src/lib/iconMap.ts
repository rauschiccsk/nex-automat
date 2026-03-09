/**
 * Lucide icon mapping for dynamic module rendering.
 *
 * Maps icon name strings (from module_registry.yaml / API) to actual
 * Lucide React icon components. Used by Sidebar and other components
 * that render module icons dynamically.
 */

import {
  Users,
  Package,
  Layers,
  ArrowDownToLine,
  ArrowUpFromLine,
  ArrowLeftRight,
  ClipboardCheck,
  FileText,
  FileHeart,
  ShoppingCart,
  Truck,
  FileInput,
  ClipboardList,
  BookOpen,
  Calculator,
  Receipt,
  ListTree,
  Banknote,
  Lock,
  UserCog,
  Shield,
  Settings,
  ScrollText,
  Database,
  Building2,
  ShoppingBag,
  type LucideIcon
} from 'lucide-react'

/**
 * Map of icon name → Lucide component.
 * Keys must match the `icon` field in module_registry.yaml.
 */
export const ICON_MAP: Record<string, LucideIcon> = {
  Users,
  Package,
  Layers,
  ArrowDownToLine,
  ArrowUpFromLine,
  ArrowLeftRight,
  ClipboardCheck,
  FileText,
  FileHeart,
  ShoppingCart,
  Truck,
  FileInput,
  ClipboardList,
  BookOpen,
  Calculator,
  Receipt,
  ListTree,
  Banknote,
  Lock,
  UserCog,
  Shield,
  Settings,
  ScrollText,
  Database,
  Building2,
  ShoppingBag
}

/**
 * Get a Lucide icon component by name, with fallback to Package.
 */
export function getIcon(name: string | undefined): LucideIcon {
  if (!name) return Package
  return ICON_MAP[name] ?? Package
}
