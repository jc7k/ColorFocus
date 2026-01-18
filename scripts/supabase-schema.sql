-- =============================================
-- ColorFocus Database Schema
-- Run this in your Supabase SQL Editor
-- =============================================

-- Table: puzzle_history
-- Stores completed puzzles with user answers and accuracy
CREATE TABLE puzzle_history (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,

  -- Puzzle configuration
  seed TEXT NOT NULL,
  grid_size INTEGER NOT NULL CHECK (grid_size >= 1 AND grid_size <= 8),
  color_count INTEGER NOT NULL CHECK (color_count >= 2 AND color_count <= 8),
  congruence_percent INTEGER NOT NULL CHECK (congruence_percent >= 0 AND congruence_percent <= 100),
  difficulty TEXT NOT NULL CHECK (difficulty IN ('accessible', 'standard', 'advanced', 'custom')),
  language TEXT NOT NULL CHECK (language IN ('zh-TW', 'en', 'es', 'vi')),

  -- Results
  user_answers JSONB NOT NULL,        -- { "BLUE": 5, "ORANGE": 3, ... }
  correct_answers JSONB NOT NULL,     -- { "BLUE": 5, "ORANGE": 4, ... }
  accuracy_percent DECIMAL(5,2) NOT NULL CHECK (accuracy_percent >= 0 AND accuracy_percent <= 100),
  completion_time_ms INTEGER,         -- Time to complete in milliseconds (optional)

  -- Timestamps
  completed_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- Index for efficient user queries
CREATE INDEX idx_puzzle_history_user_id ON puzzle_history(user_id);
CREATE INDEX idx_puzzle_history_completed_at ON puzzle_history(completed_at DESC);
CREATE INDEX idx_puzzle_history_user_completed ON puzzle_history(user_id, completed_at DESC);

-- Enable Row Level Security
ALTER TABLE puzzle_history ENABLE ROW LEVEL SECURITY;

-- RLS Policy: Users can only see their own history
CREATE POLICY "Users can view own puzzle history"
  ON puzzle_history
  FOR SELECT
  USING (auth.uid() = user_id);

-- RLS Policy: Users can only insert their own history
CREATE POLICY "Users can insert own puzzle history"
  ON puzzle_history
  FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- RLS Policy: Users can delete their own history
CREATE POLICY "Users can delete own puzzle history"
  ON puzzle_history
  FOR DELETE
  USING (auth.uid() = user_id);

-- =============================================
-- Optional: User preferences table
-- =============================================
CREATE TABLE user_preferences (
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,

  -- Display preferences
  preferred_language TEXT DEFAULT 'en' CHECK (preferred_language IN ('zh-TW', 'en', 'es', 'vi')),
  preferred_difficulty TEXT DEFAULT 'standard' CHECK (preferred_difficulty IN ('accessible', 'standard', 'advanced', 'custom')),
  preferred_spacing TEXT DEFAULT 'normal' CHECK (preferred_spacing IN ('compact', 'normal', 'relaxed', 'spacious')),
  sound_enabled BOOLEAN DEFAULT TRUE,

  -- Custom difficulty settings (when difficulty = 'custom')
  custom_grid_size INTEGER DEFAULT 4 CHECK (custom_grid_size >= 1 AND custom_grid_size <= 8),
  custom_color_count INTEGER DEFAULT 4 CHECK (custom_color_count >= 2 AND custom_color_count <= 8),
  custom_congruence INTEGER DEFAULT 12 CHECK (custom_congruence >= 0 AND custom_congruence <= 100),

  -- Timestamps
  updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- Enable Row Level Security
ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;

-- RLS Policies for user_preferences
CREATE POLICY "Users can view own preferences"
  ON user_preferences FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own preferences"
  ON user_preferences FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own preferences"
  ON user_preferences FOR UPDATE
  USING (auth.uid() = user_id);

-- =============================================
-- Helper function: Auto-create preferences on signup
-- =============================================
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO user_preferences (user_id)
  VALUES (NEW.id)
  ON CONFLICT (user_id) DO NOTHING;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger: Create preferences when user signs up
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION handle_new_user();
