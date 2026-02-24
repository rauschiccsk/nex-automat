# NEX-AUTOMAT PROJECT STRUCTURE

Generated from: `scripts/scan_project_structure.py`

## apps/

### nex-brain/

```
├── api/
│   ├── routes/
│   │   ├── __init__.py (27)
│   │   └── chat.py (3,653)
│   ├── services/
│   │   ├── __init__.py (25)
│   │   ├── llm_service.py (2,989)
│   │   └── rag_service.py (6,122)
│   ├── __init__.py (30)
│   └── main.py (775)
├── cli/
│   ├── __init__.py (20)
│   └── chat_cli.py (3,912)
├── config/
│   ├── __init__.py (23)
│   └── settings.py (1,571)
├── telegram/
│   ├── .env (558)
│   ├── __init__.py (30)
│   ├── config.py (1,928)
│   ├── create_table.sql (695)
│   ├── create_users_table.sql (1,261)
│   ├── db.py (2,487)
│   ├── multi_bot.py (18.6K)
│   ├── requirements.txt (121)
│   └── user_manager.py (9,644)
├── tests/
│   └── __init__.py (22)
├── .env (518)
├── .gitignore (27)
├── README.md (2,623)
└── requirements.txt (141)
```

### supplier-invoice-editor/

```
├── config/
│   └── config.yaml (502)
├── database/
│   ├── migrations/
│   └── README.md-old (47)
├── docs/
│   ├── architecture/
│   ├── database/
│   │   └── TYPE_MAPPINGS.md-old (6,336)
│   ├── screenshots/
│   ├── sessions/
│   ├── INIT_PROMPT_NEW_CHAT.md (19.2K)
│   ├── POSTGRESQL_SETUP.md-old (8,743)
│   ├── project_file_access.json (21.1K)
│   ├── README.md-old (44)
│   └── SESSION_NOTES.md (19.2K)
├── logs/
│   ├── supplier_invoice_editor_20251202.log (3,545)
│   ├── supplier_invoice_editor_20251205.log (733.8K)
│   └── supplier_invoice_editor_20251206.log (277.4K)
├── resources/
│   ├── icons/
│   ├── images/
│   ├── ui/
│   └── README.md-old (64)
├── scripts/
│   ├── apply_xml_import_changes.py (19.0K)
│   ├── check_database_tables.py (1,296)
│   ├── debug_gscat_barcode.py (5,733)
│   ├── debug_import_config.py (2,128)
│   ├── generate_project_access.py (11.9K)
│   ├── import_xml_to_staging.py (9,089)
│   ├── insert_test_data.py (7,574)
│   ├── load_invoice_xml.py (9,345)
│   ├── patch_postgres_client.py (2,973)
│   ├── replace_import_xml.py (8,412)
│   ├── show_table_structure.py (1,566)
│   ├── test_barcode_lookup.py (14.7K)
│   ├── test_pg8000_direct.py (1,540)
│   └── verify_database.py (4,261)
├── src/
│   ├── btrieve/
│   │   ├── __init__.py (262)
│   │   └── btrieve_client.py (7,301)
│   ├── business/
│   │   ├── __init__.py (148)
│   │   ├── invoice_service.py (12.1K)
│   │   └── nex_lookup_service.py (6,075)
│   ├── database/
│   │   ├── __init__.py (142)
│   │   ├── postgres_client.py (6,554)
│   │   └── postgres_client_pg8000.py (6,007)
│   ├── models/
│   │   ├── __init__.py (364)
│   │   ├── barcode.py (7,180)
│   │   ├── gscat.py (11.4K)
│   │   ├── mglst.py (8,291)
│   │   └── pab.py (9,589)
│   ├── ui/
│   │   ├── dialogs/
│   │   │   └── __init__.py (97)
│   │   ├── widgets/
│   │   │   ├── __init__.py (445)
│   │   │   ├── invoice_items_grid.py (10.7K)
│   │   │   ├── invoice_list_widget.py (7,491)
│   │   │   └── quick_search.py (15.2K)
│   │   ├── __init__.py (109)
│   │   ├── invoice_detail_window.py (7,765)
│   │   └── main_window.py (8,819)
│   ├── utils/
│   │   ├── __init__.py (959)
│   │   ├── config.py (2,991)
│   │   ├── constants.py (765)
│   │   ├── grid_settings.py (7,950)
│   │   ├── text_utils.py (2,665)
│   │   └── window_settings.py (3,028)
│   ├── __init__.py (513)
│   ├── config.py (1,507)
│   └── README.md-old (30)
├── tests/
│   ├── fixtures/
│   ├── integration/
│   │   └── __init__.py (30)
│   ├── unit/
│   │   └── __init__.py (30)
│   ├── __init__.py (30)
│   ├── conftest.py (567)
│   ├── README.md-old (23)
│   ├── test_config.py (962)
│   ├── test_database.py (1,081)
│   ├── test_imports.py (1,359)
│   └── test_main.py (1,346)
├── .gitignore (443)
├── cleanup_backups.py (1,685)
├── cleanup_project.py (3,966)
├── main.py (559)
├── pyproject.toml (973)
├── README.md-old (930)
└── requirements.txt (1,443)
```

