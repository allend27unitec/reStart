"""
assignment 1
part 1.3
allend27
May 2024
"""
def print_pattern(depth: int) -> None:
    print(f"in this case n = {depth}")
    for i in range(1, depth+2):
        print('* ' * i)
    for i in range(depth, 0, -1):
        print('* ' * i)

if __name__ == '__main__':
    print_pattern(4)
    print_pattern(1)
