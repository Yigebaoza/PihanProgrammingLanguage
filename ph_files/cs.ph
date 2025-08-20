var choose = ward("选择：", io)
jud choose == "1"?{
    in::writeln("Hello, world!", so)
}
nud choose == "2"?{
    in::writeln("Hi!", so)
}
not ?{
    in::writeln("This is not a true block", so)
}