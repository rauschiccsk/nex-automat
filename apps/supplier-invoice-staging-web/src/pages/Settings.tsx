import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { getHealth, getStatus } from '@/api/invoices';

export function Settings() {
  const { data: health } = useQuery({
    queryKey: ['health'],
    queryFn: getHealth,
    refetchInterval: 10000,
  });

  const { data: status } = useQuery({
    queryKey: ['status'],
    queryFn: getStatus,
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Nastavenia</h1>
        <p className="text-slate-500">Konfigurácia a stav systému</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Health Status */}
        <Card>
          <CardHeader>
            <CardTitle>Stav služby</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-slate-600">API Status</span>
              <Badge className={health?.status === 'healthy' ? 'bg-green-500' : 'bg-red-500'}>
                {health?.status ?? 'Unknown'}
              </Badge>
            </div>
            {health?.timestamp && (
              <div className="flex items-center justify-between">
                <span className="text-slate-600">Posledná kontrola</span>
                <span className="text-sm text-slate-500">
                  {new Date(health.timestamp).toLocaleString('sk-SK')}
                </span>
              </div>
            )}
          </CardContent>
        </Card>

        {/* System Info */}
        <Card>
          <CardHeader>
            <CardTitle>Systémové informácie</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {status?.uptime_seconds && (
              <div className="flex items-center justify-between">
                <span className="text-slate-600">Uptime</span>
                <span className="text-sm">
                  {Math.floor(status.uptime_seconds / 3600)}h {Math.floor((status.uptime_seconds % 3600) / 60)}m
                </span>
              </div>
            )}
            {(status as any)?.components && Object.entries((status as any).components).map(([key, value]) => (
              <div key={key} className="flex items-center justify-between">
                <span className="text-slate-600 capitalize">{key}</span>
                <Badge className={value === 'healthy' ? 'bg-green-500' : 'bg-yellow-500'}>
                  {String(value)}
                </Badge>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
