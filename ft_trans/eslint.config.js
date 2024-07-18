import eslint from '@eslint/js';
import globals from 'globals';

export default [
  eslint.configs.recommended,
  {
    files: ['spa/**/*.{js,jsx}'],
    ignores: ['node_modules', 'public/'],
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.es2021,
      },
    },
    rules: {
      'no-unused-vars': ['error', { varsIgnorePattern: '^sendRequestAsForm$' }],
    },
  },
];
