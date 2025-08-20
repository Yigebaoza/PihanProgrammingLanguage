import sys

from runtime import PihanRuntime

SEP_LENGTH = 20

def error(msg: str):
    raise RuntimeError(msg)

def main(argc, argv):
    runtime = PihanRuntime()
    if argc == 1:
        runtime.ipe_run()
        return
    elif argc == 3:
        if argv[2] == "-genpic":
            runtime.gen_pic_file(argv[1])
            exit()
        error(f"Error Arg: {argv[2]}")


    print(f"{"-" * SEP_LENGTH}Start{"-" * SEP_LENGTH}")
    try:
        runtime.execute_file(argv[1], argv[1].split(".")[1])
    except IndexError:
        runtime.execute_file(argv[1], argv[1])
    finally:
        print(f"{"-" * (SEP_LENGTH + 1)}End{"-" * (SEP_LENGTH + 1)}")


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