### supplier-invoice-loader/

```
├── backups/
│   ├── config/
│   │   └── config_backup_20251120_151508/
│   ├── daily/
│   ├── weekly/
│   └── backup.log (25.3K)
├── config/
│   ├── .env.example (5,920)
│   ├── config.template.yaml (579)
│   ├── config.yaml (1,669)
│   ├── config.yaml.template (2,018)
│   ├── config_customer.py (3,933)
│   ├── config_customer.py.template (1,929)
│   ├── config_template.py (14.7K)
│   └── invoices.db (44.0K)
├── database/
│   ├── migrations/
│   │   └── 003_add_file_tracking_columns.sql (2,020)
│   └── schemas/
│       ├── 001_initial_schema.sql (20.1K)
│       ├── 002_add_nex_columns.sql (985)
│       ├── README.md (703)
│       ├── README.md-old (473)
│       └── test_schema.sql (11.3K)
├── deploy/
│   ├── build_package.py (18.3K)
│   ├── deploy.bat (6,134)
│   ├── deploy.sh (15.3K)
│   ├── README.md-old (57)
│   ├── run_smoke_tests.bat (6,592)
│   ├── service_uninstaller.bat (2,261)
│   ├── test-deployment.ps1 (10.5K)
│   └── upgrade_dependencies.bat (2,040)
├── docs/
│   ├── architecture/
│   │   └── README.md-old (398)
│   ├── database/
│   │   └── TYPE_MAPPINGS.md-old (3,041)
│   ├── decisions/
│   │   └── README.md-old (97)
│   ├── deployment/
│   ├── guides/
│   │   ├── CUSTOMER_TESTING_CHECKLIST.md-old (10.6K)
│   │   ├── DEVELOPMENT.md-old (13.3K)
│   │   ├── PYTHON_SETUP.md-old (15.7K)
│   │   ├── SECURITY.md-old (14.1K)
│   │   └── TESTING.md-old (12.3K)
│   ├── operations/
│   │   ├── EMAIL_ALERTING.md-old (12.9K)
│   │   └── MONITORING.md-old (16.5K)
│   ├── sessions/
│   │   └── README.md-old (53)
│   ├── stories/
│   │   └── README.md-old (67)
│   ├── troubleshooting/
│   │   └── README.md-old (57)
│   ├── INIT_PROMPT_NEW_CHAT.md (15.3K)
│   ├── project_file_access.json (46.9K)
│   └── SESSION_NOTES.md (15.2K)
├── logs/
│   ├── backup_daily_20251124.log (3,677)
│   ├── backup_daily_20251125.log (3,677)
│   ├── backup_daily_20251126.log (3,677)
│   ├── backup_daily_20251127.log (3,677)
│   ├── backup_daily_20251128.log (3,677)
│   ├── backup_daily_20251129.log (3,677)
│   ├── backup_daily_20251130.log (3,677)
│   ├── backup_daily_20251201.log (3,677)
│   ├── backup_daily_20251202.log (3,677)
│   ├── backup_daily_20251203.log (3,677)
│   ├── backup_daily_20251204.log (3,677)
│   ├── backup_daily_20251205.log (3,677)
│   ├── backup_daily_20251206.log (3,677)
│   ├── backup_daily_20251208.log (3,677)
│   ├── backup_daily_20251209.log (3,677)
│   ├── backup_daily_20251210.log (3,677)
│   ├── backup_daily_20251211.log (3,677)
│   ├── backup_daily_20251212.log (3,677)
│   ├── backup_daily_20251213.log (3,677)
│   ├── backup_daily_20251214.log (3,677)
│   ├── backup_daily_20251215.log (3,677)
│   ├── backup_daily_20251216.log (3,677)
│   ├── backup_daily_20251217.log (3,677)
│   ├── backup_daily_20251218.log (3,677)
│   ├── backup_daily_20251219.log (3,677)
│   ├── backup_daily_20251220.log (3,677)
│   ├── backup_daily_20251222.log (3,677)
│   ├── backup_daily_20251223.log (3,677)
│   ├── backup_daily_20251224.log (3,677)
│   ├── backup_daily_20251225.log (3,677)
│   ├── backup_daily_20251226.log (3,677)
│   ├── backup_daily_20251227.log (3,677)
│   ├── backup_daily_20251228.log (3,677)
│   ├── backup_weekly_20251124.log (3,682)
│   ├── backup_weekly_20251130.log (3,682)
│   ├── backup_weekly_20251208.log (3,682)
│   ├── backup_weekly_20251214.log (3,682)
│   ├── backup_weekly_20251222.log (3,682)
│   └── backup_weekly_20251228.log (3,682)
├── n8n-workflows/
│   ├── n8n-SupplierInvoiceEmailLoader.json (7,597)
│   ├── README.md-old (67)
│   └── template.json (7,600)
├── reports/
│   ├── templates/
│   │   └── daily_report.html (4,216)
│   ├── __init__.py (111)
│   ├── config.py (1,988)
│   └── daily_summary.py (10.1K)
├── scripts/
│   ├── backup_config.py (728)
│   ├── backup_database.py (2,644)
│   ├── backup_wrapper.py (4,798)
│   ├── clear_test_data.py (2,355)
│   ├── generate_project_access.py (8,663)
│   ├── manual_test_batch_extraction.py (2,835)
│   ├── manual_test_extraction.py (2,133)
│   ├── manual_test_isdoc.py (1,452)
│   ├── restore_database.py (4,609)
│   ├── run_daily_report.py (2,159)
│   ├── SCHEDULER_README.md-old (2,788)
│   ├── service_installer.py (24.5K)
│   ├── setup_task_scheduler.ps1 (4,856)
│   ├── test_invoice_integration.py (10.6K)
│   └── verify_installation.py (6,523)
├── src/
│   ├── api/
│   │   ├── __init__.py (25)
│   │   ├── models.py (1,583)
│   │   └── staging_routes.py (9,058)
│   ├── backup/
│   │   ├── __init__.py (61)
│   │   ├── config_backup.py (1,112)
│   │   ├── database_backup.py (10.1K)
│   │   └── database_restore.py (11.5K)
│   ├── business/
│   │   ├── __init__.py (27)
│   │   ├── isdoc_service.py (15.0K)
│   │   └── product_matcher.py (8,565)
│   ├── database/
│   │   ├── __init__.py (23)
│   │   └── database.py (14.2K)
│   ├── extractors/
│   │   ├── __init__.py (26)
│   │   ├── base_extractor.py (1,201)
│   │   ├── generic_extractor.py (1,404)
│   │   └── ls_extractor.py (12.3K)
│   ├── monitoring/
│   │   ├── __init__.py (470)
│   │   ├── alert_manager.py (17.2K)
│   │   ├── health_monitor.py (11.0K)
│   │   └── log_manager.py (10.3K)
│   ├── utils/
│   │   ├── __init__.py (21)
│   │   ├── config.py (725)
│   │   ├── env_loader.py (2,621)
│   │   ├── monitoring.py (4,188)
│   │   └── notifications.py (20.8K)
│   └── __init__.py (18)
├── tests/
│   ├── integration/
│   │   └── __init__.py (18)
│   ├── samples/
│   │   ├── .gitkeep (0)
│   │   ├── 20250929_232558_32510374_FAK.pdf (451.4K)
│   │   ├── 20250930_214734_32510048_FAK.pdf (453.5K)
│   │   ├── 20250930_214944_32509931_FAK.pdf (460.1K)
│   │   ├── 20250930_220008_32509435_FAK.pdf (455.1K)
│   │   ├── 20251001_111835_32508001_FAK.pdf (449.7K)
│   │   ├── 20251001_114545_32509698_FAK.pdf (454.2K)
│   │   ├── 20251001_114843_32509318_FAK.pdf (454.9K)
│   │   ├── 20251001_114946_32508940_FAK.pdf (448.4K)
│   │   ├── 20251001_114952_32508635_FAK.pdf (452.8K)
│   │   ├── 20251001_115733_32508430_FAK.pdf (451.1K)
│   │   ├── 20251001_120535_32510620_FAK.pdf (452.6K)
│   │   ├── 20251001_181305_32507663_FAK.pdf (456.3K)
│   │   ├── 20251001_183614_32507429_FAK.pdf (455.7K)
│   │   ├── 20251118_103422_32506183_FAK.pdf (455.9K)
│   │   ├── 20251118_103513_32506183_FAK.pdf (455.9K)
│   │   ├── 20251118_103754_32506183_FAK.pdf (455.9K)
│   │   ├── 20251118_103935_32506183_FAK.pdf (455.9K)
│   │   ├── 20251118_105818_32506183_FAK.pdf (455.9K)
│   │   └── README.md-old (3,789)
│   ├── unit/
│   │   ├── __init__.py (18)
│   │   ├── test_alert_manager.py (5,107)
│   │   ├── test_api.py (7,060)
│   │   ├── test_backup_database.py (12.1K)
│   │   ├── test_config.py (6,827)
│   │   ├── test_health_monitor.py (2,695)
│   │   ├── test_import.py (523)
│   │   ├── test_log_manager.py (5,925)
│   │   ├── test_monitoring.py (10.4K)
│   │   └── test_notifications.py (9,156)
│   ├── __init__.py (18)
│   ├── conftest.py (5,775)
│   └── README.md-old (241)
├── .gitignore (855)
├── main.py (25.4K)
├── main.py.bak (23.9K)
├── pyproject.toml (1,159)
├── README.md-old (1,130)
├── requirements-dev.txt (1,661)
├── requirements.txt (3,131)
└── test_report.html (5,066)
```

