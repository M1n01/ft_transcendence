import eslint from "@eslint/js";

export default [
  eslint.configs.recommended,
  {
    files: ['ft_trans/**/*.{js,jsx}'],
    ignores: ['node_modules'],
  },
];
