import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default {
  entry: './ft_trans/spa/static/spa/js/index.js',
  output: {
    path: __dirname + '/ft_trans/spa/static/dist',
    filename: 'bundle.js',
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        loader: 'babel-loader',
        options: {
          presets: ['@babel/preset-env', '@babel/preset-react'],
        },
      },
    ],
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'ft_trans/spa/static/spa/js'),
      '~': __dirname,
    },
  },
};