### supplier-invoice-staging/

```
├── config/
│   ├── __init__.py (16)
│   ├── config.yaml (165)
│   └── settings.py (1,824)
├── data/
│   └── settings.db (24.0K)
├── database/
│   ├── repositories/
│   │   ├── __init__.py (115)
│   │   └── invoice_repository.py (5,191)
│   ├── schemas/
│   │   └── 001_supplier_invoice_staging.sql (7,173)
│   └── __init__.py (16)
├── models/
│   └── __init__.py (16)
├── resources/
│   └── icons/
├── services/
│   ├── __init__.py (63)
│   └── file_mover.py (4,685)
├── tests/
│   └── __init__.py (16)
├── ui/
│   ├── dialogs/
│   │   └── __init__.py (16)
│   ├── __init__.py (164)
│   ├── invoice_items_window.py (10.1K)
│   ├── invoice_items_window.py.bak (10.1K)
│   ├── main_window.py (9,108)
│   └── main_window.py.bak (8,709)
├── __init__.py (16)
├── __main__.py (279)
├── app.py (781)
└── requirements.txt (70)
```

### supplier-invoice-staging-web/

```
├── public/
│   └── vite.svg (1,497)
├── src/
│   ├── api/
│   │   ├── client.ts (764)
│   │   ├── index.ts (56)
│   │   ├── invoices.ts (3,281)
│   │   └── mockData.ts (8,596)
│   ├── assets/
│   │   └── react.svg (4,126)
│   ├── components/
│   │   ├── grids/
│   │   │   ├── configs/
│   │   │   │   ... (max depth reached)
│   │   │   ├── BaseGrid.tsx (6,334)
│   │   │   ├── gridFilters.ts (4,396)
│   │   │   ├── gridFormatters.ts (2,309)
│   │   │   ├── gridTypes.ts (1,628)
│   │   │   └── index.ts (256)
│   │   ├── layout/
│   │   │   ├── Header.tsx (893)
│   │   │   ├── index.ts (110)
│   │   │   ├── Layout.tsx (477)
│   │   │   └── Sidebar.tsx (1,333)
│   │   └── ui/
│   │       ├── badge.tsx (1,633)
│   │       ├── button.tsx (2,218)
│   │       ├── card.tsx (1,987)
│   │       ├── column-config.tsx (7,347)
│   │       ├── datagrid.tsx (29.0K)
│   │       ├── datagrid.tsx.bak (31.2K)
│   │       ├── dialog.tsx (3,981)
│   │       ├── input.tsx (1,014)
│   │       ├── select.tsx (6,358)
│   │       ├── sonner.tsx (1,034)
│   │       └── table.tsx (2,434)
│   ├── lib/
│   │   └── utils.ts (166)
│   ├── pages/
│   │   ├── Dashboard.tsx (2,922)
│   │   ├── InvoiceDetail.tsx (9,722)
│   │   ├── InvoiceDetail.tsx.bak (12.2K)
│   │   ├── InvoiceDetail.tsx.bak2 (14.9K)
│   │   ├── Invoices.tsx (2,322)
│   │   ├── Invoices.tsx.bak (5,217)
│   │   └── Settings.tsx (2,822)
│   ├── types/
│   │   ├── invoice.ts (5,480)
│   │   └── invoice.ts.bak (5,342)
│   ├── App.css (606)
│   ├── App.tsx (1,154)
│   ├── index.css (5,172)
│   └── main.tsx (230)
├── .gitignore (253)
├── components.json (444)
├── dist.zip (168.3K)
├── eslint.config.js (616)
├── index.html (377)
├── package-lock.json (175.1K)
├── package.json (1,310)
├── README.md (2,555)
├── tsconfig.app.json (744)
├── tsconfig.json (266)
├── tsconfig.node.json (653)
└── vite.config.ts (567)
```

