module.exports = function(grunt) {
    var jsFiles = ['build/*.js'],
        testFiles = ['test/*.js'],
        lintFiles = ['Gruntfile.js'].concat(jsFiles, testFiles),
        npmTasks = [
            'grunt-contrib-jshint',
            'grunt-jscs-checker',
            'grunt-contrib-jasmine'
        ];

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        jshint: {
            all: lintFiles,
            options: {
                jshintrc: '.jshintrc'
            }
        },
        jscs: {
            all: lintFiles,
            options: {
                config: '.jscs.json'
            }
        },
        jasmine: {
            src: jsFiles,
            options: {
                keepRunner: true,
                specs: testFiles,
                styles: ['build/django-user-guide.css'],
                template: require('grunt-template-jasmine-istanbul'),
                templateOptions: {
                    coverage: '.tmp/coverage.json',
                    report: [{type: 'text-summary'}],
                    thresholds: {
                        lines: 100,
                        statements: 100,
                        branches: 100,
                        functions: 100
                    }
                }
            }
        }
    });

    npmTasks.forEach(function(task) {
        grunt.loadNpmTasks(task);
    });

    grunt.registerTask('test', ['jshint', 'jscs', 'jasmine']);
};
