import sys

from runtime import PihanRuntime

SEP_LENGTH = 20


def main(argc, argv):
    runtime = PihanRuntime()
    if argc == 1:
        runtime.ipe_run()
    elif not argv[1].endswith('.ph') or argc != 2:
        print(f"Usage: {argv[0]} {argv[1].split('.')[0]}.ph")
        exit(1)

    print(f"{"-" * SEP_LENGTH}Start{"-" * SEP_LENGTH}")
    try:
        runtime.execute_file(argv[1])
    finally:
        print(f"{"-" * (SEP_LENGTH + 1)}End{"-" * (SEP_LENGTH + 1)}")


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
