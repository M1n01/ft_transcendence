import eslint from '@eslint/js';
import globals from 'globals';

export default [
  eslint.configs.recommended,
  {
    files: ['django/frontend/**/*.{js,jsx}', 'eth/**/*.{js,jsx}'],
    ignores: ['node_modules', 'django/public/', 'db_volume'],
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.es2021,
      },
    },
    rules: {
      'no-unused-vars': ['error'],
    },
  },
];
