import { useState, useEffect } from 'react';
import { Settings2, GripVertical, Eye, EyeOff, ChevronUp, ChevronDown, RotateCcw } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { cn } from '@/lib/utils';

export interface ColumnConfigItem {
  id: string;
  originalHeader: string;
  customHeader?: string;
  visible: boolean;
  order: number;
}

interface ColumnConfigProps {
  columns: { id: string; header: string }[];
  config: ColumnConfigItem[];
  onChange: (config: ColumnConfigItem[]) => void;
  storageKey?: string;
}

export function ColumnConfig({ columns, config, onChange, storageKey }: ColumnConfigProps) {
  const [open, setOpen] = useState(false);
  const [localConfig, setLocalConfig] = useState<ColumnConfigItem[]>(config);

  useEffect(() => {
    setLocalConfig(config);
  }, [config]);

  const handleVisibilityToggle = (id: string) => {
    setLocalConfig(prev => 
      prev.map(col => 
        col.id === id ? { ...col, visible: !col.visible } : col
      )
    );
  };

  const handleHeaderChange = (id: string, customHeader: string) => {
    setLocalConfig(prev =>
      prev.map(col =>
        col.id === id ? { ...col, customHeader: customHeader || undefined } : col
      )
    );
  };

  const handleMoveUp = (index: number) => {
    if (index === 0) return;
    setLocalConfig(prev => {
      const newConfig = [...prev];
      const temp = newConfig[index].order;
      newConfig[index].order = newConfig[index - 1].order;
      newConfig[index - 1].order = temp;
      return newConfig.sort((a, b) => a.order - b.order);
    });
  };

  const handleMoveDown = (index: number) => {
    if (index === localConfig.length - 1) return;
    setLocalConfig(prev => {
      const newConfig = [...prev];
      const temp = newConfig[index].order;
      newConfig[index].order = newConfig[index + 1].order;
      newConfig[index + 1].order = temp;
      return newConfig.sort((a, b) => a.order - b.order);
    });
  };

  const handleReset = () => {
    const defaultConfig = columns.map((col, index) => ({
      id: col.id,
      originalHeader: col.header,
      customHeader: undefined,
      visible: true,
      order: index,
    }));
    setLocalConfig(defaultConfig);
  };

  const handleSave = () => {
    onChange(localConfig);
    if (storageKey) {
      localStorage.setItem(storageKey, JSON.stringify(localConfig));
    }
    setOpen(false);
  };

  const handleCancel = () => {
    setLocalConfig(config);
    setOpen(false);
  };

  const sortedConfig = [...localConfig].sort((a, b) => a.order - b.order);

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="ghost" size="icon" title="Nastavenie stĺpcov">
          <Settings2 className="h-4 w-4" />
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle>Nastavenie stĺpcov</DialogTitle>
        </DialogHeader>

        <div className="space-y-2 max-h-96 overflow-y-auto">
          {sortedConfig.map((col, index) => (
            <div
              key={col.id}
              className={cn(
                "flex items-center gap-2 p-2 rounded border",
                col.visible ? "bg-white" : "bg-slate-50 opacity-60"
              )}
            >
              {/* Drag handle / Order */}
              <div className="flex flex-col">
                <button
                  onClick={() => handleMoveUp(index)}
                  disabled={index === 0}
                  className="text-slate-400 hover:text-slate-600 disabled:opacity-30"
                >
                  <ChevronUp className="h-3 w-3" />
                </button>
                <button
                  onClick={() => handleMoveDown(index)}
                  disabled={index === sortedConfig.length - 1}
                  className="text-slate-400 hover:text-slate-600 disabled:opacity-30"
                >
                  <ChevronDown className="h-3 w-3" />
                </button>
              </div>

              {/* Visibility toggle */}
              <button
                onClick={() => handleVisibilityToggle(col.id)}
                className={cn(
                  "p-1 rounded",
                  col.visible ? "text-green-600" : "text-slate-400"
                )}
              >
                {col.visible ? <Eye className="h-4 w-4" /> : <EyeOff className="h-4 w-4" />}
              </button>

              {/* Column name input */}
              <div className="flex-1">
                <Input
                  value={col.customHeader ?? col.originalHeader}
                  onChange={(e) => handleHeaderChange(col.id, e.target.value)}
                  placeholder={col.originalHeader}
                  className="h-8 text-sm"
                />
                {col.customHeader && (
                  <div className="text-xs text-slate-400 mt-0.5">
                    Pôvodný: {col.originalHeader}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        <div className="flex justify-between pt-4 border-t">
          <Button variant="ghost" onClick={handleReset}>
            <RotateCcw className="h-4 w-4 mr-2" />
            Obnoviť pôvodné
          </Button>
          <div className="flex gap-2">
            <Button variant="outline" onClick={handleCancel}>
              Zrušiť
            </Button>
            <Button onClick={handleSave}>
              Uložiť
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}

// Hook for managing column configuration
export function useColumnConfig(
  columns: { id: string; header: string }[],
  storageKey?: string
) {
  const [config, setConfig] = useState<ColumnConfigItem[]>(() => {
    // Try to load from localStorage
    if (storageKey) {
      const saved = localStorage.getItem(storageKey);
      if (saved) {
        try {
          return JSON.parse(saved);
        } catch (e) {
          console.error('Failed to parse column config:', e);
        }
      }
    }
    // Default config
    return columns.map((col, index) => ({
      id: col.id,
      originalHeader: col.header,
      customHeader: undefined,
      visible: true,
      order: index,
    }));
  });

  // Update config when columns change (keep user settings)
  useEffect(() => {
    setConfig(prev => {
      const newConfig = columns.map((col, index) => {
        const existing = prev.find(p => p.id === col.id);
        if (existing) {
          return { ...existing, originalHeader: col.header };
        }
        return {
          id: col.id,
          originalHeader: col.header,
          customHeader: undefined,
          visible: true,
          order: prev.length + index,
        };
      });
      return newConfig.sort((a, b) => a.order - b.order);
    });
  }, [columns]);

  return { config, setConfig };
}
