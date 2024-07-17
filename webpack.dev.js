import path from 'path';
import common from './webpack.common.js';
import { fileURLToPath } from 'url';
import { merge } from 'webpack-merge';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default merge(common, {
  mode: 'development',
  output: {
    publicPath: 'http://localhost:3000/frontend/webpack_bundles/',
  },
  devtool: 'source-map',
  devServer: {
    hot: true,
    historyApiFallback: true,
    host: 'localhost',
    port: 3000,
    headers: { 'Access-Control-Allow-Origin': '*' },
  },
});
