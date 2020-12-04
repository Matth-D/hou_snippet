node_list = ["node", "node_1", "node_2"]


node_name = "node"
if node_name in node_list:  # check if node already exists, use path here
    i = 1
    new_name = node_name + "_" + str(i)
    while new_name in node_list:
        i += 1
        print(new_name)
