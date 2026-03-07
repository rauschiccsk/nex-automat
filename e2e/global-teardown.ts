import { FullConfig } from '@playwright/test'
import { execSync } from 'child_process'

async function globalTeardown(config: FullConfig) {
  console.log('\n🧹 Global teardown: cleaning up E2E test data...')

  try {
    // Zisti názov postgres kontajnera
    const containerName = execSync(
      "docker ps --format '{{.Names}}' | grep postgres",
      { encoding: 'utf-8', timeout: 5000 }
    ).trim().split('\n')[0]

    if (!containerName) {
      console.warn('⚠️ No postgres container found, skipping cleanup')
      return
    }

    // 1. Hard delete E2E partnerov (CASCADE vymaže child záznamy)
    const deleteResult = execSync(
      `docker exec ${containerName} psql -U nex_admin -d nex_automat -c "DELETE FROM partner_catalog WHERE partner_name LIKE 'E2E_%';"`,
      { encoding: 'utf-8', timeout: 10000 }
    ).trim()
    console.log(`  Partners: ${deleteResult}`)

    // 2. Vyčisti audit_log
    const auditResult = execSync(
      `docker exec ${containerName} psql -U nex_admin -d nex_automat -c "DELETE FROM audit_log WHERE details::text LIKE '%E2E_%';"`,
      { encoding: 'utf-8', timeout: 10000 }
    ).trim()
    console.log(`  Audit log: ${auditResult}`)

    // 3. Obnov prípadne soft-deleted reálnych partnerov (safety net)
    const restoreResult = execSync(
      `docker exec ${containerName} psql -U nex_admin -d nex_automat -c "UPDATE partner_catalog SET is_active = true WHERE is_active = false AND partner_name NOT LIKE 'E2E_%';"`,
      { encoding: 'utf-8', timeout: 10000 }
    ).trim()
    console.log(`  Restored partners: ${restoreResult}`)

    // 4. Over finálny stav
    const countResult = execSync(
      `docker exec ${containerName} psql -U nex_admin -d nex_automat -t -c "SELECT COUNT(*) FROM partner_catalog WHERE is_active = true;"`,
      { encoding: 'utf-8', timeout: 5000 }
    ).trim()
    console.log(`  Active partners after cleanup: ${countResult}`)

    console.log('✅ Global teardown complete')
  } catch (error) {
    // Nefailuj CI ak cleanup nefunguje
    console.warn('⚠️ Global teardown warning:', (error as Error).message)
  }
}

export default globalTeardown
