var path = require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
  context: __dirname,
  mode: 'development',
  entry: {
    meeting: './aalondon/static/js/MeetingApp.js',
    meetingsearch: './aalondon/static/js/MeetingSearch.js',
    onlinemeetingsearch: './aalondon/static/js/OnlineMeetingSearch.js',
    meetingformselector:'./aalondon/static/js/MeetingFormSelector.js',



  }

  ,
  output: {
    path: path.resolve('./aalondon/static/bundles/'),
    filename: "[name]-[hash].js",
    publicPath: ''
  },

  plugins: [
    new BundleTracker({
      filename: './webpack-stats.json'
    }),
    new MiniCssExtractPlugin({
      // Options similar to the same options in webpackOptions.output
      // both options are optional
      filename: '[name]-[hash].css',
      }),
  ],
  module: {
    rules: [{
      test: /\.js$/,
      
      exclude: /node_modules/,
      loader:   'babel-loader',
      
      options: {
        presets: ['@babel/preset-env',
          '@babel/react', {
            'plugins': ['@babel/plugin-proposal-class-properties','@babel/transform-runtime']
          },
          
        ]
      }
    },
    {
      test: /\.(png|jpg|gif)$/,
      use: [
        {
          loader: 'file-loader',
          options: {
            name: '[name].[ext]',
            outputPath: 'images/',
            publicPath: ''

          }
        }
      ]
    },
    {
      test: /\.css$/i,
      use: [MiniCssExtractPlugin.loader, 'css-loader'],
    },]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx']
  },



};
