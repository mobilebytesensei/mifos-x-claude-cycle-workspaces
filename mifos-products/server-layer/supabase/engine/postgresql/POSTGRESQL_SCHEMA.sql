-- =============================================================================
-- ENGINE POSTGRESQL SCHEMA
-- Auto-generated base schema for supabase-engine local PostgreSQL
-- =============================================================================
-- Purpose: Provide sync tracking infrastructure for engine database
-- Usage: Run this script to initialize a new engine database
-- =============================================================================

-- =============================================================================
-- EXTENSIONS
-- =============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =============================================================================
-- SYNC TRACKING INFRASTRUCTURE
-- =============================================================================

-- Sync log table (tracks all sync operations)
CREATE TABLE IF NOT EXISTS _sync_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    table_name TEXT NOT NULL,
    operation TEXT NOT NULL CHECK (operation IN ('sync', 'seed', 'enrich', 'reset')),
    started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    completed_at TIMESTAMPTZ,
    status TEXT NOT NULL CHECK (status IN ('running', 'success', 'error', 'partial')),
    rows_processed INT DEFAULT 0,
    rows_succeeded INT DEFAULT 0,
    rows_failed INT DEFAULT 0,
    error_message TEXT,
    metadata JSONB DEFAULT '{}'::JSONB
);

COMMENT ON TABLE _sync_log IS 'Tracks all sync, seed, and enrich operations';
COMMENT ON COLUMN _sync_log.operation IS 'Type of operation: sync, seed, enrich, reset';
COMMENT ON COLUMN _sync_log.status IS 'Operation status: running, success, error, partial';

-- Indexes for _sync_log
CREATE INDEX IF NOT EXISTS idx_sync_log_table_name ON _sync_log(table_name);
CREATE INDEX IF NOT EXISTS idx_sync_log_status ON _sync_log(status);
CREATE INDEX IF NOT EXISTS idx_sync_log_started_at ON _sync_log(started_at DESC);

-- =============================================================================
-- SYNC TRACKING HELPER FUNCTIONS
-- =============================================================================

