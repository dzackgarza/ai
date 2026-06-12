// ESLint flat config for TypeScript QC

import tsPlugin from "@typescript-eslint/eslint-plugin";
import tsParser from "@typescript-eslint/parser";
import fpPlugin from "eslint-plugin-fp";
import promisePlugin from "eslint-plugin-promise";
import reactHooksPlugin from "eslint-plugin-react-hooks";
import reactRefreshPlugin from "eslint-plugin-react-refresh";
import globals from "globals";

export default [
  // Global ignores: apply before any rule config
  {
    ignores: [
      "**/env.d.ts",
      "**/node_modules/**",
      "**/.venv/**",
      "**/__pycache__/**",
      "**/dist/**",
      "**/build/**",
      "**/coverage/**",
      "**/_ci-support/**",
      "**/codeql-db/**",
      "**/@girs/**",
      "**/__stubs__/**",
      "**/external/**",
      "**/target/**",
      "**/*.bak/**",
      "**/.git/**",
      "**/.next/**",
      "**/.lake/**",
      "**/.worktrees/**",
      "**/vendor/**",
      "**/third_party/**",
      "**/venv/**",
    ],
  },
  {
    files: ["**/*.ts", "**/*.tsx"],
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        ecmaVersion: "latest",
        sourceType: "module",
        // projectService: true uses TypeScript's project service, which handles
        // files not explicitly listed in tsconfig.json without a hard parse error.
        projectService: true,
        tsconfigRootDir: process.cwd(),
      },
      globals: {
        ...globals.node,
      },
    },
    plugins: {
      "@typescript-eslint": tsPlugin,
      promise: promisePlugin,
      fp: fpPlugin,
      "react-hooks": reactHooksPlugin,
      "react-refresh": reactRefreshPlugin,
    },
    rules: {
      // @typescript-eslint full suite
      "@typescript-eslint/no-unsafe-assignment": "error",
      "@typescript-eslint/no-unsafe-call": "error",
      "@typescript-eslint/no-unsafe-member-access": "error",
      "@typescript-eslint/no-unsafe-return": "error",
      "@typescript-eslint/no-explicit-any": "error",
      "@typescript-eslint/no-floating-promises": "error",
      "@typescript-eslint/no-misused-promises": "error",
      "@typescript-eslint/await-thenable": "error",
      "@typescript-eslint/no-unnecessary-type-assertion": "error",
      "@typescript-eslint/prefer-nullish-coalescing": "error",
      "@typescript-eslint/prefer-optional-chain": "error",
      "@typescript-eslint/no-unused-vars": ["error", { argsIgnorePattern: "^_" }],

      // eslint-plugin-promise
      "promise/always-return": "error",
      "promise/no-return-wrap": "error",
      "promise/param-names": "error",
      "promise/catch-or-return": "error",
      "promise/no-native": "off",
      // Nesting/callback rules are intentionally off to avoid over-constraining
      // promise composition in application code.
      "promise/no-nesting": "off",
      "promise/no-promise-in-callback": "off",
      "promise/no-callback-in-promise": "off",

      // eslint-plugin-fp (functional programming)
      // fp/no-nil: every function must end with an explicit return statement,
      // so it never implicitly returns undefined.
      "fp/no-nil": "error",
      "fp/no-this": "warn",
      "fp/no-mutating-assign": "error",
      "fp/no-mutating-methods": "off", // too strict for most codebases
      // fp/no-let: disabled because global QC permits local mutable bindings
      // when they make state transitions explicit.

      // eslint-plugin-react-hooks (React)
      "react-hooks/rules-of-hooks": "error",
      "react-hooks/exhaustive-deps": "warn",

      // eslint-plugin-react-refresh (component export enforcement)
      "react-refresh/only-export-components": ["warn", { allowConstantExport: true }],
    },
  },
  {
    // Test files: relax LWC and fp rules. Async/await and void-returning callbacks
    // are idiomatic in test suites (bun:test, jest, etc.) and pre-exist in most PRs.
    // This block comes LAST so it overrides the main config above.
    files: ["tests/**/*.ts", "**/*.test.ts", "**/*.spec.ts"],
    rules: {
      "fp/no-nil": "off",
      "@typescript-eslint/no-floating-promises": "off",
      "@typescript-eslint/no-unsafe-call": "off",
      "@typescript-eslint/no-unsafe-member-access": "off",
      "@typescript-eslint/no-unsafe-assignment": "off",
      "@typescript-eslint/prefer-nullish-coalescing": "off",
      "promise/always-return": "off",
      "promise/catch-or-return": "off",
      "promise/no-native": "off",
      "no-undef": "off",
    },
  },
  {
    // AGS/GJS files: Gtk runtime types cannot be statically resolved by TSC.
    // Parse without TypeScript project service (these files are excluded from
    // tsconfig because AGS module types are unresolvable by tsc).
    files: ["**/*.tsx"],
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        ecmaVersion: "latest",
        sourceType: "module",
        projectService: false,
      },
      globals: {
        ...globals.node,
      },
    },
    plugins: {
      "@typescript-eslint": tsPlugin,
      fp: fpPlugin,
    },
    rules: {
      // Disable all type-aware rules — .tsx files have no project service
      "@typescript-eslint/no-unsafe-call": "off",
      "@typescript-eslint/no-unsafe-member-access": "off",
      "@typescript-eslint/no-unsafe-assignment": "off",
      "@typescript-eslint/no-unsafe-return": "off",
      "@typescript-eslint/no-floating-promises": "off",
      "@typescript-eslint/no-misused-promises": "off",
      "@typescript-eslint/await-thenable": "off",
      "@typescript-eslint/no-unnecessary-type-assertion": "off",
      "@typescript-eslint/prefer-nullish-coalescing": "off",
      "@typescript-eslint/prefer-optional-chain": "off",
      "fp/no-nil": "off",
      "fp/no-this": "warn",
    },
  },
];