### supplier-invoice-worker/

```
├── activities/
│   ├── __init__.py (0)
│   ├── email_activities.py (4,450)
│   ├── invoice_activities.py (2,972)
│   └── invoice_activities.py.bak (2,642)
├── config/
│   ├── __init__.py (0)
│   ├── gmail_oauth.py (3,332)
│   ├── oauth_authorize.py (649)
│   └── settings.py (1,434)
├── scheduler/
│   ├── __init__.py (0)
│   └── polling_scheduler.py (2,703)
├── tests/
│   └── __init__.py (0)
├── workers/
│   ├── __init__.py (0)
│   └── main_worker.py (1,731)
├── workflows/
│   ├── __init__.py (0)
│   └── invoice_workflow.py (3,822)
├── .env (744)
├── .env.example (605)
├── .gitignore (158)
├── .gmail_tokens.json (695)
├── __init__.py (0)
└── requirements.txt (401)
```

## packages/

### nex-shared/

```
├── database/
│   ├── __init__.py (121)
│   ├── postgres_staging.py.removed (13.5K)
│   └── window_settings_db.py (5,751)
├── nex_shared.egg-info/
│   ├── dependency_links.txt (1)
│   ├── PKG-INFO (856)
│   ├── requires.txt (52)
│   ├── SOURCES.txt (677)
│   └── top_level.txt (11)
├── ui/
│   ├── __init__.py (242)
│   ├── base_grid.py (11.9K)
│   ├── base_window.py (6,993)
│   └── window_persistence.py (6,459)
├── utils/
│   ├── __init__.py (514)
│   ├── grid_settings.py (8,030)
│   ├── monitor_utils.py (0)
│   └── text_utils.py (790)
├── __init__.py (278)
└── setup.py (1,384)
```

