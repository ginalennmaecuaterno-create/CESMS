-- Add approval and rejection timestamp columns to registrations table
-- Run this SQL in your Supabase SQL Editor

-- Add 'approved_at' column to registrations table
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_schema = 'public' 
        AND table_name = 'registrations' 
        AND column_name = 'approved_at'
    ) THEN
        ALTER TABLE public.registrations 
        ADD COLUMN approved_at TIMESTAMP WITH TIME ZONE;
        
        RAISE NOTICE 'Column "approved_at" added successfully to registrations table';
    ELSE
        RAISE NOTICE 'Column "approved_at" already exists in registrations table';
    END IF;
END $$;

-- Add 'rejected_at' column to registrations table
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_schema = 'public' 
        AND table_name = 'registrations' 
        AND column_name = 'rejected_at'
    ) THEN
        ALTER TABLE public.registrations 
        ADD COLUMN rejected_at TIMESTAMP WITH TIME ZONE;
        
        RAISE NOTICE 'Column "rejected_at" added successfully to registrations table';
    ELSE
        RAISE NOTICE 'Column "rejected_at" already exists in registrations table';
    END IF;
END $$;

-- Summary
DO $$
BEGIN
    RAISE NOTICE '';
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Migration Complete!';
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Added columns:';
    RAISE NOTICE '  - registrations.approved_at';
    RAISE NOTICE '  - registrations.rejected_at';
    RAISE NOTICE '';
    RAISE NOTICE 'These columns will track when registrations are approved or rejected.';
    RAISE NOTICE '========================================';
END $$;
