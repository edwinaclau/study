字母表(alphabet)
大小写字母，数字，特殊符号，

{b,c} {b,c,d}

{b,c,d}字母表上的字符串

假设字母表{b,c,d}

cbd

cbcc

c

字符串cbcc(一个3字符字母表{b,c,d}上的字符串)

字符串b出现，字符C出现3次，字符d 没有出现

|cbcc| 表示串的长度，|cbcc| = 4


仅包含cbd,cbcc和c集合是一个语言


public c
{
 public static void main(String[] args) 
{
}

}



语言规则(syntax rules)

语义规则(semantic rules)


一个编译器由三部分组成:单词符号管理,
                     语法分析器
                     代码生成器

Int x;
x = 55;


int
x
;
=
55
;

单词管理器不为空白（空格，制表符，换行符以及回车符)
和注释生成单词符号，因为语法分析器不需要源程序这些成分

单词符号管理器也称(词法分析器 lexical analyzer, lexer)
扫描器(scanner)或单词符号管理器(tokenizer)


词法分析器(parser)
(1)


(2)


(3)


代码生成器(code generator)是编译器最后一个模块


整数3和421组成的集合

{3,421} 和 {421,3}

{b, bb, bbb,...}

{E,定义规则}
{x:X是整数,且1<= x <= 100}




空集(empty set)

全集(universal set)