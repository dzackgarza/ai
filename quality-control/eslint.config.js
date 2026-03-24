// ESLint flat config for TypeScript QC
//
// DESIGN: Local config must be STRICTER than Codacy, not merely matching it.
// That way anything passing locally is guaranteed to pass Codacy.
//
// Base: @typescript-eslint/flat/strict-type-checked — the maximum preset,
// a strict superset of every @typescript-eslint rule Codacy could run.
// Additional plugins: promise, fp (functional), @lwc/lwc (no-async-await).

import tsPlugin from '@typescript-eslint/eslint-plugin';
import promisePlugin from 'eslint-plugin-promise';
import fpPlugin from 'eslint-plugin-fp';
import lwcPlugin from '@lwc/eslint-plugin-lwc';
import globals from 'globals';

export default [
  // Global ignores: apply before any rule config
  { ignores: ['node_modules/**', 'dist/**', 'coverage/**', '.venv/**', '_ci-support/**'] },

  // Spread the strictest @typescript-eslint preset — superset of anything Codacy runs.
  // This registers the @typescript-eslint parser, plugin, and all strict-type-checked rules.
  ...tsPlugin.configs['flat/strict-type-checked'],

  // Layer additional plugins and overrides on top of the base preset.
  {
    files: ['**/*.ts', '**/*.tsx'],
    languageOptions: {
      parserOptions: {
        // projectService handles files not explicitly listed in tsconfig without hard errors.
        projectService: true,
        tsconfigRootDir: process.cwd(),
      },
      // Codacy's LWC environment excludes Promise from globals so no-undef fires on
      // Promise.resolve() and : Promise<X> annotations. Replicate that behavior locally.
      globals: {
        ...globals.node,
        Promise: 'off',
      },
    },
    plugins: {
      promise: promisePlugin,
      fp: fpPlugin,
      '@lwc/lwc': lwcPlugin,
    },
    rules: {
      // no-undef fires on Promise.resolve() etc. because Promise is removed from globals above.
      'no-undef': 'error',

      // eslint-plugin-promise: full enforcement
      'promise/always-return': 'error',
      'promise/no-return-wrap': 'error',
      'promise/param-names': 'error',
      'promise/catch-or-return': 'error',
      'promise/no-native': 'error',
      // Nesting/callback rules: Codacy does not report these.
      'promise/no-nesting': 'off',
      'promise/no-promise-in-callback': 'off',
      'promise/no-callback-in-promise': 'off',

      // eslint-plugin-fp: functional programming constraints
      // fp/no-nil: every function must end with an explicit return (never implicitly undefined).
      'fp/no-nil': 'error',
      'fp/no-this': 'warn',
      'fp/no-mutating-assign': 'error',
      'fp/no-mutating-methods': 'off',
      // fp/no-let disabled — conflicts with the let pattern required by fp/no-nil in try/catch.

      // no-confusing-void-expression (strict-type-checked) conflicts irresolvably with fp/no-nil:
      // the fix for one (add braces) breaks the other (no explicit return). fp/no-nil is the
      // stronger semantic guarantee so this stylistic rule is disabled.
      '@typescript-eslint/no-confusing-void-expression': 'off',

      // @lwc/lwc: no async/await — all async code must use .then() chains.
      '@lwc/lwc/no-async-await': 'error',
      '@lwc/lwc/no-for-of': 'off', // biome requires for...of
    },
  },

  {
    // Test files: relax LWC and fp rules. Async/await and void-returning callbacks
    // are idiomatic in test suites (bun:test, jest, etc.).
    // This block comes LAST so it overrides the main config above.
    files: ['tests/**/*.ts', '**/*.test.ts', '**/*.spec.ts'],
    rules: {
      '@lwc/lwc/no-async-await': 'off',
      'fp/no-nil': 'off',
      '@typescript-eslint/no-floating-promises': 'off',
      '@typescript-eslint/no-unsafe-call': 'off',
      '@typescript-eslint/no-unsafe-member-access': 'off',
      '@typescript-eslint/no-unsafe-assignment': 'off',
      '@typescript-eslint/prefer-nullish-coalescing': 'off',
      'promise/always-return': 'off',
      'promise/catch-or-return': 'off',
      'promise/no-native': 'off',
      'no-undef': 'off',
    },
  },
];
