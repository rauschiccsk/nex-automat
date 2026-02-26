-- Migration 002: Seed system data
-- Default admin, groups, 24 modules, admin permissions

BEGIN;

-- ============================================================
-- Admin user (password: 'admin' — bcrypt hash)
-- MUST be changed on first login in production
-- ============================================================
INSERT INTO users (login_name, full_name, password_hash, email, created_by)
VALUES (
    'admin',
    'Administrátor',
    '$2b$12$x5AGAyWA/Td4/EGpv3PGUOSGpz1vl3aimwMgoqh6Z21iUngaqJVD.',
    'admin@icc.sk',
    'system'
) ON CONFLICT (login_name) DO NOTHING;

-- ============================================================
-- Default groups
-- ============================================================
INSERT INTO groups (group_name, level, description, created_by) VALUES
    ('Administrátori', 0, 'Plný prístup ku všetkým modulom', 'system'),
    ('Účtovníctvo', 0, 'Prístup k účtovným modulom', 'system'),
    ('Sklad', 0, 'Prístup k skladovým modulom', 'system'),
    ('Predaj', 0, 'Prístup k predajným modulom', 'system'),
    ('Nákup', 0, 'Prístup k nákupným modulom', 'system')
ON CONFLICT (group_name) DO NOTHING;

-- ============================================================
-- Assign admin to Administrátori group
-- ============================================================
INSERT INTO user_groups (user_id, group_id, created_by)
SELECT u.user_id, g.group_id, 'system'
FROM users u, groups g
WHERE u.login_name = 'admin' AND g.group_name = 'Administrátori'
ON CONFLICT (user_id, group_id) DO NOTHING;

-- ============================================================
-- 24 modules
-- ============================================================
INSERT INTO modules (module_code, module_name, category, icon, module_type, is_mock, sort_order, created_by) VALUES
    ('PAB', 'Evidencia partnerov',       'base',       'Users',            'catalog',  true, 10, 'system'),
    ('GSC', 'Evidencia tovaru',          'base',       'Package',          'catalog',  true, 20, 'system'),
    ('VAH', 'Váhy',                      'base',       'Scale',            'catalog',  true, 30, 'system'),
    ('STK', 'Skladové karty',            'stock',      'Layers',           'catalog',  true, 40, 'system'),
    ('IMB', 'Príjemky',                  'stock',      'ArrowDownToLine',  'document', true, 50, 'system'),
    ('OMB', 'Výdajky',                   'stock',      'ArrowUpFromLine',  'document', true, 60, 'system'),
    ('PMB', 'Presuny',                   'stock',      'ArrowLeftRight',   'document', true, 70, 'system'),
    ('INV', 'Inventúry',                 'stock',      'ClipboardCheck',   'document', true, 80, 'system'),
    ('ICB', 'Odberateľské faktúry',      'sales',      'FileText',         'document', true, 90, 'system'),
    ('PON', 'Ponuky',                    'sales',      'FileHeart',        'document', true, 100, 'system'),
    ('ODB', 'Zákazky',                   'sales',      'ShoppingCart',     'document', true, 110, 'system'),
    ('DOD', 'Dodacie listy',             'sales',      'Truck',            'document', true, 120, 'system'),
    ('ISB', 'Dodávateľské faktúry',      'purchase',   'FileInput',        'document', true, 130, 'system'),
    ('OBJ', 'Objednávky',               'purchase',   'ClipboardList',    'document', true, 140, 'system'),
    ('JRN', 'Účtovný denník',           'accounting', 'BookOpen',         'document', true, 150, 'system'),
    ('ACT', 'Predvaha',                 'accounting', 'Calculator',       'report',   true, 160, 'system'),
    ('VTR', 'DPH',                       'accounting', 'Receipt',          'report',   true, 170, 'system'),
    ('UCT', 'Účtová osnova',            'accounting', 'ListTree',         'catalog',  true, 180, 'system'),
    ('POK', 'Pokladňa',                 'pos',        'Banknote',         'document', true, 190, 'system'),
    ('UZV', 'Uzávierky',                'pos',        'Lock',             'document', true, 200, 'system'),
    ('USR', 'Používatelia',             'system',     'UserCog',          'config',   true, 210, 'system'),
    ('GRP', 'Skupiny práv',             'system',     'Shield',           'config',   true, 220, 'system'),
    ('SET', 'Nastavenia',               'system',     'Settings',         'config',   true, 230, 'system'),
    ('AUD', 'Audit log',                'system',     'ScrollText',       'report',   true, 240, 'system')
ON CONFLICT (module_code) DO NOTHING;

-- ============================================================
-- Admin group: full permissions on ALL modules
-- ============================================================
INSERT INTO group_module_permissions (group_id, module_id, can_view, can_create, can_edit, can_delete, can_print, can_export, can_admin, created_by)
SELECT g.group_id, m.module_id, true, true, true, true, true, true, true, 'system'
FROM groups g, modules m
WHERE g.group_name = 'Administrátori'
ON CONFLICT (group_id, module_id) DO NOTHING;

COMMIT;
