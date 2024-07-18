import path from 'path';
import { fileURLToPath } from 'url';
import BundleTracker from 'webpack-bundle-tracker';
import MiniCssExtractPlugin from 'mini-css-extract-plugin';
import { autoprefixer } from 'autoprefixer';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default {
  entry: './spa/static/spa/js/index.js',
  output: {
    path: __dirname + '/assets/webpack_bundles',
    filename: '[name]-[hash].js',
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
          presets: ['@babel/preset-env', '@babel/preset-react'],
        },
      },
      {
        test: /\.css$/,
        use: [MiniCssExtractPlugin.loader, 'css-loader'],
      },
      {
        test: /\.(scss)$/,
        use: [
          {
            // Adds CSS to the DOM by injecting a `<style>` tag
            loader: 'style-loader',
          },
          {
            // Interprets `@import` and `url()` like `import/require()` and will resolve them
            loader: 'css-loader',
          },
          {
            // Loader for webpack to process CSS with PostCSS
            loader: 'postcss-loader',
            options: {
              postcssOptions: {
                plugins: () => [autoprefixer],
              },
            },
          },
          {
            // Loads a SASS/SCSS file and compiles it to CSS
            loader: 'sass-loader',
          },
        ],
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