-- Function to add sync tracking columns to any table
CREATE OR REPLACE FUNCTION add_sync_tracking(p_table_name TEXT)
RETURNS VOID AS $$
BEGIN
    -- Add sync_status column
    EXECUTE format('
        ALTER TABLE %I
        ADD COLUMN IF NOT EXISTS sync_status TEXT NOT NULL DEFAULT ''pending''
            CHECK (sync_status IN (''pending'', ''synced'', ''dirty'', ''error''))
    ', p_table_name);

    -- Add sync_timestamp column
    EXECUTE format('
        ALTER TABLE %I
        ADD COLUMN IF NOT EXISTS sync_timestamp TIMESTAMPTZ
    ', p_table_name);

    -- Add sync_error column
    EXECUTE format('
        ALTER TABLE %I
        ADD COLUMN IF NOT EXISTS sync_error TEXT
    ', p_table_name);

    -- Add partial index for dirty row queries (excludes synced rows)
    EXECUTE format('
        CREATE INDEX IF NOT EXISTS idx_%I_sync_status
        ON %I (sync_status) WHERE sync_status != ''synced''
    ', p_table_name, p_table_name);

    RAISE NOTICE 'Added sync tracking to table: %', p_table_name;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION add_sync_tracking(TEXT) IS 'Add sync tracking columns to a table';

-- =============================================================================
-- DIRTY ROW TRIGGER
-- =============================================================================

-- Function to mark rows as dirty on update
CREATE OR REPLACE FUNCTION mark_dirty_on_update()
RETURNS TRIGGER AS $$
BEGIN
    -- Only mark dirty if the row was previously synced
    -- and if actual data columns changed (not sync columns)
    IF OLD.sync_status = 'synced' THEN
        -- Check if any non-sync column changed
        IF (OLD.sync_status, OLD.sync_timestamp, OLD.sync_error) IS NOT DISTINCT FROM
           (NEW.sync_status, NEW.sync_timestamp, NEW.sync_error) THEN
            -- Sync columns didn't change, so data columns must have
            NEW.sync_status := 'dirty';
            NEW.sync_timestamp := now();
            NEW.sync_error := NULL;
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION mark_dirty_on_update() IS 'Trigger function to mark synced rows as dirty when updated';

-- Function to create dirty trigger for a table
CREATE OR REPLACE FUNCTION create_dirty_trigger(p_table_name TEXT)
RETURNS VOID AS $$
BEGIN
    -- Drop existing trigger if any
    EXECUTE format('
        DROP TRIGGER IF EXISTS trg_mark_dirty_%I ON %I
    ', p_table_name, p_table_name);

    -- Create new trigger
    EXECUTE format('
        CREATE TRIGGER trg_mark_dirty_%I
            BEFORE UPDATE ON %I
            FOR EACH ROW
            EXECUTE FUNCTION mark_dirty_on_update()
    ', p_table_name, p_table_name);

    RAISE NOTICE 'Created dirty trigger for table: %', p_table_name;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION create_dirty_trigger(TEXT) IS 'Create a trigger to mark rows dirty on update';

-- =============================================================================
-- SYNC QUERY FUNCTIONS
-- =============================================================================

-- Function to get dirty rows for sync
CREATE OR REPLACE FUNCTION get_dirty_rows(
    p_table_name TEXT,
    p_limit INT DEFAULT 1000,
    p_offset INT DEFAULT 0
)
RETURNS TABLE (row_data JSONB) AS $$
BEGIN
    RETURN QUERY EXECUTE format('
        SELECT row_to_json(t.*)::JSONB as row_data
        FROM %I t
        WHERE sync_status IN (''pending'', ''dirty'')
        ORDER BY sync_timestamp NULLS FIRST
        LIMIT %s OFFSET %s
    ', p_table_name, p_limit, p_offset);
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION get_dirty_rows(TEXT, INT, INT) IS 'Get pending/dirty rows for sync with pagination';

-- Function to count dirty rows
CREATE OR REPLACE FUNCTION count_dirty_rows(p_table_name TEXT)
RETURNS BIGINT AS $$
DECLARE
    v_count BIGINT;
BEGIN
    EXECUTE format('
        SELECT COUNT(*)
        FROM %I
        WHERE sync_status IN (''pending'', ''dirty'')
    ', p_table_name)
    INTO v_count;

    RETURN v_count;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION count_dirty_rows(TEXT) IS 'Count rows needing sync';

-- =============================================================================
-- SYNC STATUS UPDATE FUNCTIONS
-- =============================================================================

-- Function to mark rows as synced
CREATE OR REPLACE FUNCTION mark_rows_synced(p_table_name TEXT, p_ids UUID[])
RETURNS INT AS $$
DECLARE
    v_affected INT;
BEGIN
    EXECUTE format('
        UPDATE %I
        SET
            sync_status = ''synced'',
            sync_timestamp = now(),
            sync_error = NULL
        WHERE id = ANY($1)
        AND sync_status != ''synced''
    ', p_table_name)
    USING p_ids;

    GET DIAGNOSTICS v_affected = ROW_COUNT;
    RETURN v_affected;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION mark_rows_synced(TEXT, UUID[]) IS 'Mark specified rows as synced';

-- Function to mark rows as error
CREATE OR REPLACE FUNCTION mark_rows_error(p_table_name TEXT, p_ids UUID[], p_error TEXT)
RETURNS INT AS $$
DECLARE
    v_affected INT;
BEGIN
    EXECUTE format('
        UPDATE %I
        SET
            sync_status = ''error'',
            sync_timestamp = now(),
            sync_error = $2
        WHERE id = ANY($1)
    ', p_table_name)
    USING p_ids, p_error;

    GET DIAGNOSTICS v_affected = ROW_COUNT;
    RETURN v_affected;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION mark_rows_error(TEXT, UUID[], TEXT) IS 'Mark specified rows as sync error';

-- Function to reset sync status for a table
CREATE OR REPLACE FUNCTION reset_sync_status(
    p_table_name TEXT,
    p_status TEXT DEFAULT 'pending'
)
RETURNS INT AS $$
DECLARE
    v_affected INT;
BEGIN
    EXECUTE format('
        UPDATE %I
        SET
            sync_status = $1,
            sync_timestamp = NULL,
            sync_error = NULL
    ', p_table_name)
    USING p_status;

    GET DIAGNOSTICS v_affected = ROW_COUNT;

    -- Log the reset
    INSERT INTO _sync_log (table_name, operation, status, rows_processed)
    VALUES (p_table_name, 'reset', 'success', v_affected);

    RETURN v_affected;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION reset_sync_status(TEXT, TEXT) IS 'Reset sync status for all rows in a table';

-- =============================================================================
-- SYNC LOG FUNCTIONS
-- =============================================================================

-- Function to start a sync operation
CREATE OR REPLACE FUNCTION start_sync_log(
    p_table_name TEXT,
    p_operation TEXT DEFAULT 'sync',
    p_metadata JSONB DEFAULT '{}'::JSONB
)
RETURNS UUID AS $$
DECLARE
    v_id UUID;
BEGIN
    INSERT INTO _sync_log (table_name, operation, status, metadata)
    VALUES (p_table_name, p_operation, 'running', p_metadata)
    RETURNING id INTO v_id;

    RETURN v_id;
END;
$$ LANGUAGE plpgsql;

-- Function to complete a sync operation
CREATE OR REPLACE FUNCTION complete_sync_log(
    p_log_id UUID,
    p_status TEXT,
    p_rows_processed INT DEFAULT 0,
    p_rows_succeeded INT DEFAULT NULL,
    p_rows_failed INT DEFAULT NULL,
    p_error_message TEXT DEFAULT NULL
)
RETURNS VOID AS $$
BEGIN
    UPDATE _sync_log
    SET
        completed_at = now(),
        status = p_status,
        rows_processed = p_rows_processed,
        rows_succeeded = COALESCE(p_rows_succeeded, p_rows_processed),
        rows_failed = COALESCE(p_rows_failed, 0),
        error_message = p_error_message
    WHERE id = p_log_id;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- STATISTICS VIEW
-- =============================================================================

-- This view will be regenerated when tables are added
-- Placeholder that can be updated
CREATE OR REPLACE VIEW sync_statistics AS
SELECT
    '_sync_log'::TEXT as table_name,
    0::BIGINT as pending_count,
    0::BIGINT as synced_count,
    0::BIGINT as dirty_count,
    0::BIGINT as error_count,
    COUNT(*)::BIGINT as total_count
FROM _sync_log;

COMMENT ON VIEW sync_statistics IS 'Aggregated sync statistics across tables (regenerate after adding tables)';

-- Function to regenerate sync_statistics view
CREATE OR REPLACE FUNCTION regenerate_sync_stats_view()
RETURNS VOID AS $$
DECLARE
    v_sql TEXT := '';
    v_table RECORD;
    v_first BOOLEAN := TRUE;
BEGIN
    FOR v_table IN
        SELECT table_name
        FROM information_schema.columns
        WHERE column_name = 'sync_status'
        AND table_schema = 'public'
        AND table_name NOT LIKE '_%'
    LOOP
        IF NOT v_first THEN
            v_sql := v_sql || ' UNION ALL ';
        END IF;

        v_sql := v_sql || format('
            SELECT
                %L::TEXT as table_name,
                COUNT(*) FILTER (WHERE sync_status = ''pending'') as pending_count,
                COUNT(*) FILTER (WHERE sync_status = ''synced'') as synced_count,
                COUNT(*) FILTER (WHERE sync_status = ''dirty'') as dirty_count,
                COUNT(*) FILTER (WHERE sync_status = ''error'') as error_count,
                COUNT(*) as total_count
            FROM %I
        ', v_table.table_name, v_table.table_name);

        v_first := FALSE;
    END LOOP;

    IF v_sql != '' THEN
        EXECUTE 'CREATE OR REPLACE VIEW sync_statistics AS ' || v_sql;
        RAISE NOTICE 'Regenerated sync_statistics view';
    END IF;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- UTILITY FUNCTIONS
-- =============================================================================

-- Function to check if a table has sync tracking
CREATE OR REPLACE FUNCTION has_sync_tracking(p_table_name TEXT)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = p_table_name
        AND column_name = 'sync_status'
        AND table_schema = 'public'
    );
END;
$$ LANGUAGE plpgsql;

-- Function to list tables with sync tracking
CREATE OR REPLACE FUNCTION list_tracked_tables()
RETURNS TABLE (table_name TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT c.table_name::TEXT
    FROM information_schema.columns c
    WHERE c.column_name = 'sync_status'
    AND c.table_schema = 'public'
    AND c.table_name NOT LIKE '_%'
    ORDER BY c.table_name;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- INITIALIZATION COMPLETE
-- =============================================================================

-- Log initialization
INSERT INTO _sync_log (table_name, operation, status, metadata)
VALUES ('_system', 'seed', 'success', '{"message": "Engine PostgreSQL schema initialized"}'::JSONB);

-- Output confirmation
DO $$
BEGIN
    RAISE NOTICE '=============================================================================';
    RAISE NOTICE 'ENGINE POSTGRESQL SCHEMA INITIALIZED SUCCESSFULLY';
    RAISE NOTICE '=============================================================================';
    RAISE NOTICE 'Available functions:';
    RAISE NOTICE '  - add_sync_tracking(table_name)';
    RAISE NOTICE '  - create_dirty_trigger(table_name)';
    RAISE NOTICE '  - get_dirty_rows(table_name, limit, offset)';
    RAISE NOTICE '  - count_dirty_rows(table_name)';
    RAISE NOTICE '  - mark_rows_synced(table_name, ids[])';
    RAISE NOTICE '  - mark_rows_error(table_name, ids[], error)';
    RAISE NOTICE '  - reset_sync_status(table_name, status)';
    RAISE NOTICE '  - regenerate_sync_stats_view()';
    RAISE NOTICE '=============================================================================';
END $$;
