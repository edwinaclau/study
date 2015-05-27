文件上传


针对上传功能DOS
使上传文件服务器作为脚本执行
诱使用户下载恶意文件
越权下载文件


PHP.ini

file_uploads
upload_max_filesize

post_max_size

memoery_limit



例如上传文件会变成

<?php

system('/bin/cat /etc/passwd');

?>


关键取得文件名 content_type
和后缀


一般执行脚本会 假后缀.pdf,实际上是个shell

浏览器除了判断Content-type,还要
打开文件开头的固定字符串，识别GIF,JPEG,PNG

GIF头 \GIF87 或 GIF89a

JPEG头 \xFF\XD8\xFF


PNG头

Content-Type 文件头不一致，你懂，马上干掉.

PDF 的Content-type application/pdf

而非application/x-pdf


文件上传策略
  1.校对扩展名
  2.图像文件确认头
getimagesize函数


一般上传是做了唯一性，那就在文件库中找即可



