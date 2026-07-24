// Shared browser Supabase client for the HomeTogether Hire marketplace.
// The anon (public) key is safe to ship in the page; Row Level Security is
// what actually protects the data. Paste your project's anon key below.
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

// NEW dedicated HomeTogether Hire project (NOT the Caring Companions hub project).
// Both come from the new project's Dashboard -> Project Settings -> API.
export const SUPABASE_URL = 'https://lrlczrpehjpncqixubuk.supabase.co';
export const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxybGN6cnBlaGpwbmNxaXh1YnVrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODQ2Njc3ODYsImV4cCI6MjEwMDI0Mzc4Nn0.I5kHlMyXotpJ4uhRFExdq7wT1u2jQou09fVpNWR-Uww';

export const sb = createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {
  auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true },
});

export const isConfigured = () =>
  SUPABASE_ANON_KEY.indexOf('__PASTE') !== 0 && SUPABASE_URL.indexOf('__PASTE') !== 0;

export function esc(t) {
  return String(t == null ? '' : t)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
