/*!
 * Gruntfile
 * @author Regi Ellis
 */

/* jslint node: true */
/* jslint curly: false */

/*
    Grunt installation:
    -------------------
        npm install -g grunt-cli
        npm install -g grunt-init
        npm install -g browser-sync
        npm init (creates a `package.json` file)

    Project Dependencies:
    ---------------------
        npm install grunt --save-dev
        npm install grunt-cli --save-dev
        npm install load-grunt-tasks --save-dev
        npm install grunt-contrib-watch --save-dev
        npm install grunt-contrib-jshint --save-dev
        npm install grunt-contrib-uglify --save-dev
        npm install grunt-contrib-requirejs --save-dev
        npm install grunt-contrib-less --save-dev
        npm install grunt-contrib-imagemin --save-dev
        npm install grunt-contrib-htmlmin --save-dev
        npm install grunt-contrib-requirejs --save-dev
        npm install grunt-contrib-copy --save-dev
        npm install grunt-svgmin --save-dev
        npm install grunt-autoshot --save-dev
        npm install grunt-casperjs --save-dev
        npm install time-grunt --save-dev
        npm install grunt-jsbeautifier --save-dev
        npm install grunt-concurrent --save-dev
        npm install grunt-newer --save-dev
        npm install grunt-node-inspector --save-dev
        npm install grunt-browser-sync --save-dev

        Grunt Devtools extension for Chrome Developer Tools
        https://chrome.google.com/webstore/detail/grunt-devtools/fbiodiodggnlakggeeckkjccjhhjndnb?hl=en
        npm install grunt-devtools --save-dev

*/

'use strict';

