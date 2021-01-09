var path = require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  context: __dirname,
  mode: 'development',
  entry: {
    meeting: './aalondon/static/js/MeetingApp.js',
    meetingsearch: './aalondon/static/js/MeetingSearch.js',
    onlinemeetingsearch: './aalondon/static/js/OnlineMeetingSearch.js',
    meetingform:'./aalondon/static/js/MeetingForm.js',



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
    },]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx']
  },



};
