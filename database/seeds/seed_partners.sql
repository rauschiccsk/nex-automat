-- Seed: 10 sample partners for PAB module
-- Covers: SK/CZ/HU/AT, customer/supplier/both, various payment methods,
--         billing/shipping addresses, active/inactive, VAT/non-VAT
-- Uses real DB column names from: \d partners

BEGIN;

-- PAB001 — Plné dáta, both, Komárno, IBAN SK, IČO, DPH
INSERT INTO partners (
    code, name, partner_type, is_supplier, is_customer,
    company_id, tax_id, vat_id, is_vat_payer,
    street, city, zip_code, country_code,
    billing_street, billing_city, billing_zip_code, billing_country_code,
    shipping_street, shipping_city, shipping_zip_code, shipping_country_code,
    phone, mobile, email, website, contact_person,
    payment_due_days, credit_limit, discount_percent, price_category,
    payment_method, currency,
    iban, bank_name, swift_bic,
    notes, is_active, created_by, updated_by
) VALUES (
    'PAB001', 'Mágerstav s.r.o.', 'both', true, true,
    '36521001', '2021234567', 'SK2021234567', true,
    'Hlavná 15', 'Komárno', '94501', 'SK',
    'Fakturačná 8', 'Komárno', '94501', 'SK',
    NULL, NULL, NULL, NULL,
    '+421 35 7701234', '+421 905 123456', 'info@magerstav.sk', 'www.magerstav.sk', 'Ing. Ján Máger',
    14, 10000.00, 5.00, 'A',
    'transfer', 'EUR',
    'SK3112000000001987654321', 'Všeobecná úverová banka', 'SUBASKBX',
    'Kľúčový partner, dodávateľ aj odberateľ stavebného materiálu', true, 'seed', 'seed'
) ON CONFLICT (code) DO NOTHING;

-- PAB002 — Dodávateľ, Bratislava, iná fakturačná adresa
INSERT INTO partners (
    code, name, partner_type, is_supplier, is_customer,
    company_id, tax_id, vat_id, is_vat_payer,
    street, city, zip_code, country_code,
    billing_street, billing_city, billing_zip_code, billing_country_code,
    phone, email, contact_person,
    payment_due_days, credit_limit, discount_percent,
    payment_method, currency,
    iban, bank_name, swift_bic,
    is_active, created_by, updated_by
) VALUES (
    'PAB002', 'Stavmat s.r.o.', 'supplier', true, false,
    '31322581', '2020345678', 'SK2020345678', true,
    'Priemyselná 22', 'Bratislava', '82104', 'SK',
    'Panónska cesta 1', 'Bratislava', '85101', 'SK',
    '+421 2 44556677', 'obchod@stavmat.sk', 'Peter Horváth',
    30, 0.00, 3.00,
    'transfer', 'EUR',
    'SK8509000000005012345678', 'Slovenská sporiteľňa', 'GIBASKBX',
    true, 'seed', 'seed'
) ON CONFLICT (code) DO NOTHING;

-- PAB003 — Odberateľ, Nové Zámky, kreditný limit 5000
INSERT INTO partners (
    code, name, partner_type, is_supplier, is_customer,
    company_id, tax_id, vat_id, is_vat_payer,
    street, city, zip_code, country_code,
    phone, email, contact_person,
    payment_due_days, credit_limit, discount_percent,
    payment_method, currency,
    iban, bank_name, swift_bic,
    is_active, created_by, updated_by
) VALUES (
    'PAB003', 'Kovosteel a.s.', 'customer', false, true,
    '44556677', '2022334455', 'SK2022334455', true,
    'Továrenská 5', 'Nové Zámky', '94002', 'SK',
    '+421 35 6401234', 'kovosteel@kovosteel.sk', 'Mária Kováčová',
    14, 5000.00, 0.00,
    'transfer', 'EUR',
    'SK2611000000002612345678', 'Tatra banka', 'TATRSKBX',
    true, 'seed', 'seed'
) ON CONFLICT (code) DO NOTHING;

-- PAB004 — Dodávateľ, Košice, splatnosť 30 dní
INSERT INTO partners (
    code, name, partner_type, is_supplier, is_customer,
    company_id, tax_id, vat_id, is_vat_payer,
    street, city, zip_code, country_code,
    phone, mobile, email, contact_person,
    payment_due_days, credit_limit, discount_percent,
    payment_method, currency,
    iban, bank_name, swift_bic,
    is_active, created_by, updated_by
) VALUES (
    'PAB004', 'Drevex Trade s.r.o.', 'supplier', true, false,
    '50123456', '2023456789', 'SK2023456789', true,
    'Južná trieda 88', 'Košice', '04001', 'SK',
    '+421 55 6223344', '+421 917 234567', 'drevex@drevex.sk', 'Tomáš Drevený',
    30, 0.00, 10.00,
    'transfer', 'EUR',
    'SK7575000000004023456789', 'ČSOB', 'CABORSKBX',
    true, 'seed', 'seed'
) ON CONFLICT (code) DO NOTHING;

