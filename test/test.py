with open("./test.bin", "wb") as f:
    f.write(b"\x00")
    f.write("HelloWorld".encode())