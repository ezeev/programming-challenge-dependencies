
import sys

all_deps = []
depths = []
def parse_deps(name: str, depth: int):
    all_deps.append(name)
    depths.append(depth)
    prefix = 'apps/' + name
    if name.startswith('lib'):
         prefix = 'libs/' + name[3:len(name)]
    f = open(f'{prefix}/meta.txt', "r")
    for line in f:
        l = line
        if (line.startswith("deps:")):
            deps_str = line.split(":")[1]
            new_deps = [d.strip() for d in deps_str.split(",")]
            for dep in new_deps:
                if dep in all_deps:
                    # add it as a duplicate to the list but do not recurse into it
                    all_deps.append(dep + " (duplicate)")
                    depths.append(depth+1)
                    continue
                parse_deps(dep, depth+1)


def main(app: str):
    print(f'Getting dependencies for {app}')
    parse_deps(app, 0)
    for i, dep in enumerate(all_deps):
        tabs = ""
        for x in range(depths[i]):
            tabs+="+"
        print(tabs+dep)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("You must pass in the name of the app to scan for dependencies! Example:")
        print("\tpython3 deps.py breakfast")
        exit()
    app = sys.argv[1]
    main(app)