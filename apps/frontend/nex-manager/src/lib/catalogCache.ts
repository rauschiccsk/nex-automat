/**
 * IndexedDB cache for NEX Manager catalogs (PAB, GSC, …).
 *
 * Genesis Performance Pattern (Phase J): each catalog mirrors its server
 * data into IndexedDB so subsequent opens are instantaneous.
 *
 * Storage shape — SINGLE BLOB per catalog
 * ────────────────────────────────────────
 * Earlier per-record-row layout was killed by 250k structured-clone copies
 * (read 6s, write 70s). Now each catalog is stored as ONE record:
 *
 *   { catalog: 'pab', json: '<serialized array>', etag: '…', count, fetchedAt }
 *
 * Reads = 1 IDB get + 1 JSON.parse.   ~1-2s for 80MB on Chrome.
 * Writes = 1 IDB put + JSON.stringify already done by caller.   <500ms.
 *
 * Layout
 * ──────
 * DB:    `nex-manager-cache`  (version 2 — version 1 used per-row layout)
 * Store: `catalogs`           (keyPath = 'catalog')
 *
 * Versioning
 * ──────────
 * Bumping CACHE_VERSION nukes existing data — schema migration logic
 * lives in `onupgradeneeded`. v1 → v2 simply drops the old per-catalog
 * stores; users will re-sync on next open.
 *
 * Concurrency
 * ───────────
 * One transaction per call (atomic). Reads and writes do not block each
 * other — IDB handles isolation.
 */

const DB_NAME = 'nex-manager-cache'
const STORE = 'catalogs'
const CACHE_VERSION = 2

const CATALOG_CODES = ['pab'] as const
export type CatalogCode = (typeof CATALOG_CODES)[number]

interface CatalogBlobRecord {
  catalog: CatalogCode
  /** Serialized JSON string of the items array. Storing as a string lets the
   * browser skip structured-clone of 250k objects (which is the killer cost
   * of the obvious "store each record as an IDB row" approach). */
  json: string
  etag: string
  count: number
  fetchedAt: number // epoch ms
}

// ───────────────────────────────────────────────────────────────
// DB connection (singleton, lazily opened)
// ───────────────────────────────────────────────────────────────

let dbPromise: Promise<IDBDatabase> | null = null

function openDb(): Promise<IDBDatabase> {
  if (dbPromise) return dbPromise
  dbPromise = new Promise<IDBDatabase>((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, CACHE_VERSION)
    req.onerror = () => reject(req.error)
    req.onsuccess = () => resolve(req.result)
    req.onupgradeneeded = () => {
      const db = req.result
      // Drop legacy v1 per-catalog stores (one store per catalog) if present.
      // v1 → v2 migration: best to nuke + re-sync; old layout is unusable.
      for (const name of Array.from(db.objectStoreNames)) {
        if (name !== STORE) db.deleteObjectStore(name)
      }
      if (!db.objectStoreNames.contains(STORE)) {
        db.createObjectStore(STORE, { keyPath: 'catalog' })
      }
    }
    req.onblocked = () =>
      reject(new Error('IndexedDB open blocked — close other tabs of this app'))
  })
  return dbPromise
}

function reqToPromise<T>(req: IDBRequest<T>): Promise<T> {
  return new Promise<T>((resolve, reject) => {
    req.onsuccess = () => resolve(req.result)
    req.onerror = () => reject(req.error)
  })
}

async function getRecord(
  catalog: CatalogCode
): Promise<CatalogBlobRecord | undefined> {
  const db = await openDb()
  const tx = db.transaction(STORE, 'readonly')
  const store = tx.objectStore(STORE)
  return reqToPromise<CatalogBlobRecord | undefined>(
    store.get(catalog) as IDBRequest<CatalogBlobRecord | undefined>
  )
}

// ───────────────────────────────────────────────────────────────
// Public API
// ───────────────────────────────────────────────────────────────

