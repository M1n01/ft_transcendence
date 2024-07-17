import path from 'path';
import { fileURLToPath } from 'url';
//import webpack from 'webpack';
import BundleTracker from 'webpack-bundle-tracker';
import MiniCssExtractPlugin from 'mini-css-extract-plugin';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default {
  mode: 'development',
  //context: path.resolve(__dirname, 'ft_trans/'),
  entry: './ft_trans/assets/js/index',
  //entry: './ft_trans/spa/static/spa/js/index.js',
  //entry: './ft_trans/spa/static/spa/js/index.js',
  output: {
    path: __dirname + '/ft_trans/assets/webpack_bundles',
    //filename: 'bundle.js',
    //path: path.resolve(__dirname, 'ft_trans', 'assets', 'webpack_bundles'),
    publicPath: 'http://localhost:3000/frontend/webpack_bundles/',
    //publicPath: 'auto',
    filename: '[name]-[hash].js',
  },
  devtool: 'source-map',
  devServer: {
    hot: true,
    historyApiFallback: true,
    host: 'localhost',
    port: 3000,
    // Allow CORS requests from the Django dev server domain:
    headers: { 'Access-Control-Allow-Origin': '*' },
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
