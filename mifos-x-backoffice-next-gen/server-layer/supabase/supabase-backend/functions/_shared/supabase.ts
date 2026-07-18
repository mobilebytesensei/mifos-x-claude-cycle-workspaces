/**
 * Supabase Client Utilities for Edge Functions
 *
 * Two client types:
 * 1. supabaseAdmin - Service role, bypasses RLS (use for server operations)
 * 2. createUserClient - Anon key with user JWT (respects RLS)
 */

import { createClient, SupabaseClient } from "https://esm.sh/@supabase/supabase-js@2";

/**
 * Admin client with service role key.
 * Bypasses Row Level Security - use carefully!
 *
 * Usage:
 *   import { supabaseAdmin } from "../_shared/supabase.ts"
 *   const { data } = await supabaseAdmin.from('table').select()
 */
export const supabaseAdmin: SupabaseClient = createClient(
  Deno.env.get("SUPABASE_URL") ?? "",
  Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? ""
);

/**
 * Create a user-scoped client that respects RLS.
 * Pass the Authorization header from the request.
 *
 * Usage:
 *   import { createUserClient } from "../_shared/supabase.ts"
 *
 *   const authHeader = req.headers.get('Authorization')!
 *   const supabase = createUserClient(authHeader)
 *   const { data: { user } } = await supabase.auth.getUser()
 */
export const createUserClient = (authHeader: string): SupabaseClient => {
  return createClient(
    Deno.env.get("SUPABASE_URL") ?? "",
    Deno.env.get("SUPABASE_ANON_KEY") ?? "",
    {
      global: {
        headers: { Authorization: authHeader },
      },
    }
  );
};

/**
 * Get authenticated user from request.
 * Returns null if not authenticated.
 *
 * Usage:
 *   import { getUser } from "../_shared/supabase.ts"
 *
 *   const user = await getUser(req)
 *   if (!user) return errorResponse('Unauthorized', 401)
 */
export const getUser = async (req: Request) => {
  const authHeader = req.headers.get("Authorization");
  if (!authHeader) return null;

  const supabase = createUserClient(authHeader);
  const {
    data: { user },
    error,
  } = await supabase.auth.getUser();

  if (error || !user) return null;
  return user;
};