### nex-staging/

```
├── nex_staging/
│   ├── models/
│   │   ├── __init__.py (230)
│   │   ├── invoice_head.py (2,380)
│   │   └── invoice_item.py (1,442)
│   ├── repositories/
│   │   ├── __init__.py (159)
│   │   └── invoice_repository.py (8,089)
│   ├── __init__.py (350)
│   ├── connection.py (5,502)
│   └── staging_client.py (10.4K)
├── pyproject.toml (369)
└── README.md (719)
```

### nexdata/

```
├── nexdata/
│   ├── auth/
│   │   └── __init__.py (29)
│   ├── btrieve/
│   │   ├── __init__.py (14)
│   │   └── btrieve_client.py (14.4K)
│   ├── database/
│   │   └── __init__.py (29)
│   ├── models/
│   │   ├── __init__.py (14)
│   │   ├── barcode.py (6,967)
│   │   ├── gscat.py (3,196)
│   │   ├── mglst.py (8,055)
│   │   ├── pab.py (9,334)
│   │   ├── tsh.py (10.1K)
│   │   └── tsi.py (9,558)
│   ├── monitoring/
│   │   └── __init__.py (29)
│   ├── repositories/
│   │   ├── __init__.py (518)
│   │   ├── barcode_repository.py (2,441)
│   │   ├── base_repository.py (6,695)
│   │   ├── gscat_repository.py (2,281)
│   │   ├── mglst_repository.py (1,613)
│   │   ├── pab_repository.py (1,868)
│   │   ├── tsh_repository.py (1,987)
│   │   └── tsi_repository.py (2,046)
│   ├── utils/
│   │   └── __init__.py (14)
│   └── __init__.py (945)
├── pyproject.toml (322)
└── README.md-old (983)
```

