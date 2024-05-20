"""
assignment 1
part 1.3
allend27
May 2024
"""
def print_pattern(depth: int) -> str:
    output:str = (f"in this case n = {depth}{'\n'}")
    for i in range(1, depth+2):
        output += str('* ' * i)
        output += "\n"
    for i in range(depth, 0, -1):
        output += str('* ' * i)
        output += "\n"
    return output

if __name__ == '__main__':
    print(print_pattern(4))
    print(print_pattern(1))
