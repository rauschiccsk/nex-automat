import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  FileText, 
  CheckCircle, 
  Settings,
  Clock
} from 'lucide-react';
import { cn } from '@/lib/utils';

const navigation = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'Faktúry', href: '/invoices', icon: FileText },
  { name: 'Na schválenie', href: '/invoices?status=pending_approval', icon: Clock },
  { name: 'Schválené', href: '/invoices?status=approved', icon: CheckCircle },
  { name: 'Nastavenia', href: '/settings', icon: Settings },
];

export function Sidebar() {
  return (
    <aside className="w-64 border-r border-slate-200 bg-white">
      <nav className="p-4 space-y-1">
        {navigation.map((item) => (
          <NavLink
            key={item.name}
            to={item.href}
            className={({ isActive }) =>
              cn(
                'flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors',
                isActive
                  ? 'bg-blue-50 text-blue-700'
                  : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
              )
            }
          >
            <item.icon className="h-5 w-5" />
            {item.name}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
