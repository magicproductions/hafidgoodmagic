import gulp        from 'gulp';
import yargs       from 'yargs';
import cleanCSS    from 'gulp-clean-css';
import gulpif      from 'gulp-if';
import sourcemaps  from 'gulp-sourcemaps';
import imagemin    from 'gulp-imagemin';
import del         from 'del';
import webpack     from 'webpack-stream';
import uglify      from 'gulp-uglify';
import named       from 'vinyl-named';
import browserSync from 'browser-sync';
import zip         from 'gulp-zip';

const server     = browserSync.create();
const sass       = require('gulp-sass')(require('sass'));
const PRODUCTION = yargs.argv.prod;


const paths = {
    styles: {
        src : [
            'resources/scss/theme.scss',
            'resources/scss/helper.scss',
            'resources/scss/admin.scss',
        ],
        dest: 'hafid_good_magic/static/css'
    },
    scrips: {
        src : [
            'resources/js/theme.js',
            'resources/js/shop.js',
        ],
        dest: 'hafid_good_magic/static/js'
    },
    // copyJS: {
    //     src : [
    //         'resources/js/plugin.js',
    //     ],
    //     dest: 'magic_prod_proj/static/js'
    // },
    // copyCss: {
    //     src : [
    //         'resources/admin/admin.scss',
    //     ],
    //     dest: 'magic_prod_proj/static/css'
    // },
    images : {
        src : 'resources/assets/img/**/*.{jpeg,jpg,png,svg,gif}',
        dest: 'hafid_good_magic/static/assets/img'
    },
    other  : {
        src : ['resources/**/*', '!resources/{img,js,scss}', '!resources/{img,js,scss}/**/*'],
        dest: 'hafid_good_magic/static'
    },
    package: {
        src : [
            '**/*', '!node_modules{,/**}', '!venv{,/**}', '!.gitignore', '!git{,/**}', '!resources{,/**}',
            '!packaged{,/**}', '!.babelrc', '!db.sqlite3', '!gulpfile.babel.js', '!package.json', '!package-lock.json'
        ],
        dest: 'packaged'
    }
};

export const serve = (done) => {
    server.init({
                    notify: false,
                    port  : 8000,
                    proxy : 'http://127.0.0.1:8000'
                });
    done();
};

export const reload = (done) => {
    server.reload();
    done();
};

export const clean = () => {
    return del(['magic_prod_proj/static/']);
};

export const styles = () => {
    return gulp.src(paths.styles.src)
               .pipe(gulpif(!PRODUCTION, sourcemaps.init()))
               .pipe(sass().on('error', sass.logError))
               .pipe(gulpif(PRODUCTION, cleanCSS({compatibility: 'ie8'})))
               .pipe(gulpif(!PRODUCTION, sourcemaps.write()))
               .pipe(gulp.dest(paths.styles.dest))
               .pipe(server.stream());

};

// export const copyAdminCss = () => {
//     return gulp.src(paths.copyCss.src)
//                .pipe(gulpif(!PRODUCTION, sourcemaps.init()))
//                .pipe(sass().on('error', sass.logError))
//                .pipe(gulpif(PRODUCTION, cleanCSS({compatibility: 'ie8'})))
//                .pipe(gulpif(!PRODUCTION, sourcemaps.write()))
//                .pipe(gulp.dest(paths.copyCss.dest))
//                .pipe(server.stream());
//
// };

export const images = () => {
    return gulp.src(paths.images.src)
               .pipe(gulpif(PRODUCTION, imagemin()))
               .pipe(gulp.dest(paths.images.dest));

};

export const watch = () => {
    gulp.watch('resources/scss/**/*.scss', styles);
    // gulp.watch('resources/admin/**/*.scss', copyAdminCss);
    gulp.watch('resources/js/**/*.js', gulp.series(scripts, reload));
    // gulp.watch("**/*.py", reload);
    gulp.watch('**/*.html', reload);
    gulp.watch(paths.images.src, gulp.series(images, reload));
    gulp.watch(paths.other.src, gulp.series(copy, reload));
};

export const copy = () => {
    return gulp.src(paths.other.src)
               .pipe(gulp.dest(paths.other.dest));

};

// export const copyMinJs = () => {
//     return gulp.src(paths.copyJS.src)
//                .pipe(gulp.dest(paths.copyJS.dest));
//
// };

export const scripts = () => {
    return gulp.src(paths.scrips.src)
               .pipe(named())
               .pipe(webpack({
                                 module : {
                                     rules: [
                                         {
                                             test: /\.js$/,
                                             use : {
                                                 loader : 'babel-loader',
                                                 options: {
                                                     presets: ['@babel/preset-env']
                                                 }
                                             }
                                         }
                                     ]
                                 },
                                 output : {
                                     filename: '[name].js'
                                 },
                                 devtool: !PRODUCTION ? 'inline-source-map' : false,
                                 mode   : PRODUCTION ? 'production' : 'development'
                             }))
               .pipe(gulpif(PRODUCTION, uglify()))
               .pipe(gulp.dest(paths.scrips.dest));
};

export const compress = () => {
    return gulp.src(paths.package.src)
               .pipe(zip('magic_prod.zip'))
               .pipe(gulp.dest(paths.package.dest));

};


export const dev    = gulp.series(clean, gulp.parallel(styles, scripts, images, copy), serve, watch);
export const build  = gulp.series(clean, gulp.parallel(styles, scripts, images, copy));
export const bundle = gulp.series(build, compress);

export default dev;

// copyMinJs, images, copyMinJs, images,
