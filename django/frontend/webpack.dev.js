//import path from 'path';
import common from './webpack.common.js';
//import { fileURLToPath } from 'url';
import { merge } from 'webpack-merge';
//import webpack from 'webpack';

//const __filename = fileURLToPath(import.meta.url);
//const __dirname = path.dirname(__filename);
// devtool refer:https://webpack.js.org/configuration/devtool/

export default merge(common, {
  mode: 'development',
  output: {
    publicPath: 'http://localhost:3000/frontend/webpack_bundles/',
  },
  //watchOptions: {
  //aggregateTimeout: 100, // リビルドのディレイ時間
  //poll: 500, // ポーリングの間隔
  //ignored: /node_modules/, // 監視から除外するディレクトリ
  //},
  devtool: 'eval',
  devServer: {
    hot: true,
    compress: true, // gzip圧縮を有効化
    historyApiFallback: true,
    host: '0.0.0.0',
    port: 3000,
    headers: { 'Access-Control-Allow-Origin': '*' },
    watchFiles: {
      paths: ['src/**/*'], // 監視するファイルを指定
      options: {
        ignored: /node_modules/, // node_modulesを無視
        poll: true,
      },
    },
  },
  cache: {
    type: 'filesystem', // ファイルシステムキャッシュを使用
  },
  optimization: {
    splitChunks: {
      chunks: 'all', // コード分割を有効化
    },
  },
});
