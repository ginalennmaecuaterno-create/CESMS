-- Requirements Tracking System Database Setup
-- Run this SQL in your Supabase SQL Editor

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

-- Enable Row Level Security (RLS)
ALTER TABLE public.event_requirements ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.registration_requirements ENABLE ROW LEVEL SECURITY;

-- RLS Policies for event_requirements
-- Allow departments to manage requirements for their own events
CREATE POLICY "Departments can view requirements for their events"
    ON public.event_requirements FOR SELECT
    USING (
        event_id IN (
            SELECT id FROM public.events 
            WHERE department_id = auth.uid()
        )
    );

CREATE POLICY "Departments can insert requirements for their events"
    ON public.event_requirements FOR INSERT
    WITH CHECK (
        event_id IN (
            SELECT id FROM public.events 
            WHERE department_id = auth.uid()
        )
    );

CREATE POLICY "Departments can update requirements for their events"
    ON public.event_requirements FOR UPDATE
    USING (
        event_id IN (
            SELECT id FROM public.events 
            WHERE department_id = auth.uid()
        )
    );

CREATE POLICY "Departments can delete requirements for their events"
    ON public.event_requirements FOR DELETE
    USING (
        event_id IN (
            SELECT id FROM public.events 
            WHERE department_id = auth.uid()
        )
    );

-- Students can view requirements for events they registered for
CREATE POLICY "Students can view requirements for their registrations"
    ON public.event_requirements FOR SELECT
    USING (
        event_id IN (
            SELECT event_id FROM public.registrations 
            WHERE student_id = auth.uid()
        )
    );

-- RLS Policies for registration_requirements
-- Departments can view and manage requirement status for their events
CREATE POLICY "Departments can view registration requirements for their events"
    ON public.registration_requirements FOR SELECT
    USING (
        registration_id IN (
            SELECT r.id FROM public.registrations r
            JOIN public.events e ON r.event_id = e.id
            WHERE e.department_id = auth.uid()
        )
    );

CREATE POLICY "Departments can insert registration requirements"
    ON public.registration_requirements FOR INSERT
    WITH CHECK (
        registration_id IN (
            SELECT r.id FROM public.registrations r
            JOIN public.events e ON r.event_id = e.id
            WHERE e.department_id = auth.uid()
        )
    );

CREATE POLICY "Departments can update registration requirements"
    ON public.registration_requirements FOR UPDATE
    USING (
        registration_id IN (
            SELECT r.id FROM public.registrations r
            JOIN public.events e ON r.event_id = e.id
            WHERE e.department_id = auth.uid()
        )
    );

-- Students can view their own requirement status
CREATE POLICY "Students can view their own registration requirements"
    ON public.registration_requirements FOR SELECT
    USING (
        registration_id IN (
            SELECT id FROM public.registrations 
            WHERE student_id = auth.uid()
        )
    );

-- Students can update their submission status
CREATE POLICY "Students can update their submission status"
    ON public.registration_requirements FOR UPDATE
    USING (
        registration_id IN (
            SELECT id FROM public.registrations 
            WHERE student_id = auth.uid()
        )
    )
    WITH CHECK (
        registration_id IN (
            SELECT id FROM public.registrations 
            WHERE student_id = auth.uid()
        )
    );

-- Students can insert their requirement submissions
CREATE POLICY "Students can insert their requirement submissions"
    ON public.registration_requirements FOR INSERT
    WITH CHECK (
        registration_id IN (
            SELECT id FROM public.registrations 
            WHERE student_id = auth.uid()
        )
    );

-- Create trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_event_requirements_updated_at
    BEFORE UPDATE ON public.event_requirements
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_registration_requirements_updated_at
    BEFORE UPDATE ON public.registration_requirements
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create trigger to automatically set submitted_at when student_submitted becomes true
CREATE OR REPLACE FUNCTION set_submitted_at()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.student_submitted = TRUE AND OLD.student_submitted = FALSE THEN
        NEW.submitted_at = NOW();
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

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

CREATE TRIGGER set_registration_requirements_verified_at
    BEFORE UPDATE ON public.registration_requirements
    FOR EACH ROW
    EXECUTE FUNCTION set_verified_at();

-- Grant necessary permissions
GRANT ALL ON public.event_requirements TO authenticated;
GRANT ALL ON public.registration_requirements TO authenticated;

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'Requirements tracking tables created successfully!';
    RAISE NOTICE 'Tables created: event_requirements, registration_requirements';
    RAISE NOTICE 'Indexes, RLS policies, and triggers have been set up.';
END $$;
