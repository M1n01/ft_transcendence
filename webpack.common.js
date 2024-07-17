import path from 'path';
import { fileURLToPath } from 'url';
import BundleTracker from 'webpack-bundle-tracker';
import MiniCssExtractPlugin from 'mini-css-extract-plugin';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default {
  entry: './ft_trans/spa/static/spa/js/index.js',
  output: {
    path: __dirname + '/ft_trans/assets/webpack_bundles',
    filename: '[name]-[hash].js',
  },
  plugins: [
    new BundleTracker({
      path: path.resolve(__dirname, 'ft_trans', 'assets'),
      filename: 'webpack-stats.json',
    }),
    new MiniCssExtractPlugin(),
  ],
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
      {
        test: /\.css$/,
        use: [MiniCssExtractPlugin.loader, 'css-loader'],
      },
    ],
  },
  resolve: {
    extensions: ['.js'],
    alias: {
      '@': path.resolve(__dirname, 'ft_trans/spa/static/spa/js'),
      '~': __dirname,
    },
  },
};
