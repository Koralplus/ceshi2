def check_brackets(string):
    stack = []
    result = ""

    for i, char in enumerate(string):
        if char == '(':
            stack.append((char, i))
        elif char == ')':
            if stack:
                stack.pop()
            else:
                result += "?"
                continue  # 跳过继续处理右括号
        result += ' '

    while stack:
        _, idx = stack.pop()
        result = result[:idx] + "x" + result[idx+1:]

    print(result)  # 输出结果


# 读取输入测试用例
while True:
    try:
        test_case = input()
        print(test_case)
        check_brackets(test_case)
    except EOFError:
        break
