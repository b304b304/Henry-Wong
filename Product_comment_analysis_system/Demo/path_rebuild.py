import re

test = "\"assets/img/avatars/128.jpg\""

print()


def assets_to_statcic(file_path):
    f = open(file_path, "r+")
    content = f.readlines()
    f.seek(0, 0)
    for line in content:
        line_new = re.sub("assets", "/static", line)
        f.write(line_new)
    f.close()

if __name__ == "__main__":
    assets_to_statcic("./templates/index.html")
