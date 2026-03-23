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
        project: './tsconfig.json',
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
      'promise/no-nesting': 'warn',
      'promise/no-promise-in-callback': 'warn',
      'promise/no-callback-in-promise': 'warn',

      // eslint-plugin-fp (functional programming)
      'fp/no-return-void': 'error',
      'fp/no-let': 'error',
      'fp/no-this': 'warn',
      'fp/no-mutating-assign': 'error',
      'fp/no-mutating-methods': 'off', // too strict for most codebases

      // @lwc/lwc (Lightning Web Components)
      '@lwc/lwc/no-async-await': 'off', // conflicts with modern Node.js patterns
      '@lwc/lwc/no-for-of': 'off', // biome requires for...of
    },
  },
];
