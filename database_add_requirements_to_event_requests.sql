-- Add requirements column to event_requests table
-- This will store requirements as JSON array when department requests an event

ALTER TABLE event_requests 
ADD COLUMN IF NOT EXISTS requirements JSONB DEFAULT '[]'::jsonb;

-- Add comment
COMMENT ON COLUMN event_requests.requirements IS 'JSON array of requirement names for limited events';
