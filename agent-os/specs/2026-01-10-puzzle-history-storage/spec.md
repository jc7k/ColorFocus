# Puzzle History Storage

## Overview

Store completed puzzles with timestamps, user answers, and accuracy for each authenticated user. This enables tracking progress over time.

## User Stories

1. As an authenticated user, I want my puzzle attempts saved automatically so I can track my progress
2. As a user, I want to see that my attempt was saved after checking answers

## Technical Design

### Database Schema (Supabase)

Table: `puzzle_attempts`

| Column | Type | Description |
|--------|------|-------------|
| id | uuid | Primary key (auto-generated) |
| user_id | uuid | References auth.users(id) |
| created_at | timestamptz | When puzzle was completed |
| seed | integer | Puzzle seed for reproducibility |
| grid_size | integer | Grid dimension (3-8) |
| color_count | integer | Number of colors used |
| difficulty | text | Difficulty tier (accessible/standard/advanced/custom) |
| language | text | Language used (zh-TW/english/spanish/vietnamese) |
| congruence_percent | decimal | Congruence percentage setting |
| user_answers | jsonb | User's submitted answers {color: count} |
| correct_answers | jsonb | Actual correct answers {color: count} |
| correct_count | integer | Number of colors answered correctly |
| total_colors | integer | Total colors in puzzle |
| accuracy_percent | integer | Percentage correct (0-100) |
| total_off | integer | Sum of absolute differences |

### Row Level Security (RLS)

- Users can only INSERT their own attempts
- Users can only SELECT their own attempts
- No UPDATE or DELETE allowed (immutable history)

### Frontend Changes

1. Add `savePuzzleAttempt()` function after `checkAnswers()`
2. Only save for authenticated users
3. Show subtle confirmation when saved
4. Handle errors gracefully (don't block UX)

## Acceptance Criteria

- [x] Puzzle attempts are saved to Supabase after checking answers
- [x] Only authenticated users' attempts are saved
- [x] All puzzle metadata is stored correctly
- [x] RLS policies prevent unauthorized access
- [x] Graceful error handling if save fails
