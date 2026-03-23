// ESLint flat config for TypeScript QC
// Matches Codacy's plugin suite: @typescript-eslint, promise, fp, @lwc/lwc

import tsParser from '@typescript-eslint/parser';
import tsPlugin from '@typescript-eslint/eslint-plugin';
import promisePlugin from 'eslint-plugin-promise';
import fpPlugin from 'eslint-plugin-fp';
import lwcPlugin from '@lwc/eslint-plugin-lwc';

export default [
  {
    files: ['**/*.ts', '**/*.tsx'],
    ignores: ['node_modules/**', 'dist/**', 'coverage/**', '.venv/**'],
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module',
        // projectService: true uses TypeScript's project service, which handles
        // files not explicitly listed in tsconfig.json without a hard parse error.
        projectService: true,
        tsconfigRootDir: process.cwd(),
      },
    },
    plugins: {
      '@typescript-eslint': tsPlugin,
      promise: promisePlugin,
      fp: fpPlugin,
      '@lwc/lwc': lwcPlugin,
    },
    rules: {
      // @typescript-eslint full suite
      '@typescript-eslint/no-unsafe-assignment': 'error',
      '@typescript-eslint/no-unsafe-call': 'error',
      '@typescript-eslint/no-unsafe-member-access': 'error',
      '@typescript-eslint/no-unsafe-return': 'error',
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/no-floating-promises': 'error',
      '@typescript-eslint/no-misused-promises': 'error',
      '@typescript-eslint/await-thenable': 'error',
      '@typescript-eslint/no-unnecessary-type-assertion': 'error',
      '@typescript-eslint/prefer-nullish-coalescing': 'error',
      '@typescript-eslint/prefer-optional-chain': 'error',
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],

      // eslint-plugin-promise
      'promise/always-return': 'error',
      'promise/no-return-wrap': 'error',
      'promise/param-names': 'error',
      'promise/catch-or-return': 'error',
      'promise/no-native': 'error',
      // Nesting/callback rules: Codacy does not report these so don't fail locally.
      'promise/no-nesting': 'off',
      'promise/no-promise-in-callback': 'off',
      'promise/no-callback-in-promise': 'off',

      // eslint-plugin-fp (functional programming)
      // fp/no-nil: every function must end with an explicit return statement,
      // so it never implicitly returns undefined. Codacy enforces this.
      'fp/no-nil': 'error',
      'fp/no-this': 'warn',
      'fp/no-mutating-assign': 'error',
      'fp/no-mutating-methods': 'off', // too strict for most codebases
      // fp/no-let: disabled — Codacy does not run it, and enabling it here
      // conflicts with the pattern required to satisfy fp/no-nil in try/catch contexts.

      // @lwc/lwc (Lightning Web Components)
      // Codacy's LWC plugin forbids async/await; all async code must use .then() chains.
      '@lwc/lwc/no-async-await': 'error',
      '@lwc/lwc/no-for-of': 'off', // biome requires for...of
    },
  },
  {
    // Test files: relax LWC and fp rules. Async/await and void-returning callbacks
    // are idiomatic in test suites (bun:test, jest, etc.) and pre-exist in most PRs.
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
    },
  },
];
