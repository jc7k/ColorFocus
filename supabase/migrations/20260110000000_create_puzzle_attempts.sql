-- Create puzzle_attempts table for storing user puzzle history
-- This migration creates the table and sets up Row Level Security (RLS) policies

-- Create the puzzle_attempts table
CREATE TABLE IF NOT EXISTS puzzle_attempts (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,

    -- Puzzle configuration
    seed INTEGER NOT NULL,
    grid_size INTEGER NOT NULL CHECK (grid_size >= 1 AND grid_size <= 8),
    color_count INTEGER NOT NULL CHECK (color_count >= 1 AND color_count <= 8),
    difficulty TEXT NOT NULL CHECK (difficulty IN ('accessible', 'standard', 'advanced', 'custom')),
    language TEXT NOT NULL CHECK (language IN ('zh-TW', 'english', 'spanish', 'vietnamese')),
    congruence_percent DECIMAL(5,2) NOT NULL CHECK (congruence_percent >= 0 AND congruence_percent <= 100),

    -- User answers and results
    user_answers JSONB NOT NULL,
    correct_answers JSONB NOT NULL,
    correct_count INTEGER NOT NULL CHECK (correct_count >= 0),
    total_colors INTEGER NOT NULL CHECK (total_colors >= 1),
    accuracy_percent INTEGER NOT NULL CHECK (accuracy_percent >= 0 AND accuracy_percent <= 100),
    total_off INTEGER NOT NULL CHECK (total_off >= 0)
);

-- Create index on user_id for faster queries
CREATE INDEX IF NOT EXISTS idx_puzzle_attempts_user_id ON puzzle_attempts(user_id);

-- Create index on created_at for time-based queries
CREATE INDEX IF NOT EXISTS idx_puzzle_attempts_created_at ON puzzle_attempts(created_at DESC);

-- Enable Row Level Security
ALTER TABLE puzzle_attempts ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only insert their own attempts
CREATE POLICY "Users can insert own attempts"
    ON puzzle_attempts
    FOR INSERT
    TO authenticated
    WITH CHECK (auth.uid() = user_id);

-- Policy: Users can only view their own attempts
CREATE POLICY "Users can view own attempts"
    ON puzzle_attempts
    FOR SELECT
    TO authenticated
    USING (auth.uid() = user_id);

-- Note: No UPDATE or DELETE policies - puzzle history is immutable
