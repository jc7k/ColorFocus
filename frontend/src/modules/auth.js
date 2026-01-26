/**
 * Authentication module.
 * Handles Supabase authentication with Google OAuth.
 */

import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm';
import { getUIText } from './ui.js';
import * as state from './state.js';

// ===========================================
// SUPABASE CONFIGURATION
// ===========================================
const SUPABASE_URL = 'YOUR_SUPABASE_PROJECT_URL';
const SUPABASE_ANON_KEY = 'YOUR_SUPABASE_ANON_KEY';

// Initialize Supabase client (only if configured)
const supabaseConfigured = SUPABASE_URL !== 'YOUR_SUPABASE_PROJECT_URL';
export const supabase = supabaseConfigured ? createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {
  auth: {
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: true,
    storage: window.sessionStorage,
    flowType: 'pkce'
  }
}) : null;

// ===========================================
// AUTH FUNCTIONS
// ===========================================

/**
 * Sign in with Google OAuth
 */
export async function signInWithGoogle() {
  if (!supabase) {
    console.warn('Supabase not configured. Please set SUPABASE_URL and SUPABASE_ANON_KEY.');
    alert('Authentication not configured. Please contact the administrator.');
    return;
  }
  try {
    const { data, error } = await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: window.location.origin + window.location.pathname
      }
    });
    if (error) {
      console.error('Sign in error:', error.message);
      alert(getUIText('auth_error_signin') || 'Sign in failed. Please try again.');
    }
  } catch (err) {
    console.error('Sign in failed:', err);
    alert(getUIText('auth_error_signin') || 'Sign in failed. Please try again.');
  }
}

/**
 * Sign out
 */
export async function signOut() {
  if (!supabase) return;
  try {
    const { error } = await supabase.auth.signOut();
    if (error) {
      console.error('Sign out error:', error.message);
      alert(getUIText('auth_error_signout') || 'Sign out failed. Please try again.');
    }
  } catch (err) {
    console.error('Sign out failed:', err);
    alert(getUIText('auth_error_signout') || 'Sign out failed. Please try again.');
  }
}

/**
 * Update UI based on auth state
 */
export function updateAuthUI(user) {
  const loginBtn = document.getElementById('loginBtn');
  const userInfo = document.getElementById('userInfo');
  const userName = document.getElementById('userName');
  const userAvatar = document.getElementById('userAvatar');

  if (user) {
    loginBtn.style.display = 'none';
    userInfo.style.display = 'flex';

    // Use display name or email
    const displayName = user.user_metadata?.full_name ||
                        user.user_metadata?.name ||
                        user.email?.split('@')[0] ||
                        'User';
    userName.textContent = displayName;

    // Use avatar URL or keep placeholder
    const avatarUrl = user.user_metadata?.avatar_url ||
                      user.user_metadata?.picture;
    if (avatarUrl) {
      userAvatar.src = avatarUrl;
    }
    userAvatar.alt = `${displayName}'s avatar`;
  } else {
    loginBtn.style.display = 'flex';
    userInfo.style.display = 'none';
  }
}

/**
 * Initialize auth state listener
 */
export function initAuthListener() {
  if (!supabase) {
    // Hide auth UI elements when not configured
    document.getElementById('authSection')?.classList.add('hidden');
    return;
  }

  supabase.auth.onAuthStateChange((event, session) => {
    state.setCurrentUser(session?.user || null);
    updateAuthUI(state.currentUser);
  });
}

/**
 * Check for existing session on page load
 */
export async function checkExistingSession() {
  if (!supabase) return;

  try {
    const { data: { session }, error } = await supabase.auth.getSession();
    if (error) {
      console.error('Session check error:', error.message);
      return;
    }
    if (session?.user) {
      state.setCurrentUser(session.user);
      updateAuthUI(state.currentUser);
    }
  } catch (err) {
    console.error('Session check failed:', err);
  }
}

/**
 * Save puzzle attempt to history
 */
export async function savePuzzleHistory(userAnswers, accuracy) {
  if (!supabase || !state.currentUser) return;

  const historyEntry = {
    user_id: state.currentUser.id,
    seed: state.currentSeed,
    grid_size: state.currentGridSize,
    color_count: state.currentColorCount,
    congruent_count: state.currentCongruentCount,
    difficulty: state.currentDifficulty,
    language: state.currentLanguage,
    user_answers: userAnswers,
    correct_answers: state.correctAnswers,
    accuracy: accuracy,
    completed_at: new Date().toISOString()
  };

  try {
    const { error } = await supabase
      .from('puzzle_history')
      .insert(historyEntry);

    if (error) {
      console.error('Error saving puzzle history:', error.message);
    }
  } catch (err) {
    console.error('Failed to save puzzle history:', err);
  }
}

/**
 * Get user's puzzle history
 */
export async function getPuzzleHistory(limit = 10) {
  if (!supabase || !state.currentUser) return [];

  try {
    const { data, error } = await supabase
      .from('puzzle_history')
      .select('*')
      .eq('user_id', state.currentUser.id)
      .order('completed_at', { ascending: false })
      .limit(limit);

    if (error) {
      console.error('Error fetching puzzle history:', error.message);
      return [];
    }

    return data || [];
  } catch (err) {
    console.error('Failed to fetch puzzle history:', err);
    return [];
  }
}
