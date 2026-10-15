class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        raise IndexError("pop from empty stack")

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        raise IndexError("peek from empty stack")

    def size(self):
        return len(self.items)


def precedence(op):
    if op in ('+', '-'):
        return 1
    if op in ('*', '/'):
        return 2
    return 0


def apply_op(a, b, op):
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/': 
        if b == 0:
            raise ValueError("Division by zero")
        return int(a / b)


def evaluate_expression(expression):
    expression = expression.strip()
    if not expression:
        return None

    if expression.lstrip('-').isdigit():
        return int(expression)

    value_stack = Stack()
    op_stack = Stack()
    i = 0
    n = len(expression)

    while i < n:
        char = expression[i]

        if char.isspace():
            i += 1
            continue

        if char.isdigit():
            val = 0
            while i < n and expression[i].isdigit():
                val = (val * 10) + int(expression[i])
                i += 1
            value_stack.push(val)
            continue

        elif char == '(':
            op_stack.push(char)

        elif char == ')':
            while not op_stack.is_empty() and op_stack.peek() != '(':
                val2 = value_stack.pop()
                val1 = value_stack.pop()
                op = op_stack.pop()
                value_stack.push(apply_op(val1, val2, op))
            if not op_stack.is_empty() and op_stack.peek() == '(':
                op_stack.pop()

        elif char in ('+', '-', '*', '/'):
            while (not op_stack.is_empty() and 
                   precedence(op_stack.peek()) >= precedence(char)):
                val2 = value_stack.pop()
                val1 = value_stack.pop()
                op = op_stack.pop()
                value_stack.push(apply_op(val1, val2, op))
            op_stack.push(char)

        i += 1

    while not op_stack.is_empty():
        val2 = value_stack.pop()
        val1 = value_stack.pop()
        op = op_stack.pop()
        value_stack.push(apply_op(val1, val2, op))

    return value_stack.pop() if not value_stack.is_empty() else None


def process_files(input_filename, output_filename):
    with open(input_filename, 'r') as infile:
        lines = infile.readlines()

    output_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('-----') or stripped == '':
            output_lines.append(line)
        else:
            try:
                result = evaluate_expression(stripped)
                output_lines.append(f"{result}\n" if not line.endswith('\n') else f"{result}\n")
            except Exception as e:
                output_lines.append(f"Error: {e}\n")

    with open(output_filename, 'w') as outfile:
        outfile.writelines(output_lines)


if __name__ == "__main__":
    process_files("input.txt", "output.txt")
    print("Processing complete. output.txt has been generated.")