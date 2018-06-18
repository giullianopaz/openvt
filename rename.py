import os, sys
dirname = sys.argv[2]
i = int(sys.argv[1])
if os.path.isdir(dirname):
    dir_list = os.listdir(dirname)
    dir_list.sort()
    for filename in dir_list:
        # print("{} - {}".format(dirname + "/" + filename, dirname + "/" + str(i)))
        os.rename(dirname + "/" + filename, dirname + "/" + str(i) + '.jpg')
        i += 1