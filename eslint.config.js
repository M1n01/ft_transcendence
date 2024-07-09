
import eslint from "@eslint/js";
import globals from "globals"

export default [
  eslint.configs.recommended,
  {
    files: ['ft_trans/**/*.js', 'ft_trans/**/*.jsx'],
    ignores: ['node_modules', 'ft_trans/public/'],
    languageOptions: {
        globals: {
            ...globals.browser,
            ...globals.node
        },
    },
    rules: {
      'no-console': ['error', { allow: ['warn', 'error'] }],
    },
  },
];
