/**
 * CORS Headers for Edge Functions
 *
 * Usage:
 *   import { corsHeaders } from "../_shared/cors.ts"
 *
 *   // Handle preflight
 *   if (req.method === 'OPTIONS') {
 *     return new Response('ok', { headers: corsHeaders })
 *   }
 *
 *   // Include in response
 *   return new Response(data, { headers: { ...corsHeaders, ... } })
 */

export const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers":
    "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
};
