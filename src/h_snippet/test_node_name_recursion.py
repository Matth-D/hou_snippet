node_list = ["node", "node_1", "node_2"]


# node_name = "node"
# if node_name in node_list:  # check if node already exists, use path here
#     i = 1
#     new_name = node_name + "_" + str(i)
#     while new_name in node_list:
#         i += 1

name = "node"
basename = "node"
i = 1
while name in node_list:

    name = basename + "_" + str(i)
    i += 1
print name


# i = 1
# while i < 5:
#     i += 1
# print i