-- PAB005 — FO (SZČO), bez IČ DPH, is_vat_payer=false
INSERT INTO partners (
    code, name, partner_type, is_supplier, is_customer,
    company_id, tax_id, is_vat_payer,
    street, city, zip_code, country_code,
    mobile, email,
    payment_due_days, credit_limit, discount_percent,
    payment_method, currency,
    is_active, created_by, updated_by
) VALUES (
    'PAB005', 'Ján Novák - SZČO', 'customer', false, true,
    '12345678', '1012345678', false,
    'Záhradná 3', 'Komárno', '94501', 'SK',
    '+421 903 345678', 'jan.novak@gmail.com',
    7, 1000.00, 0.00,
    'cash', 'EUR',
    true, 'seed', 'seed'
) ON CONFLICT (code) DO NOTHING;

-- PAB006 — CZ partner, country_code=CZ, mena CZK, both
INSERT INTO partners (
    code, name, partner_type, is_supplier, is_customer,
    company_id, tax_id, vat_id, is_vat_payer,
    street, city, zip_code, country_code,
    billing_street, billing_city, billing_zip_code, billing_country_code,
    phone, email, website, contact_person,
    payment_due_days, credit_limit, discount_percent,
    payment_method, currency,
    iban, bank_name, swift_bic,
    is_active, created_by, updated_by
) VALUES (
    'PAB006', 'EuroStav Group a.s.', 'both', true, true,
    '27082440', '2027082440', 'CZ27082440', true,
    'Vinohradská 120', 'Praha', '13000', 'CZ',
    'Na Příkopě 15', 'Praha', '11000', 'CZ',
    '+420 221 456789', 'info@eurostav.cz', 'www.eurostav.cz', 'Karel Novotný',
    21, 20000.00, 3.00,
    'transfer', 'CZK',
    'CZ6508000000192000145399', 'Česká spořitelna', 'GIBACZPX',
    true, 'seed', 'seed'
) ON CONFLICT (code) DO NOTHING;

-- PAB007 — HU partner, country_code=HU, mena EUR
INSERT INTO partners (
    code, name, partner_type, is_supplier, is_customer,
    company_id, tax_id, vat_id, is_vat_payer,
    street, city, zip_code, country_code,
    phone, email, contact_person,
    payment_due_days, credit_limit, discount_percent,
    payment_method, currency,
    iban, bank_name, swift_bic,
    is_active, created_by, updated_by
) VALUES (
    'PAB007', 'TechnoPlast Kft.', 'customer', false, true,
    '12345678901', '12345678202', 'HU12345678', true,
    'Győri út 45', 'Győr', '9021', 'HU',
    '+36 96 512345', 'techno@technoplast.hu', 'László Nagy',
    14, 3000.00, 0.00,
    'transfer', 'EUR',
    'HU42117730161111101800000000', 'OTP Bank', 'OTPVHUHB',
    true, 'seed', 'seed'
) ON CONFLICT (code) DO NOTHING;

-- PAB008 — Neaktívny partner
INSERT INTO partners (
    code, name, partner_type, is_supplier, is_customer,
    company_id, tax_id, vat_id, is_vat_payer,
    street, city, zip_code, country_code,
    phone, email,
    payment_due_days, credit_limit, discount_percent,
    payment_method, currency,
    is_active, created_by, updated_by
) VALUES (
    'PAB008', 'Neaktívny Partner s.r.o.', 'customer', false, true,
    '99887766', '2099887766', 'SK2099887766', true,
    'Stará 1', 'Nitra', '94901', 'SK',
    '+421 37 6559900', 'info@neaktivny.sk',
    14, 0.00, 0.00,
    'transfer', 'EUR',
    false, 'seed', 'seed'
) ON CONFLICT (code) DO NOTHING;

-- PAB009 — AT partner, SWIFT, kredit 50000, shipping adresa iná
INSERT INTO partners (
    code, name, partner_type, is_supplier, is_customer,
    company_id, tax_id, vat_id, is_vat_payer,
    street, city, zip_code, country_code,
    shipping_street, shipping_city, shipping_zip_code, shipping_country_code,
    phone, email, website, contact_person,
    payment_due_days, credit_limit, discount_percent,
    payment_method, currency,
    iban, bank_name, swift_bic,
    notes, is_active, created_by, updated_by
) VALUES (
    'PAB009', 'ALDI Purchasing GmbH', 'supplier', true, false,
    'FN123456a', 'ATU12345678', 'ATU12345678', true,
    'Industriestraße 10', 'Wien', '1200', 'AT',
    'Lagerstraße 5', 'Schwechat', '2320', 'AT',
    '+43 1 7654321', 'purchasing@aldi.at', 'www.aldi.at', 'Hans Müller',
    60, 50000.00, 5.00,
    'transfer', 'EUR',
    'AT611904300234573201', 'Erste Bank', 'GIBAATWWXXX',
    'Hlavný dodávateľ pre AT región, preferovaná platba SEPA', true, 'seed', 'seed'
) ON CONFLICT (code) DO NOTHING;

-- PAB010 — Len povinné polia
INSERT INTO partners (
    code, name, partner_type, is_supplier, is_customer,
    is_vat_payer,
    city, country_code,
    payment_method, currency,
    is_active, created_by, updated_by
) VALUES (
    'PAB010', 'Lokálny Obchod', 'customer', false, true,
    false,
    'Komárno', 'SK',
    'cod', 'EUR',
    true, 'seed', 'seed'
) ON CONFLICT (code) DO NOTHING;

COMMIT;