### shared-pyside6/

```
├── shared_pyside6/
│   ├── database/
│   │   ├── __init__.py (237)
│   │   └── settings_repository.py (9,468)
│   ├── ui/
│   │   ├── __init__.py (809)
│   │   ├── base_grid.py (27.0K)
│   │   ├── base_window.py (5,480)
│   │   └── quick_search.py (11.4K)
│   ├── utils/
│   │   ├── __init__.py (304)
│   │   └── text_utils.py (1,743)
│   └── __init__.py (282)
├── shared_pyside6.egg-info/
│   ├── dependency_links.txt (1)
│   ├── PKG-INFO (1,309)
│   ├── requires.txt (85)
│   ├── SOURCES.txt (506)
│   └── top_level.txt (15)
├── tests/
│   ├── __init__.py (41)
│   ├── test_base_grid.py (6,460)
│   ├── test_base_window.py (4,308)
│   ├── test_imports.py (535)
│   └── test_quick_search.py (5,033)
├── pyproject.toml (636)
└── README.md (853)
```

## docs/knowledge/

```
├── credentials/
│   └── CREDENTIALS.md (3,031)
├── decisions/
│   └── .gitkeep (0)
├── deployment/
│   ├── magerstav/
│   │   └── TEMPORAL_DEPLOYMENT_MAGERSTAV.md (9,353)
│   ├── .gitkeep (0)
│   ├── DEPLOYMENT_GUIDE_ANDROS.md (17.2K)
│   └── DEPLOYMENT_GUIDE_V3.md (9,857)
├── development/
│   ├── .gitkeep (0)
│   ├── 2025-12-19_nex-brain-api.md (2,276)
│   ├── 2025-12-19_nex-brain-foundation.md (3,108)
│   ├── 2025-12-24_nex-brain-telegram.md (4,759)
│   └── INIT_PROMPT_SUPPLIER_INVOICE_STAGING_WEB.md (10.1K)
├── scripts/
│   └── .gitkeep (0)
├── sessions/
│   ├── KNOWLEDGE_2025-12-19_nex-brain-tenant-filtering.md (1,465)
│   ├── KNOWLEDGE_2025-12-20_temporal-migration-implementation.md (9,845)
│   ├── KNOWLEDGE_2025-12-20_temporal-phase5-deployment.md (303)
│   ├── KNOWLEDGE_2025-12-20_temporal_migration_implementation.md (1,543)
│   ├── KNOWLEDGE_2025-12-21_temporal-phase5-deployment-complete.md (3,390)
│   ├── KNOWLEDGE_2025-12-21_temporal-phase5-deployment-continued.md (3,456)
│   ├── KNOWLEDGE_2025-12-22_file-organization-phase-d-documentation.md (1,477)
│   ├── KNOWLEDGE_2025-12-22_nex-staging-package-migration.md (2,171)
│   ├── KNOWLEDGE_2025-12-22_project-structure.md (15.1K)
│   ├── KNOWLEDGE_2025-12-22_temporal-phase6-validation-file-organization.md (2,199)
│   ├── KNOWLEDGE_2025-12-23_nex-automat-v3-deployment.md (5,097)
│   ├── KNOWLEDGE_2025-12-23_nex-staging-pg8000-deployment.md (2,546)
│   ├── KNOWLEDGE_2025-12-24_daily-reports-smtp-security.md (2,765)
│   ├── KNOWLEDGE_2025-12-24_nex-brain-telegram-multibot.md (3,542)
│   ├── KNOWLEDGE_2025-12-24_v31-deployment-daily-reports.md (1,287)
│   ├── KNOWLEDGE_2025-12-25_cleanup-services-magerstav.md (1,395)
│   ├── KNOWLEDGE_2025-12-25_rag-cleanup-telegram-tokens.md (1,968)
│   ├── KNOWLEDGE_2025-12-25_todo-master-review.md (1,392)
│   ├── KNOWLEDGE_2025-12-26_staging-web-v32-deployment.md (2,262)
│   ├── KNOWLEDGE_2025-12-26_supplier-invoice-staging-web-basegrid.md (2,823)
│   ├── KNOWLEDGE_2025-12-26_supplier-invoice-staging-web-datagrid-final.md (1,532)
│   ├── KNOWLEDGE_2025-12-26_supplier-invoice-staging-web-datagrid.md (1,873)
│   ├── KNOWLEDGE_2025-12-26_supplier-invoice-staging-web.md (3,206)
│   └── KNOWLEDGE_2025-12-27_v32-staging-web-deployment.md (1,483)
├── shared/
│   ├── BOZP_PRAVIDLA.md (318)
│   └── README.md (330)
├── specifications/
│   ├── .gitkeep (0)
│   ├── 2025-12-18_supplier-invoice-staging-db-schema.md (3,993)
│   └── 2025-12-18_supplier-invoice-staging-db.md (5,234)
├── strategic/
│   ├── N8N_TO_TEMPORAL_MIGRATION.md (24.3K)
│   └── NEX_BRAIN_PRODUCT.md (11.9K)
├── tenants/
│   ├── andros/
│   │   ├── hr/
│   │   │   ... (max depth reached)
│   │   ├── processes/
│   │   │   ... (max depth reached)
│   │   ├── technical/
│   │   │   ... (max depth reached)
│   │   └── README.md (569)
│   └── icc/
│       ├── hr/
│       │   ... (max depth reached)
│       ├── processes/
│       │   ... (max depth reached)
│       ├── technical/
│       │   ... (max depth reached)
│       └── README.md (554)
└── TODO_MASTER.md (7,966)
```

## Root files

```
.gitattributes (595)
.gitignore (1,645)
INIT_PROMPT.md (1,267)
INIT_PROMPT_ANDROS_DEPLOYMENT.md (17.2K)
pyproject.toml (482)
README.md-old (7,196)
requirements-rag.txt (326)
```