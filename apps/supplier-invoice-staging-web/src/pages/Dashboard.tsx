import { useQuery } from '@tanstack/react-query';
import { FileText, Clock, CheckCircle, TrendingUp } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { getStats } from '@/api/invoices';

export function Dashboard() {
  const { data: stats, isLoading } = useQuery({
    queryKey: ['stats'],
    queryFn: getStats,
    refetchInterval: 30000, // Refresh every 30s
  });

  const cards = [
    {
      title: 'Celkom faktúr',
      value: stats?.total_invoices ?? 0,
      icon: FileText,
      color: 'text-blue-600',
      bg: 'bg-blue-50',
    },
    {
      title: 'Čaká na schválenie',
      value: stats?.by_status?.pending_approval ?? 0,
      icon: Clock,
      color: 'text-yellow-600',
      bg: 'bg-yellow-50',
    },
    {
      title: 'Schválené',
      value: stats?.by_status?.approved ?? 0,
      icon: CheckCircle,
      color: 'text-green-600',
      bg: 'bg-green-50',
    },
    {
      title: 'Spracované',
      value: stats?.by_status?.processed ?? 0,
      icon: TrendingUp,
      color: 'text-purple-600',
      bg: 'bg-purple-50',
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Dashboard</h1>
        <p className="text-slate-500">Prehľad dodávateľských faktúr</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {cards.map((card) => (
          <Card key={card.title}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-slate-600">
                {card.title}
              </CardTitle>
              <div className={`p-2 rounded-lg ${card.bg}`}>
                <card.icon className={`h-4 w-4 ${card.color}`} />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {isLoading ? '...' : card.value}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Status breakdown */}
      {stats?.by_status && (
        <Card>
          <CardHeader>
            <CardTitle>Faktúry podľa stavu</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {Object.entries(stats.by_status).map(([status, count]) => (
                <div key={status} className="text-center p-3 bg-slate-50 rounded-lg">
                  <div className="text-lg font-semibold">{count}</div>
                  <div className="text-sm text-slate-500">{status}</div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
