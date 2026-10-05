import sys
import os

def solve():

    pass

def main():
   
    if os.path.exists('input.txt'):
        sys.stdin = open('input.txt', 'r')
        sys.stdout = open('output.txt', 'w')
    
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    # Example parsing
    # t = int(input_data[0])
    
if __name__ == '__main__':
    main()