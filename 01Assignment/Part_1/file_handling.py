"""
assignment 1
part 1.4
allend27
May 2024
"""

async def format_text_file(input_file, output_file) -> int:
    # Read lines from input file
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Open output file for writing
    with open(output_file, 'w') as f:
        # Print and save lines with line numbers
        for i, line in enumerate(lines, start=1):
            formatted_line = f"{i:2}: {line}"
            # print(formatted_line, end='')
            f.write(formatted_line)
    return 0 

if __name__ == '__main__':
    input_file: str = 'input.txt'
    output_file: str = 'output.txt'
    format_text_file(input_file, output_file)