/**
 * Read all cached items for a catalog. Returns null if no cache yet.
 *
 * Performance — single IDB get + JSON.parse. For 250k records:
 *   - IDB get: <50ms
 *   - JSON.parse(80MB): ~2-3s on Chrome
 * Down from ~6s with the per-row layout.
 */
export async function getCachedItems<T extends { id: number | string }>(
  catalog: CatalogCode
): Promise<T[] | null> {
  const rec = await getRecord(catalog)
  if (!rec) return null
  try {
    const items = JSON.parse(rec.json) as T[]
    return items.length === 0 ? null : items
  } catch {
    // Corrupted cache — treat as miss
    return null
  }
}

/**
 * Replace the cached items for a catalog.
 *
 * Performance — single IDB put. JSON.stringify dominates (~500ms for 80MB).
 * Down from ~70s with the per-row layout (which did 250k IDB add ops).
 */
export async function setCachedItems<T extends { id: number | string }>(
  catalog: CatalogCode,
  items: T[],
  etag: string
): Promise<void> {
  const json = JSON.stringify(items)
  const db = await openDb()
  const tx = db.transaction(STORE, 'readwrite')
  const store = tx.objectStore(STORE)
  store.put({
    catalog,
    json,
    etag,
    count: items.length,
    fetchedAt: Date.now(),
  } satisfies CatalogBlobRecord)
  await new Promise<void>((resolve, reject) => {
    tx.oncomplete = () => resolve()
    tx.onerror = () => reject(tx.error)
    tx.onabort = () => reject(tx.error ?? new Error('Transaction aborted'))
  })
}

export async function getCachedEtag(
  catalog: CatalogCode
): Promise<string | null> {
  const rec = await getRecord(catalog)
  return rec?.etag ?? null
}

export async function getCachedMeta(catalog: CatalogCode): Promise<{
  catalog: CatalogCode
  etag: string
  count: number
  fetchedAt: number
} | null> {
  const rec = await getRecord(catalog)
  if (!rec) return null
  return {
    catalog: rec.catalog,
    etag: rec.etag,
    count: rec.count,
    fetchedAt: rec.fetchedAt,
  }
}

/**
 * After a CRUD op, update the cached array in place — patch in memory,
 * re-serialize, write. Saves a full re-sync round trip from server.
 *
 * Caller is responsible for eventually triggering a full re-sync
 * (typically on next ETag check) so that concurrent edits from other
 * users are picked up.
 */
export async function upsertCachedItem<T extends { id: number | string }>(
  catalog: CatalogCode,
  item: T
): Promise<void> {
  const rec = await getRecord(catalog)
  if (!rec) return // no cache to patch — full sync will fill it later
  let items: T[]
  try {
    items = JSON.parse(rec.json) as T[]
  } catch {
    return
  }
  const idx = items.findIndex((x) => x.id === item.id)
  if (idx >= 0) items[idx] = item
  else items.push(item)
  await setCachedItems(catalog, items, rec.etag)
}

export async function removeCachedItem(
  catalog: CatalogCode,
  id: number | string
): Promise<void> {
  const rec = await getRecord(catalog)
  if (!rec) return
  let items: Array<{ id: number | string }>
  try {
    items = JSON.parse(rec.json)
  } catch {
    return
  }
  const filtered = items.filter((x) => x.id !== id)
  if (filtered.length === items.length) return // not found
  await setCachedItems(catalog, filtered, rec.etag)
}

export async function clearCache(catalog: CatalogCode): Promise<void> {
  const db = await openDb()
  const tx = db.transaction(STORE, 'readwrite')
  tx.objectStore(STORE).delete(catalog)
  await new Promise<void>((resolve, reject) => {
    tx.oncomplete = () => resolve()
    tx.onerror = () => reject(tx.error)
  })
}

export async function clearAllCaches(): Promise<void> {
  await Promise.all(CATALOG_CODES.map((c) => clearCache(c)))
}
