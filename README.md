# Pihan(Python core f***i***le ***han***dle program language)
## Pihan语言是一种用于操作文件的编程语言，它具有以下特性：
1. 定义的变量默认是字符串（ 可用类型转换函数转换成其他类型 ）
2. 面向流程
3. in::关键字（ 不加时外部会运行一遍，其实是缺点\[doge\] ）
4. 具有Python的一些特性

## Pihan语言有以下内置函数：
  #### 1. write(text, stream)
  - text: 要写入的内容
  - stream: 要写入的流（so, sys.so, "C:\\a\b\s\path\file.txt", "../files/writeme.py"）
   
    操作: 将`text`写入`stream`
    
  #### 2. writeln(text, stream)
  - text: 要写入的内容
  - stream: 要写入的流（ so, sys.so, "C:\\a\b\s\path\file.txt", "../files/writeme.py" ）
   
    操作: 将`text`写入`stream`，然后换行
    
  #### 3. readchar(stream)
  - stream: 要读取的流（ "C:\\a\b\s\path\file.txt", "../files/writeme.py" ）
   
    操作: 返回从`stream`读取的一个字符
    
  #### 4. readln(stream)
  - stream: 要读取的流（ "C:\\a\b\s\path\file.txt", "../files/writeme.py" ）
   
    操作: 返回从`stream`读取的一行字符串
    
  #### 5. read(stream, length=-1)
  - length: 要读取的长度（-1是一行）
  - stream: 要读取的流（ "C:\\a\b\s\path\file.txt", "../files/writeme.py" ）
   
    操作: 返回从`stream`读取的长度为`length`的内容
    
  #### 6. ward, wardln(text, streams, length=-1)
  - text: 要写入的内容
  - length: 要读取的长度（默认是一行）
  - stream: 要写入并读取的流（ sys.io, io, "C:\\a\b\s\path\file.txt", "../files/writeme.py" ）
   
    操作: 先从`streams[0]`写入内容，再返回从`streams[1]`读取的内容
    
  #### 7. `type`(a)
  - type: int, str, float（ 暂不支持dict, list, 可使用，但有漏洞 ）
  - a: 值或变量
    
    操作: 将`a`转换成`type`，再返回 
## 语法规则
  ### Hello world
  ```pihan
  // 将HelloWorld写入到系统（控制台）的标准输出
  writeln("HelloWorld", so)
  // 另一种写法
  writeln("HelloWorld", sys.so)
  ```

  ### 声明变量
  ```pihan
  var num = 1
  writeln(f"num = {num}", so)
  // res -> num = 1
  ```

  ### 条件判断语句
  ```pihan
  var choose = ward("选择：", io)
  jud choose == "1"?{
    in::writeln("True", so)
  }
  not ?{
    in::writeln("This is not a true block", so)
  }
  ```
  ### 函数
  ```pihan
  func add(a, b)&{
    < a + b
  }
  var res = add(10, 2)
  writeln(f"res: {res}", so)
  ```

    