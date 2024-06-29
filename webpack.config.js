const path = require('path');

module.exports = {
  ...
  resolve: {
    alias: {
      '@bar': path.resolve(__dirname, 'src/foo/bar')
    }
  }
};
