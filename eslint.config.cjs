module.exports = {
  rules: {
    indent: ['error', 2],
    quotes: ['error', 'single'],
  },
  extends: ['prettier'],
  include: [
    'src/**/*.js',
    'src/**/*.jsx',
  ],
  exclude: ['node_modules'],

};
