import path from 'path';
import { fileURLToPath } from 'url';
import BundleTracker from 'webpack-bundle-tracker';
import MiniCssExtractPlugin from 'mini-css-extract-plugin';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

console.log("__filename:" + __filename );
console.log("__dirname:" + __dirname );

export default {
  entry: __dirname + '/spa/static/spa/js/index',
  output: {
    path: __dirname + '/assets/webpack_bundles',
    filename: '[name]-[contenthash].js',

  },
  plugins: [
    new BundleTracker({
      path: path.resolve(__dirname, 'assets'),
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
          presets: ['@babel/preset-env'],
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
      '@': path.resolve(__dirname, 'spa/static/spa/js'),
      '~': __dirname,
    },
  },
};
