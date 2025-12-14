-- Feedback System Database Setup
-- Run this SQL in your Supabase SQL Editor

-- Table: event_feedback
-- Stores student feedback for events they attended
CREATE TABLE IF NOT EXISTS public.event_feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    registration_id UUID NOT NULL REFERENCES public.registrations(id) ON DELETE CASCADE,
    event_id UUID NOT NULL REFERENCES public.events(id) ON DELETE CASCADE,
    student_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(registration_id)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_event_feedback_event_id ON public.event_feedback(event_id);
CREATE INDEX IF NOT EXISTS idx_event_feedback_student_id ON public.event_feedback(student_id);
CREATE INDEX IF NOT EXISTS idx_event_feedback_registration_id ON public.event_feedback(registration_id);

-- Trigger to update updated_at timestamp
DROP TRIGGER IF EXISTS update_event_feedback_updated_at ON public.event_feedback;
CREATE TRIGGER update_event_feedback_updated_at
    BEFORE UPDATE ON public.event_feedback
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Success message
SELECT 'Feedback system table created successfully!' AS status;
