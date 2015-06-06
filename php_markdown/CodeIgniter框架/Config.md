<?php  if ( ! defined('BASEPATH')) exit('No direct script access allowed');
 
class CI_Config {
 
    /**
     * 配置变量列表
     */
    var $config = array();
    /**
     * 保存已加载的配置文件列表
     */
    var $is_loaded = array();
    /**
     * 配置路径
     */
    var $_config_paths = array(APPPATH);
 
 
    function __construct()
    {
        $this->config =& get_config();
        log_message('debug', "Config Class Initialized");
 
        // 如果base_url没有配置，如果没有则动态配置(set_item)base_url
        if ($this->config['base_url'] == '')
        {
            if (isset($_SERVER['HTTP_HOST']))
            {
                $base_url = isset($_SERVER['HTTPS']) && strtolower($_SERVER['HTTPS']) !== 'off' ? 'https' : 'http';
                $base_url .= '://'. $_SERVER['HTTP_HOST'];
                                //当然要去掉文件名
                $base_url .= str_replace(basename($_SERVER['SCRIPT_NAME']), '', $_SERVER['SCRIPT_NAME']);
            }
 
            else
            {
                $base_url = 'http://localhost/';
            }
 
            $this->set_item('base_url', $base_url);
        }
    }
 
    // --------------------------------------------------------------------
 
    /**
     * 加载配置文件
     *
 
     * @param $file    string    配置文件的名称
     * @param $use_sections  boolean  配置变量是否方法默认的Config::$config，还是以独立的数组存在
         * 这个其实很简单，例如你加载test_config.php配置文件，配置信息是以$configp['test_config'][×××]还是直接$config[×××]保存
         * 
     * @param $fail_gracefully  boolean  如果文件加载失败是否报错，如果为TRUE直接返回return false,如果为FALSE,则返回错误信息
     * @return    boolean    if the file was loaded correctly
     */
    function load($file = '', $use_sections = FALSE, $fail_gracefully = FALSE)
    {
        $file = ($file == '') ? 'config' : str_replace('.php', '', $file);
        $found = FALSE;
        $loaded = FALSE;
                
                //从相应的开发环境查找文件
        $check_locations = defined('ENVIRONMENT')
            ? array(ENVIRONMENT.'/'.$file, $file)
            : array($file);
 
        foreach ($this->_config_paths as $path)
        {
            foreach ($check_locations as $location)
            {
                $file_path = $path.'config/'.$location.'.php';
 
                if (in_array($file_path, $this->is_loaded, TRUE))
                {
                    $loaded = TRUE;
                    continue 2;//跳出两层循环
                }
 
                if (file_exists($file_path))
                {
                    $found = TRUE;
                    break;
                }
            }
 
            if ($found === FALSE)
            {
                continue;
            }
 
            include($file_path);
 
            if ( ! isset($config) OR ! is_array($config))
            {
                if ($fail_gracefully === TRUE)
                {
                    return FALSE;
                }
                show_error('Your '.$file_path.' file does not appear to contain a valid configuration array.');
            }
 
            if ($use_sections === TRUE)
            {
                if (isset($this->config[$file]))
                {
                    $this->config[$file] = array_merge($this->config[$file], $config);
                }
                else
                {
                    $this->config[$file] = $config;
                }
            }
            else
            {
                $this->config = array_merge($this->config, $config);
            }
 
            $this->is_loaded[] = $file_path;
            unset($config);
 
            $loaded = TRUE;
            log_message('debug', 'Config file loaded: '.$file_path);
            break;
        }
 
        if ($loaded === FALSE)
        {
            if ($fail_gracefully === TRUE)
            {
                return FALSE;
            }
            show_error('The configuration file '.$file.'.php does not exist.');
        }
 
        return TRUE;
    }
 
    // --------------------------------------------------------------------
 
    /**
     * 获取配置信息
     *
     * @param  $item  string  配置元素名
     * @param $index   string  键名
         * 第二个参数，看看load()中的第二个参数就动了，如果为TRUE,当然是以$this->config[$index][$item]获取配置信息
         * 
         * 
     * @param    bool
     * @return    string
     */
    function item($item, $index = '')
    {
        if ($index == '')
        {
            if ( ! isset($this->config[$item]))
            {
                return FALSE;
            }
 
            $pref = $this->config[$item];
        }
        else
        {
            if ( ! isset($this->config[$index]))
            {
                return FALSE;
            }
 
            if ( ! isset($this->config[$index][$item]))
            {
                return FALSE;
            }
 
            $pref = $this->config[$index][$item];
        }
 
        return $pref;
    }
 
    // --------------------------------------------------------------------
 
    /**
     * 这个函数简单，返回修剪后的以“/”结尾的配置信息
         * PS:下面会用到
     */
    function slash_item($item)
    {
        if ( ! isset($this->config[$item]))
        {
            return FALSE;
        }
 
        if( trim($this->config[$item]) == '')
        {
            return '';
        }
 
        return rtrim($this->config[$item], '/').'/';
    }
 
    // --------------------------------------------------------------------
 
    /**
     * url_helper的site_url()函数调用的就是这个方法
     *
     * @access    public
     * @param    string    the URI string
     * @return    string
     */
    function site_url($uri = '')
    {
        if ($uri == '')
        {
            return $this->slash_item('base_url').$this->item('index_page');
        }
 
        if ($this->item('enable_query_strings') == FALSE)
        {
            $suffix = ($this->item('url_suffix') == FALSE) ? '' : $this->item('url_suffix');
            return $this->slash_item('base_url').$this->slash_item('index_page').$this->_uri_string($uri).$suffix;
        }
        else
        {
            return $this->slash_item('base_url').$this->item('index_page').'?'.$this->_uri_string($uri);
        }
    }
 
    // -------------------------------------------------------------
 
    /**
     * 获取base_url
     */
    function base_url($uri = '')
    {
        return $this->slash_item('base_url').ltrim($this->_uri_string($uri), '/');
    }
 
    // -------------------------------------------------------------
 
    /**
     *返回uri_string
     */
    protected function _uri_string($uri)
    {
        if ($this->item('enable_query_strings') == FALSE)
        {
            if (is_array($uri))
            {
                $uri = implode('/', $uri);
            }
            $uri = trim($uri, '/');
        }
        else
        {
            if (is_array($uri))
            {
                $i = 0;
                $str = '';
                foreach ($uri as $key => $val)
                {
                    $prefix = ($i == 0) ? '' : '&';
                    $str .= $prefix.$key.'='.$val;
                    $i++;
                }
                $uri = $str;
            }
        }
        return $uri;
    }
 
    // --------------------------------------------------------------------
 
    /**
     * 获取系统的目录路径
     */
    function system_url()
    {
             
        $x = explode("/", preg_replace("|/*(.+?)/*$|", "\\1", BASEPATH));
        return $this->slash_item('base_url').end($x).'/';
    }
 
    // --------------------------------------------------------------------
 
    /**
     * 重新动态设置配置信息
     */
    function set_item($item, $value)
    {
        $this->config[$item] = $value;
    }
 
    // --------------------------------------------------------------------
 
    /**
     * 动态添加配置信息，这个在CodeIgniter.php中有用，将index.php中配置信息添加到config组件中
     */
    function _assign_to_config($items = array())
    {
        if (is_array($items))
        {
            foreach ($items as $key => $val)
            {
                $this->set_item($key, $val);
            }
        }
    }
}