-- Seed Data for {{PROJECT_NAME}}
-- This file runs after migrations during `supabase db reset`
-- Add initial/reference data here

-- =============================================================================
-- REFERENCE DATA
-- =============================================================================

-- Example: Categories
-- INSERT INTO categories (id, name, slug) VALUES
--     ('cat_1', 'Category One', 'category-one'),
--     ('cat_2', 'Category Two', 'category-two'),
--     ('cat_3', 'Category Three', 'category-three')
-- ON CONFLICT (id) DO NOTHING;

-- Example: Settings
-- INSERT INTO app_settings (key, value) VALUES
--     ('app_name', '{{PROJECT_NAME}}'),
--     ('version', '1.0.0'),
--     ('maintenance_mode', 'false')
-- ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value;

-- =============================================================================
-- TEST DATA (Development Only)
-- =============================================================================

-- Only insert test data in development environment
-- DO $$
-- BEGIN
--     IF current_setting('app.environment', true) = 'development' THEN
--         -- Insert test users, items, etc.
--     END IF;
-- END $$;

-- =============================================================================
-- NOTES
-- =============================================================================

-- 1. Use ON CONFLICT to make seeding idempotent
-- 2. Reference data should work in all environments
-- 3. Test data should be conditional on environment
-- 4. Keep this file organized by table/domain