module.exports = function(grunt) {

    // DISPLAYS THE ELAPSED EXECUTION TIME OF GRUNT TASKS
    require('time-grunt')(grunt);

    // DYNAMICALLY LOAD NPM TASKS
    require('load-grunt-tasks')(grunt);

    grunt.initConfig({
        pkg   : grunt.file.readJSON('package.json'),
        config: grunt.file.readJSON('config.json'),
        meta  : {
            projectName: '<%= pkg.name %>',
            basePath: '<%= config.baseDir %>',
            buildPath: '<%= config.buildPath %>',
            sourcePath: '<%= config.sourcePath %>',
            developUrl: '<%= config.develop_url %>',
            develop_port: '<%= config.develop_port %>'
        },

        tag: {
          banner: '/*!\n' +
                  ' * <%= config.name %>\n' +
                  ' * <%= config.title %>\n' +
                  ' * <%= config.url %>\n' +
                  ' * @author <%= config.author %>\n' +
                  ' * @version <%= config.version %>\n' +
                  ' * Copyright <%= config.copyright %> <%= config.name %>.  All Rights Reserved.\n' +
                  ' * Major Frameworks Req: <%= config.frameworks %>' +
                  ' */\n\n'
        },

        bower: {
          install: {
            options: {
                targetDir: '<%= meta.sourcePath %>',
                verbose: true,
                install: false
            }
          }
        },

        browserSync: {
            dev: {
                bsFiles: {
                    src : '<%= meta.buildPath %>styles/**/*.css %>'
                },
                options: {
                    proxy: '<%= meta.developUrl %>',
                    watchTask: true,
                    port: '<%= meta.develop_port %>'
                }
            }
        },

        concat: {
          options: {
            banner: '<%= tag.banner %>'
          },
          dist: {
            expand: false,
            src: ['<%= meta.sourcePath %>/scripts/libs/jquery/*.js', '<%= meta.sourcePath %>/scripts/libs/**/*.js'],
            dest: '<%= meta.sourcePath %>/scripts/core_libs.js',
            ext: '.js'
          }
        },

        concat_css: {
          dist: {
            options: {
              banner: '<%= tag.banner %>'
            },
            expand: false,
            src: ['<%= meta.sourcePath %>/styles/libs/**/*.css'],
            dest: '<%= meta.sourcePath %>/styles/core_libs.css',
            ext: '.css'
          }
        },

        autoprefixer: {
            dist: {
                options: {
                  browsers: ['last 2 versions', '> 1%', 'ie 8', 'bb 10', 'android 4', 'ios 7', 'safari 7']
                },
                expand: true,
                cwd: '<%= meta.buildPath %>styles/',
                src: ['**/*.css', '!libs/**/*.css'],
                dest: '<%= meta.buildPath %>styles',
                ext: '.css'
            }
        },

        jshint: {
            options: {
                jshintrc: '.jshintrc'
            },
            gruntfile: 'Gruntfile.js',
            files: ['<%= meta.buildPath %>scripts/**/*.js', '!<%= meta.buildPath %>scripts/libs/**/*.js', '!<%= meta.buildPath %>scripts/core_libs.js']
        },

        csso: {
            compress: {
                options: {
                    report: 'gzip',
                    restructure: true,
                    banner: '<%= tag.banner %>'
                },
                expand: true,
                cwd: '<%= meta.buildPath %>styles',
                src: ['**/*.css'],
                dest: '<%= meta.buildPath %>styles',
                ext: '.css'
            }
        },

        uglify: {
            general: {
                options: {
                    mangle: false,
                    compress: false,
                    preserveComments: 'all',
                    beautify: true
                },
                expand: true,
                files: {
                    '<%= meta.buildPath %>scripts/general.js': [
                        '<%= meta.sourcePath %>scripts/general.js',
                        // '<%= meta.sourcePath %>scripts/**/*.js',
                        // '!<%= meta.sourcePath %>scripts/core_libs.js',
                        // '!<%= meta.sourcePath %>scripts/config.js',
                        // '!<%= meta.sourcePath %>scripts/modules/**/*.js',
                        // '!<%= meta.sourcePath %>scripts/tests/**/*.js'
                    ]
                }
            }
        },

        requirejs: {
            compile: {
                options: {
                    baseUrl: '<%= meta.buildPath %>scripts',
                    mainConfigFile: '<%= meta.buildPath %>scripts/config.js',
                    dir: '<%= meta.buildPath %>scripts/',
                    fileExclusionRegExp: /^\.|node_modules|Gruntfile|\.md|package.json/,
                    // optimize: 'none',
                    modules: [
                        {
                            name: 'config'
                        }
                    ]
                }
            }
        },

        less: {
          dev: {
              options: {
                  compress: false,
                  dumpLineNumbers: false,
                  sourceMap: false,
                  banner: '<%= tag.banner %>'
                  // require: ['<%= meta.srcPath %>/url64.rb']
              },
              expand: true,
              cwd: '<%= meta.sourcePath %>/styles/',
              src: ['**/*.less', 'libs/**/*.less', 'modules/**/*.less', '!**/_*.less', '!partials/**/*.less', '!mixins/**/*.less'],
              dest: '<%= meta.buildPath %>styles',
              ext: '.css'
          },
          build: {
              options: {
                  compress: true,
                  dumpLineNumbers: 'comments',
                  sourceMap: false,
                  banner: '<%= tag.banner %>'
                  // require: ['<%= meta.srcPath %>/url64.rb']
              },
              expand: true,
              cwd: '<%= meta.sourcePath %>/styles/',
              src: ['**/*.less', 'libs/**/*.less', 'modules/**/*.less', '!**/_*.less', '!partials/**/*.less',  '!mixins/**/*.less'],
              dest: '<%= meta.buildPath %>styles',
              ext: '.css'
          },
          dist: {
              options: {
                  compress: true,
                  dumpLineNumbers: false,
                  sourceMap: false,
                  banner: '<%= tag.banner %>'
                  // require: ['<%= meta.srcPath %>/url64.rb']
              },
              expand: true,
              cwd: '<%= meta.sourcePath %>/styles/',
              src: ['**/*.less', 'libs/**/*.less', 'modules/**/*.less', '!**/_*.less', '!partials/**/*.less', '!mixins/**/*.less'],
              dest: '<%= meta.buildPath %>styles/',
              ext: '.css'
          }
        },
        copy: {
          fonts: {
            option : {},
            expand: true,
            cwd: '<%= meta.sourcePath %>/fonts',
            src: ['**/*'],
            dest: '<%= meta.buildPath %>fonts/',
            filter: 'isFile'
          },
          images: {
            option : {},
            expand: true,
            cwd: '<%= meta.sourcePath %>/images',
            src: ['**/*'],
            dest: '<%= meta.buildPath %>images/',
            filter: 'isFile'
          },
          js: {
            option : {},
            expand: true,
            cwd: '<%= meta.sourcePath %>/scripts',
            src: ['**/*.js', '!libs/**/*.js', '!libs/**/*.min.js'],
            dest: '<%= meta.buildPath %>scripts/',
            filter: 'isFile'
          },
          css: {
            option : {},
            expand: true,
            cwd: '<%= meta.sourcePath %>/styles',
            src: ['**/*.css', '!**/*.min.css'],
            dest: '<%= meta.buildPath %>styles/',
            filter: 'isFile'
          },
        },
        imagemin: {
          dist: {
              expand: true,
              cwd: '<%= meta.sourcePath %>/images',
              src: ['**/*.{png,jpg,gif}'],
              dest: '<%= meta.buildPath %>images/'
          }
        },
        svgmin: {
          options: {
            plugins: [{
                removeViewBox: false
            }]
          },
          dist: {
            expand: true,
            cwd: '<%= meta.sourcePath %>/images/',
            src: ['**/*.svg'],
            dest: '<%= meta.buildPath %>images/',
            ext: '.svg'
          }
        },
        validation: {
          options: {
            reset: grunt.option('reset') || true,
            path: '<%= pkg.name %>/build/templates/validation.json',
            reportpath: '<%= pkg.name %>/build/templates/validation.json'
          },
          files: ['<%= pkg.name %>/build/templates/**/*.html']
        },
        autoshot: {
            options: {
                path: '<%= meta.sourcePath %>/screenshots',
                remote : {
                  files: [{ src:'<%= meta.developUrl %>', dest:'test.png', delay: 2500 }]
                },
                viewport: ['240x320','320x480', '320x568','360x640','480x800','480x854','540x960',
                '640x960','720x1280', '768x1024','960x600','1024x768','1152x864','1280x1024','1366x768',
                '1440x900','1600x900','1680x1050','1920x1080']
            },
        },
        casperjs: {
          options: {
            test: true, // seems to not work ...
            async: {
              parallel: true
            },
            casperjsOptions: ['test'] // pass test directly
          },
          files: ['<%= meta.buildPath %>scripts/tests/**/*.js']
        },
        clean: {
          options: {
            force: true
          },
          build: [ "<%= meta.buildPath %>images/**/*", "<%= meta.buildPath %>styles/**/*",
          "<%= meta.buildPath %>scripts/**/*","<%= pkg.name %>/build/templates/**/*",
          "<%= meta.buildPath %>fonts/**/*", "<%= pkg.name %>/build/screenshots/**/*" ]
        },

        // Watch Tasks
        watch: {
            // options: {
            //   livereload: true
            // },
            styles: {
              files: ['<%= less.dev.src %>', '<%= meta.sourcePath %>/styles/**/*.{less}'],
              tasks: ['less:dev', 'concat_css', 'copy:css', 'autoprefixer:dist', 'csso']
            },
            scripts: {
              files: ['<%= meta.sourcePath %>/scripts/**/*.{coffee,js}'],
              tasks: ['copy:js', 'jshint']
            },
            concat: {
              files: ['<%= meta.sourcePath %>/scripts/libs/*.{coffee,js}'],
              tasks: ['concat', 'copy:js']
            },
            casperjs: {
              files: ['<%= meta.sourcePath %>/scripts/**/*.{coffee,js}', '<%= meta.sourcePath %>/scripts/templates/**/*.html'],
              tasks: ['casperjs']
            },
            copy: {
              files: ['<%= meta.sourcePath %>/fonts/**/*.{eot, woff, ttf, svg}', '<%= meta.sourcePath %>/images/{,**/}*.{png,jpg,jpeg,gif,webp,svg}', '<%= meta.sourcePath %>/scripts/{,**/}*.js', '<%= meta.sourcePath %>/styles/{,**/}*.css'],
              tasks: ['copy:fonts', 'copy:images', 'copy:css', 'copy:js']
            },
            images: {
              files: ['<%= imagemin.dist.src %>', ],
              tasks: ['imagemin:dist', 'svgmin:dist']
            }
            // livereload: {
            //     options: {
            //         livereload: true
            //     },
            //     expand: true,
            //     files: [
            //         '<%= meta.buildPath %>scripts/templates/*.css',
            //         '<%= meta.buildPath %>styles/**/*.css',
            //         '<%= meta.buildPath %>scripts/**/*.js',
            //         '<%= meta.buildPath %>images/{,**/}*.{png,jpg,jpeg,gif,webp,svg}'
            //     ]
            // }
        }
    });


    grunt.registerTask('default', function() {
      grunt.log.write('Santy Check!');
    });

    grunt.registerTask('screenshot', ['autoshot']);

    grunt.registerTask('develop', ['browserSync', 'watch']);

    grunt.registerTask('asset_copy', ['clean:build',
                                      'copy:fonts',
                                      'copy:images',
                                      'copy:html',
                                      'copy:js',
                                      'copy:css']);


    grunt.registerTask('rebuild', ['clean:build',
                              'concat',
                              'concat_css',
                              'less:dev',
                              'csso',
                              'imagemin',
                              'svgmin:dev',
                              'copy:fonts',
                              'copy:images',
                              'copy:js',
                              'copy:css',
                              'jshint',
                              'uglify:general',
                              'autoshot']);


    grunt.registerTask('build', ['clean:build',
                              'concat',
                              'concat_css',
                              'less:dist',
                              'csso',
                              'imagemin',
                              'svgmin:dist',
                              'copy:fonts',
                              'copy:images',
                              'copy:js',
                              'copy:css',
                              'jshint',
                              'uglify:general',
                              'autoshot']);
};
