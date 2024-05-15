from typing import List, Dict
import sys
sys.path.append("../../01Assignment")
from Part_1 import list, dictionaries, flow_control, file_handling 

def test_transform():
    result: List[str] = list.transform_list(["a", "b", "c", "d", "e"])
    expected: List[str] = ["e", "d", "c", "z", "b", "a", "o"]
    assert expected == result

def test_convert():
    result: Dict[str, int] = dictionaries.convert(["Ten", "Twenty", "Thirty"], [10, 20, 30])
    expected: Dict[str, int] = {"Ten": 1000, "Twenty": 2000, "Thirty": 3000}
    assert result == expected

def test_patterns():
    flow_control.print_pattern(1)
    flow_control.print_pattern(4)
    flow_control.print_pattern(10)
    assert True

def test_format_text_file():
    input_file: str = 'input.txt'
    output_file: str = 'output.txt'
    file_handling.format_text_file(input_file, output_file)
    with open(input_file, 'r') as f:
        in_lines = sum(1 for _ in f) # count number of lines
    with open(output_file, 'r') as f:
        out_lines = sum(1 for _ in f)
    assert in_lines == out_lines
