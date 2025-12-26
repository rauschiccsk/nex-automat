import { Outlet } from 'react-router-dom';
import { Header } from './Header';
import { Sidebar } from './Sidebar';

export function Layout() {
  return (
    <div className="h-screen flex flex-col overflow-hidden bg-slate-50">
      <Header />
      <div className="flex flex-1 min-h-0 overflow-hidden">
        <Sidebar />
        <main className="flex-1 p-4 overflow-hidden flex flex-col">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
