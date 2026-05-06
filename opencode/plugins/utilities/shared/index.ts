/**
 * Shared utilities for OpenCode plugins.
 *
 * Import individual modules for tree-shaking:
 *   import { endpointFor } from "../utilities/shared/providers";
 *   import { scheduleCallback } from "../utilities/shared/callbacks";
 *
 * Or import from the barrel:
 *   import { endpointFor, scheduleCallback } from "../utilities/shared";
 */

export * from "./providers";
export * from "./callbacks";
