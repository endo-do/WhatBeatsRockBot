with open("Names.txt", "r") as f:
    content = f.readlines()
    clean_list = []
    for i in content:
        if i not in clean_list:
            clean_list.append(i)

with open("Names.txt", "w") as f:
    f.writelines(clean_list)