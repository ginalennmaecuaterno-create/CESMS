-- Requirements Tracking System Database Setup (Simple Version - No RLS)
-- Run this SQL in your Supabase SQL Editor if you're NOT using Supabase Auth

-- Table 1: event_requirements
-- Stores the list of requirements for each event
CREATE TABLE IF NOT EXISTS public.event_requirements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_id UUID NOT NULL REFERENCES public.events(id) ON DELETE CASCADE,
    requirement_name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table 2: registration_requirements
-- Tracks the status of each requirement for each student registration
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

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_event_requirements_event_id ON public.event_requirements(event_id);
CREATE INDEX IF NOT EXISTS idx_registration_requirements_registration_id ON public.registration_requirements(registration_id);
CREATE INDEX IF NOT EXISTS idx_registration_requirements_requirement_id ON public.registration_requirements(requirement_id);

-- Create trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_event_requirements_updated_at ON public.event_requirements;
CREATE TRIGGER update_event_requirements_updated_at
    BEFORE UPDATE ON public.event_requirements
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_registration_requirements_updated_at ON public.registration_requirements;
CREATE TRIGGER update_registration_requirements_updated_at
    BEFORE UPDATE ON public.registration_requirements
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create trigger to automatically set submitted_at when student_submitted becomes true
CREATE OR REPLACE FUNCTION set_submitted_at()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.student_submitted = TRUE AND (OLD.student_submitted = FALSE OR OLD.student_submitted IS NULL) THEN
        NEW.submitted_at = NOW();
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS set_registration_requirements_submitted_at ON public.registration_requirements;
CREATE TRIGGER set_registration_requirements_submitted_at
    BEFORE UPDATE ON public.registration_requirements
    FOR EACH ROW
    EXECUTE FUNCTION set_submitted_at();

-- Create trigger to automatically set verified_at when department_verified becomes true
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

DROP TRIGGER IF EXISTS set_registration_requirements_verified_at ON public.registration_requirements;
CREATE TRIGGER set_registration_requirements_verified_at
    BEFORE UPDATE ON public.registration_requirements
    FOR EACH ROW
    EXECUTE FUNCTION set_verified_at();

-- Success message
SELECT 'Requirements tracking tables created successfully!' AS status;
