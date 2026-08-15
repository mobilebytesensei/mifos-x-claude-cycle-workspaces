/**
 * Response Utilities for Edge Functions
 *
 * Consistent response format with CORS headers.
 */

import { corsHeaders } from "./cors.ts";

/**
 * Create a JSON response with CORS headers.
 *
 * Usage:
 *   import { jsonResponse } from "../_shared/response.ts"
 *   return jsonResponse({ success: true, data: items })
 */
export const jsonResponse = (data: unknown, status = 200): Response => {
  return new Response(JSON.stringify(data), {
    headers: { ...corsHeaders, "Content-Type": "application/json" },
    status,
  });
};

/**
 * Create an error response with CORS headers.
 *
 * Usage:
 *   import { errorResponse } from "../_shared/response.ts"
 *   return errorResponse('Not found', 404)
 */
export const errorResponse = (message: string, status = 400): Response => {
  return new Response(JSON.stringify({ error: message }), {
    headers: { ...corsHeaders, "Content-Type": "application/json" },
    status,
  });
};

/**
 * Handle CORS preflight request.
 *
 * Usage:
 *   import { handleCors } from "../_shared/response.ts"
 *   if (req.method === 'OPTIONS') return handleCors()
 */
export const handleCors = (): Response => {
  return new Response("ok", { headers: corsHeaders });
};

/**
 * Wrap handler with CORS and error handling.
 *
 * Usage:
 *   import { withHandler } from "../_shared/response.ts"
 *
 *   Deno.serve(withHandler(async (req) => {
 *     const data = await doSomething()
 *     return jsonResponse(data)
 *   }))
 */
export const withHandler = (
  handler: (req: Request) => Promise<Response>
): ((req: Request) => Promise<Response>) => {
  return async (req: Request): Promise<Response> => {
    // Handle CORS preflight
    if (req.method === "OPTIONS") {
      return handleCors();
    }

    try {
      return await handler(req);
    } catch (error) {
      console.error("Handler error:", error);
      return errorResponse(
        error instanceof Error ? error.message : "Internal server error",
        500
      );
    }
  };
};
