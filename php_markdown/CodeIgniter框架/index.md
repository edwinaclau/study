<?php
//这个文件是入口，后期所有的文件都要在这里执行。
*/
 * -----------------------------------------------
 *     development //开发环境报告所有错误
 *     testing     //测试环境不报告错误
 *     production  //生产环境不报告错误
 */
    define('ENVIRONMENT', 'development');
 
/*
 * 根据环境常量打开不同的错误显示级别
 */
    switch (ENVIRONMENT){
        case 'development':
            error_reporting(E_ALL);
        break;
 
        case 'testing':
        case 'production':
            error_reporting(0);
        break;
 
        default:
            exit('应用的环境设置错误.');
    }
 
/*
 * 系统文件目录，可以自定义
 * --------------------
 * 默认情况下是"system"文件夹，并且在相对于index.php文件同一个目录下。
 * 你可以更改这个路径，但是路径必须与你的系统文件所在位置一致
 *
 */
 
    $system_path = 'system';
 
/*
 *---------------------------------------------------------------
 * 应用程序目录
 *---------------------------------------------------------------
 *
 * 这个文件夹是放置程序的地方，默认情况是“application”文件夹，可以重命名或重定位到服务器上的任何位置。
 * 详情可以访问：
 *
 * 不需要后面的斜杠"/";
 *
 */
 
    $application_folder = 'application';
 
/*
 * --------------------------------------------------------------------
 * --------------------------------------------------------------------
 */

/*
 * ---------------------------------------------------------------
 * 使用可靠的路径解决路由问题
 * ---------------------------------------------------------------
 */
 
    // 是否是从命令行运行？————正确设置当前目录下命令行（CLI）请求
    if (defined('STDIN')){
 
        chdir(dirname(__FILE__));
    }
 
    if (realpath($system_path) !== FALSE){
 
        $system_path = realpath($system_path).'/';
    }
 
    // 确保最后一定以后一个斜杠"/";
    $system_path = rtrim($system_path, '/').'/';
 
    // 判断系统目录是否存在
    if ( ! is_dir($system_path)){
 
        exit("你的系统目录未设置正确. 请打开以下文件重新设置: ".pathinfo(__FILE__, PATHINFO_BASENAME));
    }
 
/*
 * -------------------------------------------------------------------
 *  设置路径（目录）常量
 * -------------------------------------------------------------------
 */
    // 获得当前文件名，即定义入口文件名
    define('SELF', pathinfo(__FILE__, PATHINFO_BASENAME));
 
    // php文件扩展名
　　//不推荐使用全局常量
    define('EXT', '.php');
 
    // 系统目录常量
    define('BASEPATH', str_replace("\\", "/", $system_path));
 
    // 前端控制器路径常量，即入口文件的目录
    define('FCPATH', str_replace(SELF, '', __FILE__));
 
    // 系统核心目录名
　　//trim(BASEPATH, '/')用来去掉首尾的‘/’————trim()函数从字符串的两端删除空白字符和其他预定义字符
　　//strrchr()函数查找字符串在另一个字符串中最后一次出现的位置，并返回从该位置到字符串结尾的所有字符 

    define('SYSDIR', trim(strrchr(trim(BASEPATH, '/'), '/'), '/'));
 
    //定义应用目录常量
    if (is_dir($application_folder)){
 
        define('APPPATH', $application_folder.'/');
    }else{
        if ( ! is_dir(BASEPATH.$application_folder.'/')){
 
            exit("你的应用程序目录可能未设置正确. 请打开以下文件设置: ".SELF);
        }
 
        define('APPPATH', BASEPATH.$application_folder.'/');
    }
 
/*
 * --------------------------------------------------------------------
 * 载入自举文件
 * --------------------------------------------------------------------
 */

require_once BASEPATH.'core/CodeIgniter'.EXT;
 
/* End of file index.php */
/* Location: ./index.php */
