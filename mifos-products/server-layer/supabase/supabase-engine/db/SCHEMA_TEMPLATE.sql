-- =============================================================================
-- Supabase Engine Schema Template
-- =============================================================================
--
-- Template Variables:
--     {TABLE_NAME}       - Primary table name (e.g., movies)
--     {TABLE_NAME_UPPER} - Uppercase table name for trigger names
--
-- Features:
--     - UUID primary key (gen_random_uuid)
--     - Sync tracking columns (sync_status, sync_timestamp, sync_error)
--     - Automatic dirty marking on updates
--     - Indexes for sync queries
--
-- Rule: RULE-ENGINE-AUTO-001
-- =============================================================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =============================================================================
-- Main Table: {TABLE_NAME}
-- =============================================================================
-- Customize this section for your specific data model

CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    -- Primary Key
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- External IDs (example: for movies)
    -- imdb_id TEXT UNIQUE,
    -- tmdb_id INTEGER,

    -- Core Data Fields (customize these)
    -- title TEXT NOT NULL,
    -- description TEXT,
    -- year INTEGER,
    -- rating NUMERIC(3, 1),

    -- JSONB fields for flexible data
    -- metadata JSONB DEFAULT '{}'::jsonb,
    -- tags JSONB DEFAULT '[]'::jsonb,

    -- ==========================================================================
    -- Sync Tracking Columns (REQUIRED - Do not modify)
    -- ==========================================================================
    sync_status TEXT NOT NULL DEFAULT 'pending'
        CHECK (sync_status IN ('pending', 'synced', 'dirty', 'error')),
    sync_timestamp TIMESTAMPTZ,
    sync_error TEXT,

    -- Audit Columns
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    source TEXT  -- Track data origin (api, csv, manual, etc.)
);

-- =============================================================================
-- Indexes for Sync Operations
-- =============================================================================

-- Fast lookup of dirty/pending rows for sync
CREATE INDEX IF NOT EXISTS idx_{TABLE_NAME}_sync_status
    ON {TABLE_NAME}(sync_status)
    WHERE sync_status IN ('pending', 'dirty', 'error');

-- Fast lookup by sync timestamp for incremental sync
CREATE INDEX IF NOT EXISTS idx_{TABLE_NAME}_sync_timestamp
    ON {TABLE_NAME}(sync_timestamp)
    WHERE sync_timestamp IS NOT NULL;

-- Fast lookup by updated_at for change detection
CREATE INDEX IF NOT EXISTS idx_{TABLE_NAME}_updated_at
    ON {TABLE_NAME}(updated_at);

-- =============================================================================
-- Trigger: Auto-mark rows as dirty on update
-- =============================================================================

CREATE OR REPLACE FUNCTION mark_{TABLE_NAME}_dirty()
RETURNS TRIGGER AS $$
BEGIN
    -- Only mark as dirty if currently synced
    IF OLD.sync_status = 'synced' THEN
        NEW.sync_status := 'dirty';
        NEW.updated_at := NOW();
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Drop existing trigger if exists (for idempotent schema updates)
DROP TRIGGER IF EXISTS trigger_{TABLE_NAME}_dirty ON {TABLE_NAME};

-- Create trigger
CREATE TRIGGER trigger_{TABLE_NAME}_dirty
    BEFORE UPDATE ON {TABLE_NAME}
    FOR EACH ROW
    WHEN (OLD.* IS DISTINCT FROM NEW.*)
    EXECUTE FUNCTION mark_{TABLE_NAME}_dirty();

-- =============================================================================
-- Utility Functions
-- =============================================================================

-- Get count of rows by sync status
CREATE OR REPLACE FUNCTION get_{TABLE_NAME}_sync_stats()
RETURNS TABLE (
    status TEXT,
    count BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT sync_status, COUNT(*)
    FROM {TABLE_NAME}
    GROUP BY sync_status
    ORDER BY sync_status;
END;
$$ LANGUAGE plpgsql;

-- Mark synced rows
CREATE OR REPLACE FUNCTION mark_{TABLE_NAME}_synced(row_ids UUID[])
RETURNS INTEGER AS $$
DECLARE
    updated_count INTEGER;
BEGIN
    UPDATE {TABLE_NAME}
    SET
        sync_status = 'synced',
        sync_timestamp = NOW(),
        sync_error = NULL
    WHERE id = ANY(row_ids);

    GET DIAGNOSTICS updated_count = ROW_COUNT;
    RETURN updated_count;
END;
$$ LANGUAGE plpgsql;

-- Mark error rows
CREATE OR REPLACE FUNCTION mark_{TABLE_NAME}_error(row_ids UUID[], error_msg TEXT)
RETURNS INTEGER AS $$
DECLARE
    updated_count INTEGER;
BEGIN
    UPDATE {TABLE_NAME}
    SET
        sync_status = 'error',
        sync_timestamp = NOW(),
        sync_error = error_msg
    WHERE id = ANY(row_ids);

    GET DIAGNOSTICS updated_count = ROW_COUNT;
    RETURN updated_count;
END;
$$ LANGUAGE plpgsql;

-- Reset all to pending (for full re-sync)
CREATE OR REPLACE FUNCTION reset_{TABLE_NAME}_sync()
RETURNS INTEGER AS $$
DECLARE
    updated_count INTEGER;
BEGIN
    UPDATE {TABLE_NAME}
    SET
        sync_status = 'pending',
        sync_timestamp = NULL,
        sync_error = NULL;

    GET DIAGNOSTICS updated_count = ROW_COUNT;
    RETURN updated_count;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- Example: Movies Table (for mood-movies project)
-- =============================================================================
--
-- CREATE TABLE IF NOT EXISTS movies (
--     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
--
--     -- External IDs
--     imdb_id TEXT UNIQUE,
--     tmdb_id INTEGER,
--
--     -- Core Movie Data
--     title TEXT NOT NULL,
--     original_title TEXT,
--     overview TEXT,
--     tagline TEXT,
--     release_date DATE,
--     runtime INTEGER,
--     budget BIGINT,
--     revenue BIGINT,
--
--     -- Media
--     poster_path TEXT,
--     backdrop_path TEXT,
--
--     -- Ratings
--     vote_average NUMERIC(3, 1),
--     vote_count INTEGER,
--     popularity NUMERIC(10, 3),
--
--     -- Classification (JSONB for flexibility)
--     genres JSONB DEFAULT '[]'::jsonb,
--     keywords JSONB DEFAULT '[]'::jsonb,
--     production_companies JSONB DEFAULT '[]'::jsonb,
--     production_countries JSONB DEFAULT '[]'::jsonb,
--     spoken_languages JSONB DEFAULT '[]'::jsonb,
--
--     -- Mood Movies Specific
--     moods JSONB DEFAULT '[]'::jsonb,
--     emotions JSONB DEFAULT '[]'::jsonb,
--     quality_score NUMERIC(5, 2),
--
--     -- Sync Tracking (REQUIRED)
--     sync_status TEXT NOT NULL DEFAULT 'pending'
--         CHECK (sync_status IN ('pending', 'synced', 'dirty', 'error')),
--     sync_timestamp TIMESTAMPTZ,
--     sync_error TEXT,
--
--     -- Audit
--     created_at TIMESTAMPTZ DEFAULT NOW(),
--     updated_at TIMESTAMPTZ DEFAULT NOW(),
--     source TEXT
-- );
