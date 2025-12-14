-- Complete Database Setup for Missing Features
-- Run this ONCE in your Supabase SQL Editor
-- This will add all missing columns and tables

-- ============================================
-- PART 1: Fix Attendance Tracking
-- ============================================

-- Add 'attended' column to registrations table
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
        
        RAISE NOTICE 'Column "attended" added to registrations table';
    ELSE
        RAISE NOTICE 'Column "attended" already exists';
    END IF;
END $$;

-- Add 'attended_at' column to track check-in time
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
        
        RAISE NOTICE 'Column "attended_at" added to registrations table';
    ELSE
        RAISE NOTICE 'Column "attended_at" already exists';
    END IF;
END $$;

-- Remove old 'attendance_time' column if it exists (for cleanup)
DO $$ 
BEGIN
    IF EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_schema = 'public' 
        AND table_name = 'registrations' 
        AND column_name = 'attendance_time'
    ) THEN
        -- Copy data from old column to new column first
        EXECUTE 'UPDATE public.registrations SET attended_at = attendance_time WHERE attendance_time IS NOT NULL';
        
        -- Drop old column
        ALTER TABLE public.registrations DROP COLUMN attendance_time;
        
        RAISE NOTICE 'Old column "attendance_time" migrated to "attended_at" and removed';
    END IF;
END $$;

-- ============================================
-- PART 2: Requirements Tracking Tables
-- ============================================

-- Table 1: event_requirements
CREATE TABLE IF NOT EXISTS public.event_requirements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_id UUID NOT NULL REFERENCES public.events(id) ON DELETE CASCADE,
    requirement_name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table 2: registration_requirements
CREATE TABLE IF NOT EXISTS public.registration_requirements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    registration_id UUID NOT NULL REFERENCES public.registrations(id) ON DELETE CASCADE,
    requirement_id UUID NOT NULL REFERENCES public.event_requirements(id) ON DELETE CASCADE,
    student_submitted BOOLEAN DEFAULT FALSE,
    department_verified BOOLEAN DEFAULT FALSE,
    submitted_at TIMESTAMP WITH TIME ZONE,
    verified_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(registration_id, requirement_id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_event_requirements_event_id 
    ON public.event_requirements(event_id);
    
CREATE INDEX IF NOT EXISTS idx_registration_requirements_registration_id 
    ON public.registration_requirements(registration_id);
    
CREATE INDEX IF NOT EXISTS idx_registration_requirements_requirement_id 
    ON public.registration_requirements(requirement_id);

-- ============================================
-- PART 3: Triggers and Functions
-- ============================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for event_requirements
DROP TRIGGER IF EXISTS update_event_requirements_updated_at ON public.event_requirements;
CREATE TRIGGER update_event_requirements_updated_at
    BEFORE UPDATE ON public.event_requirements
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger for registration_requirements
DROP TRIGGER IF EXISTS update_registration_requirements_updated_at ON public.registration_requirements;
CREATE TRIGGER update_registration_requirements_updated_at
    BEFORE UPDATE ON public.registration_requirements
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Function to set submitted_at timestamp
CREATE OR REPLACE FUNCTION set_submitted_at()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.student_submitted = TRUE AND (OLD.student_submitted = FALSE OR OLD.student_submitted IS NULL) THEN
        NEW.submitted_at = NOW();
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for submitted_at
DROP TRIGGER IF EXISTS set_registration_requirements_submitted_at ON public.registration_requirements;
CREATE TRIGGER set_registration_requirements_submitted_at
    BEFORE UPDATE ON public.registration_requirements
    FOR EACH ROW
    EXECUTE FUNCTION set_submitted_at();

-- Function to set verified_at timestamp
CREATE OR REPLACE FUNCTION set_verified_at()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.department_verified = TRUE AND (OLD.department_verified = FALSE OR OLD.department_verified IS NULL) THEN
        NEW.verified_at = NOW();
    ELSIF NEW.department_verified = FALSE THEN
        NEW.verified_at = NULL;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for verified_at
DROP TRIGGER IF EXISTS set_registration_requirements_verified_at ON public.registration_requirements;
CREATE TRIGGER set_registration_requirements_verified_at
    BEFORE UPDATE ON public.registration_requirements
    FOR EACH ROW
    EXECUTE FUNCTION set_verified_at();

-- ============================================
-- Success Summary
-- ============================================

DO $$
BEGIN
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Database setup completed successfully!';
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Added columns:';
    RAISE NOTICE '  - registrations.attended';
    RAISE NOTICE '  - registrations.attended_at';
    RAISE NOTICE '';
    RAISE NOTICE 'Created tables:';
    RAISE NOTICE '  - event_requirements';
    RAISE NOTICE '  - registration_requirements';
    RAISE NOTICE '';
    RAISE NOTICE 'Created indexes and triggers';
    RAISE NOTICE '========================================';
END $$;

SELECT 'Setup complete! All missing tables and columns have been added.' AS status;
