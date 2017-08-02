import sys
import time

# def spinning_cursor():
#     while True:
#         for cursor in '|/-\\':
#             yield cursor
#
#
# spinner = spinning_cursor()
# for _ in range(50):
#     sys.stdout.write(spinner.next())
#     sys.stdout.flush()
#     time.sleep(0.1)
#     sys.stdout.write('\b')

old_src = ""


def overwrite_statement(source, last_statement=False):
    global old_src
    if old_src is not "":
        for x in range(0, len(old_src)):
            #sys.stdout.write('\b')
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
    old_src = source
    sys.stdout.write(old_src)
    sys.stdout.flush()
    if last_statement:
        old_src = ""
        print old_src
