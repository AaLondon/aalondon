var path = require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  context: __dirname,
  mode: 'development',
  entry: {
    meeting: './aalondon/static/js/MeetingApp.js',


  }

  ,
  output: {
    path: path.resolve('./aalondon/static/bundles/'),
    filename: "[name]-[hash].js",
  },

  plugins: [
    new BundleTracker({
      filename: './webpack-stats.json'
    }),
  ],
  module: {
    rules: [{
      test: /\.js$/,
      exclude: /node_modules/,
      loader: 'babel-loader',
      options: {
        presets: ['@babel/preset-env',
          '@babel/react', {
            'plugins': ['@babel/plugin-proposal-class-properties']
          }
        ]
      }
    }]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx']
  },



};