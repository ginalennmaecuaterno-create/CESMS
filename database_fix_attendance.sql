-- Fix Attendance Tracking - Add missing 'attended' column
-- Run this SQL in your Supabase SQL Editor

-- Add 'attended' column to registrations table if it doesn't exist
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_schema = 'public' 
        AND table_name = 'registrations' 
        AND column_name = 'attended'
    ) THEN
        ALTER TABLE public.registrations 
        ADD COLUMN attended BOOLEAN DEFAULT FALSE;
        
        RAISE NOTICE 'Column "attended" added successfully to registrations table';
    ELSE
        RAISE NOTICE 'Column "attended" already exists in registrations table';
    END IF;
END $$;

-- Add 'attended_at' column to track when student checked in
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_schema = 'public' 
        AND table_name = 'registrations' 
        AND column_name = 'attended_at'
    ) THEN
        ALTER TABLE public.registrations 
        ADD COLUMN attended_at TIMESTAMP WITH TIME ZONE;
        
        RAISE NOTICE 'Column "attended_at" added successfully to registrations table';
    ELSE
        RAISE NOTICE 'Column "attended_at" already exists in registrations table';
    END IF;
END $$;

-- Success message
SELECT 'Attendance columns added successfully!' AS status;
