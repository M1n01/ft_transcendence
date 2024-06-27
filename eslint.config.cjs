module.exports = {
  extends: [
    'eslint:recommended',
    'prettier',
  ],
  include: [
    'ft_trans/**/*.js',
    'ft_trans/**/*.jsx',
  ],
  exclude: ['node_modules'],
};
