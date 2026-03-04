// RunWizard — 4-step migration run wizard
import { useState, type ReactElement } from 'react'
import {
  CheckCircle2,
  XCircle,
  Clock,
  AlertTriangle,
  Loader2,
  ArrowRight,
  ArrowLeft,
  Info
} from 'lucide-react'
import { cn } from '@renderer/lib/utils'
import { api, type ApiError } from '@renderer/lib/api'
import type { MigrationCategory, MigrationRunResponse } from '@renderer/types/migration'

interface RunWizardProps {
  category: MigrationCategory
  onClose: () => void
  onCompleted: () => void
}

type WizardStep = 1 | 2 | 3 | 4

const STEP_LABELS: Record<WizardStep, string> = {
  1: 'Kontrola predpokladov',
  2: 'Informacie',
  3: 'Potvrdenie',
  4: 'Vysledok'
}

export default function RunWizard({ category, onClose, onCompleted }: RunWizardProps): ReactElement {
  const [step, setStep] = useState<WizardStep>(1)
  const [confirmed, setConfirmed] = useState(false)
  const [running, setRunning] = useState(false)
  const [result, setResult] = useState<MigrationRunResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isNotImplemented, setIsNotImplemented] = useState(false)

  const allDepsOk = category.dependencies.every((d) => d.is_satisfied)

  const handleRun = async (): Promise<void> => {
    setRunning(true)
    setError(null)
    setIsNotImplemented(false)
    try {
      const res = await api.runMigration({ category: category.code, dry_run: false })
      setResult(res)
      setStep(4)
    } catch (err) {
      const e = err as ApiError
      if (e.status === 501) {
        setIsNotImplemented(true)
        setError(e.message || e.detail || `Extractor/Loader pre ${category.code} este nie je implementovany.`)
      } else {
        setError(e.message || e.detail || 'Migracia zlyhala')
      }
      setStep(4)
    } finally {
      setRunning(false)
    }
  }

  const renderStepIndicator = (): ReactElement => (
    <div className="flex items-center gap-2 mb-6">
      {([1, 2, 3, 4] as WizardStep[]).map((s) => (
        <div key={s} className="flex items-center gap-2">
          <div
            className={cn(
              'flex items-center justify-center w-8 h-8 rounded-full text-sm font-semibold transition-colors',
              s === step
                ? 'bg-blue-600 text-white'
                : s < step
                  ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
                  : 'bg-gray-100 text-gray-400 dark:bg-gray-700 dark:text-gray-500'
            )}
          >
            {s < step ? <CheckCircle2 className="h-4 w-4" /> : s}
          </div>
          {s < 4 && (
            <div
              className={cn(
                'w-8 h-0.5',
                s < step ? 'bg-green-400 dark:bg-green-600' : 'bg-gray-200 dark:bg-gray-700'
              )}
            />
          )}
        </div>
      ))}
      <span className="ml-3 text-sm text-gray-600 dark:text-gray-400">{STEP_LABELS[step]}</span>
    </div>
  )

  const renderStep1 = (): ReactElement => (
    <div className="space-y-4">
      <h3 className="text-base font-semibold text-gray-900 dark:text-white">
        Kontrola zavislosti pre {category.code}
      </h3>
      {category.dependencies.length === 0 ? (
        <p className="text-sm text-green-600 dark:text-green-400">
          Tato kategoria nema ziadne zavislosti — mozete pokracovat.
        </p>
      ) : (
        <div className="space-y-2">
          {category.dependencies.map((dep) => (
            <div
              key={dep.code}
              className={cn(
                'flex items-center gap-3 p-3 rounded-lg border',
                dep.is_satisfied
                  ? 'border-green-200 dark:border-green-800 bg-green-50 dark:bg-green-900/10'
                  : 'border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-900/10'
              )}
            >
              {dep.is_satisfied ? (
                <CheckCircle2 className="h-5 w-5 text-green-500 shrink-0" />
              ) : dep.status === 'failed' ? (
                <XCircle className="h-5 w-5 text-red-500 shrink-0" />
              ) : (
                <Clock className="h-5 w-5 text-amber-500 shrink-0" />
              )}
              <div>
                <span className="font-mono text-sm font-semibold text-gray-900 dark:text-white">
                  {dep.code}
                </span>
                <span className="ml-2 text-sm text-gray-600 dark:text-gray-400">{dep.name}</span>
              </div>
              <span
                className={cn(
                  'ml-auto text-xs font-medium px-2 py-0.5 rounded-full',
                  dep.status === 'completed'
                    ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
                    : dep.status === 'failed'
                      ? 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
                      : 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-400'
                )}
              >
                {dep.status}
              </span>
            </div>
          ))}
        </div>
      )}
      {!allDepsOk && (
        <div className="flex items-center gap-2 p-3 rounded-lg bg-amber-50 dark:bg-amber-900/10 border border-amber-200 dark:border-amber-800">
          <AlertTriangle className="h-5 w-5 text-amber-500 shrink-0" />
          <span className="text-sm text-amber-700 dark:text-amber-400">
            Nie vsetky zavislosti su splnene. Najprv dokoncite zavisle kategorie.
          </span>
        </div>
      )}
    </div>
  )

  const renderStep2 = (): ReactElement => (
    <div className="space-y-4">
      <h3 className="text-base font-semibold text-gray-900 dark:text-white">
        Informacie o migracii — {category.code}
      </h3>
      <p className="text-sm text-gray-600 dark:text-gray-400">{category.description}</p>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <h4 className="text-xs font-semibold uppercase text-gray-500 dark:text-gray-400 mb-2">
            Zdrojove tabulky (Btrieve)
          </h4>
          <div className="space-y-1">
            {category.source_tables.map((t) => (
              <div key={t} className="flex items-center gap-2 text-sm">
                <span className="font-mono text-xs px-1.5 py-0.5 bg-blue-50 dark:bg-blue-900/20 rounded text-blue-700 dark:text-blue-400">
                  {t}
                </span>
              </div>
            ))}
          </div>
        </div>
        <div>
          <h4 className="text-xs font-semibold uppercase text-gray-500 dark:text-gray-400 mb-2">
            Cielove tabulky (PostgreSQL)
          </h4>
          <div className="space-y-1">
            {category.target_tables.map((t) => (
              <div key={t} className="flex items-center gap-2 text-sm">
                <span className="font-mono text-xs px-1.5 py-0.5 bg-green-50 dark:bg-green-900/20 rounded text-green-700 dark:text-green-400">
                  {t}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
      <div className="p-3 rounded-lg bg-blue-50 dark:bg-blue-900/10 border border-blue-200 dark:border-blue-800">
        <div className="flex items-start gap-2">
          <Info className="h-4 w-4 text-blue-500 mt-0.5 shrink-0" />
          <p className="text-sm text-blue-700 dark:text-blue-400">
            ETL proces extrahuje data zo zdrojovych tabuliek, transformuje ich a ulozi do cielovych
            tabuliek. ID mapovanie sa zaznamenava pre spatnu trasovatelnost.
          </p>
        </div>
      </div>
    </div>
  )

  const renderStep3 = (): ReactElement => (
    <div className="space-y-4">
      <h3 className="text-base font-semibold text-gray-900 dark:text-white">
        Potvrdenie spustenia — {category.code}
      </h3>
      <div className="p-4 rounded-lg bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
        <dl className="space-y-2 text-sm">
          <div className="flex justify-between">
            <dt className="text-gray-500 dark:text-gray-400">Kategoria:</dt>
            <dd className="font-mono font-semibold text-gray-900 dark:text-white">{category.code}</dd>
          </div>
          <div className="flex justify-between">
            <dt className="text-gray-500 dark:text-gray-400">Nazov:</dt>
            <dd className="text-gray-900 dark:text-white">{category.name}</dd>
          </div>
          <div className="flex justify-between">
            <dt className="text-gray-500 dark:text-gray-400">Zdrojove tabulky:</dt>
            <dd className="text-gray-900 dark:text-white">{category.source_tables.join(', ')}</dd>
          </div>
          <div className="flex justify-between">
            <dt className="text-gray-500 dark:text-gray-400">Cielove tabulky:</dt>
            <dd className="text-gray-900 dark:text-white">{category.target_tables.join(', ')}</dd>
          </div>
        </dl>
      </div>
      <label className="flex items-center gap-3 p-3 rounded-lg border border-gray-200 dark:border-gray-700 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
        <input
          type="checkbox"
          checked={confirmed}
          onChange={(e) => setConfirmed(e.target.checked)}
          className="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
        />
        <span className="text-sm text-gray-700 dark:text-gray-300">
          Rozumiem, ze migracia prepise existujuce data
        </span>
      </label>
    </div>
  )

  const renderStep4 = (): ReactElement => (
    <div className="space-y-4">
      <h3 className="text-base font-semibold text-gray-900 dark:text-white">
        Vysledok migracie — {category.code}
      </h3>
      {running && (
        <div className="flex items-center justify-center py-8">
          <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
          <span className="ml-3 text-gray-600 dark:text-gray-400">Prebieha migracia...</span>
        </div>
      )}
      {isNotImplemented && !running && (
        <div className="p-4 rounded-lg bg-blue-50 dark:bg-blue-900/10 border border-blue-200 dark:border-blue-800">
          <div className="flex items-start gap-3">
            <Info className="h-5 w-5 text-blue-500 mt-0.5 shrink-0" />
            <div>
              <p className="font-medium text-blue-700 dark:text-blue-400">Este nie je implementovane</p>
              <p className="text-sm text-blue-600 dark:text-blue-400 mt-1">{error}</p>
            </div>
          </div>
        </div>
      )}
      {error && !isNotImplemented && !running && (
        <div className="p-4 rounded-lg bg-red-50 dark:bg-red-900/10 border border-red-200 dark:border-red-800">
          <div className="flex items-start gap-3">
            <XCircle className="h-5 w-5 text-red-500 mt-0.5 shrink-0" />
            <div>
              <p className="font-medium text-red-700 dark:text-red-400">Migracia zlyhala</p>
              <p className="text-sm text-red-600 dark:text-red-400 mt-1">{error}</p>
            </div>
          </div>
        </div>
      )}
      {result && !running && (
        <div className="p-4 rounded-lg bg-green-50 dark:bg-green-900/10 border border-green-200 dark:border-green-800">
          <div className="flex items-start gap-3">
            <CheckCircle2 className="h-5 w-5 text-green-500 mt-0.5 shrink-0" />
            <div className="flex-1">
              <p className="font-medium text-green-700 dark:text-green-400">
                Migracia dokoncena
              </p>
              <dl className="mt-2 grid grid-cols-3 gap-2 text-sm">
                <div>
                  <dt className="text-gray-500 dark:text-gray-400">Zdrojove</dt>
                  <dd className="font-semibold text-gray-900 dark:text-white">{result.source_count}</dd>
                </div>
                <div>
                  <dt className="text-gray-500 dark:text-gray-400">Cielove</dt>
                  <dd className="font-semibold text-gray-900 dark:text-white">{result.target_count}</dd>
                </div>
                <div>
                  <dt className="text-gray-500 dark:text-gray-400">Chyby</dt>
                  <dd className={cn('font-semibold', result.error_count > 0 ? 'text-red-600' : 'text-gray-900 dark:text-white')}>
                    {result.error_count}
                  </dd>
                </div>
              </dl>
              {result.message && (
                <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">{result.message}</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )

  return (
    <div className="space-y-4">
      {renderStepIndicator()}

      <div className="min-h-[200px]">
        {step === 1 && renderStep1()}
        {step === 2 && renderStep2()}
        {step === 3 && renderStep3()}
        {step === 4 && renderStep4()}
      </div>

      {/* Navigation */}
      <div className="flex items-center justify-between pt-4 border-t border-gray-200 dark:border-gray-700">
        <button
          onClick={step === 1 || step === 4 ? onClose : () => setStep((step - 1) as WizardStep)}
          className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
        >
          {step === 4 ? (
            'Zavriet'
          ) : step === 1 ? (
            'Zrusit'
          ) : (
            <>
              <ArrowLeft className="h-4 w-4" /> Spat
            </>
          )}
        </button>

        {step < 3 && (
          <button
            onClick={() => setStep((step + 1) as WizardStep)}
            disabled={step === 1 && !allDepsOk}
            className={cn(
              'flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors',
              step === 1 && !allDepsOk
                ? 'bg-gray-200 text-gray-400 dark:bg-gray-700 dark:text-gray-500 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            )}
          >
            Dalej <ArrowRight className="h-4 w-4" />
          </button>
        )}

        {step === 3 && (
          <button
            onClick={() => { void handleRun() }}
            disabled={!confirmed || running}
            className={cn(
              'flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors',
              !confirmed || running
                ? 'bg-gray-200 text-gray-400 dark:bg-gray-700 dark:text-gray-500 cursor-not-allowed'
                : 'bg-green-600 text-white hover:bg-green-700'
            )}
          >
            {running ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" /> Spusta sa...
              </>
            ) : (
              'Spustit migraciu'
            )}
          </button>
        )}

        {step === 4 && (result || error) && (
          <button
            onClick={() => {
              onCompleted()
              onClose()
            }}
            className="px-4 py-2 rounded-lg text-sm font-medium bg-blue-600 text-white hover:bg-blue-700 transition-colors"
          >
            Hotovo
          </button>
        )}
      </div>
    </div>
  )
}
