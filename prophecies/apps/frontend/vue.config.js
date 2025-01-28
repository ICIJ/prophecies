const BundleTracker = require('webpack-bundle-tracker')
const { join } = require('path')

const resolve = (filepath) => join(__dirname, filepath)

module.exports = {
  configureWebpack: {
    devtool: 'source-map'
  },
  lintOnSave: false,
  runtimeCompiler: process.env.NODE_ENV === 'test',
  // Temporary workarround for map file not being created
  // @see https://github.com/django-webpack/django-webpack-loader/issues/280#issuecomment-871447482
  productionSourceMap: false,
  publicPath: process.env.NODE_ENV === 'production' ? 'static/' : '/',
  devServer: {
    port: 9009,
    proxy: {
      '^/': {
        target: 'http://0.0.0.0:8008',
        headers: {
          'Access-Control-Allow-Origin': ['*']
        },
        hotOnly: true,
        xfwd: true,
        watchOptions: {
          poll: 1000
        }
      }
    }
  },
  chainWebpack: (config) => {
    // Resource loader configuration:
    // 4 named rules must include this loader
    ;['vue', 'vue-modules', 'normal', 'normal-modules'].forEach((rule) => {
      config.module
        .rule('scss')
        .oneOf(rule)
        .use('sass-resources-loader')
        .loader('sass-resources-loader')
        .options({
          resources: [resolve('src/utils/_settings.scss')]
        })
    })

    // Aliases configuration
    config.resolve.alias
      .set('images', resolve('src/assets/images'))
      .set('node_modules', resolve('node_modules'))
      .set('tests', resolve('tests'))
      .set('__STATIC__', 'static')

    // Configure the BundleTracker to generate a `webpack-stats.json`.
    // This file is required by django-webpack-loader.
    config.plugin('BundleTracker').use(BundleTracker, [{ filename: 'webpack-stats.json', path: './dist' }])
  }
}
