import eslint from '@eslint/js';
import globals from 'globals';

export default [
  eslint.configs.recommended,
  {
    files: ['ft_trans/**/*.{js,jsx}'],
    ignores: ['node_modules', 'ft_trans/public/'],
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
