import re

def find_index_parenthesis(func: str):
    first_parenthesis = None
    last_parenthesis = func.find(')')
    index = 0
    for i in func[:last_parenthesis]:
        if i == '(':
            first_parenthesis = int(index)
        index += 1
    if first_parenthesis is None:
        raise print('Parse error didnt find first_parenthesis')

    return first_parenthesis, last_parenthesis


def parse_func(func):
    while '(' in func:
        first_parenthesis, last_parenthesis = find_index_parenthesis(func)
        subexpression = func[first_parenthesis: last_parenthesis + 1]
        if '-' in subexpression:
            answer = 'True' if 'False' in subexpression else 'False'
            func = func.replace(subexpression, answer, 1)
        elif '==' in subexpression:
            answer = 'True' if subexpression.count('False') == 2 or subexpression.count('True') == 2 else 'False'
            func = func.replace(subexpression, answer, 1)
        elif '+' in subexpression:
            answer = 'True' if 'True' in subexpression else 'False'
            func = func.replace(subexpression, answer, 1)
        elif '*' in subexpression:
            answer = 'True' if subexpression.count('True') == 2 else 'False'
            func = func.replace(subexpression, answer, 1)
        elif '>' in subexpression:
            first_symbol, second_symbol = subexpression.split('>')
            if 'True' in second_symbol:
                answer = 'True'
            elif 'False' in first_symbol:
                answer = 'True'
            else:
                answer = 'False'
            func = func.replace(subexpression, answer, 1)
        else:
            raise print('Parse error')
    if func == 'True':
        result = 1
    else:
        result = 0
    return result


def vars_for_truth_table(variables):
    vars_for_eval = {}
    for variant in range(1 << len(variables)):
        vars_for_eval[variant] = {}
        # заполняем входной словарь c представлением переменных
        # key идут в прямом порядке, а i - в обратном
        for i, key in reversed(list(enumerate(reversed(variables)))):
            # используем биты этого числа для инициализыции булевых значений
            vars_for_eval[variant].update({key: str(bool(variant & (1 << i)))})
            # vars_for_eval[key] = bool(variant & (1 << i))

    return vars_for_eval


def change_symbols(func: str, vars_for_eval: dict):
    # Замена символов на True and False
    for variable, is_true in vars_for_eval.items():
        func = func.replace(variable, f' {variable} ')

    for variable, is_true in vars_for_eval.items():
        func = func.replace(f' {variable} ', is_true)

    if func.count('(') != func.count(')'):
        raise Exception("Wrong amount of staples")
    return func


def calculate_truth_table(func: str, vars_for_truth_table: dict, variables: list):
    truth_table_dst = {}
    for variant in vars_for_truth_table:
        tmp_func = change_symbols(func[:], vars_for_truth_table[variant])
        answer = parse_func(tmp_func[:])
        truth_table_dst[variant] = answer

    return truth_table_dst


def print_table(vars_for_table: dict, truth_table_answer: dict, variables: list):
    for v in variables:
        print(f' {v} ', end='')
    print('  Result')
    for variant in vars_for_table:
        for variable, mean in vars_for_table[variant].items():
            mean = 1 if mean == 'True' else 0
            print(f' {mean} ', end='')
        print(f'  {truth_table_answer[variant]}')


def print_disjunctive_normal_form(vars_for_table: dict, truth_table_answer: dict):
    disjunctive_normal_form = []
    for variant, mean in truth_table_answer.items():
        if mean == 1:
            disjunctive_normal_form.append(vars_for_table[variant])

    answer = ''
    for form in disjunctive_normal_form:
        for variable, is_true in form.items():
            print(' ' if is_true == 'True' else '-', end='')
            answer += variable
        print('   ', end='')
        answer += ' ∨ '
    print()
    print(''.join(answer[:-2]))


def print_conjunctive_normal_form(vars_for_table: dict, truth_table_answer: dict):
    conjunctive_normal_form = []
    for variant, mean in truth_table_answer.items():
        if mean == 0:
            conjunctive_normal_form.append(vars_for_table[variant])

    answer = ''
    for form in conjunctive_normal_form:
        answer += '('
        print(' ', end='')

        for variable, is_true in form.items():
            print('- ' if is_true == 'True' else '  ', end='')
            answer += variable

        print(' ', end='')
        answer += ')∧'
    print()
    answer = ''.join(answer[:-1])

    for variable in variables[:-1]:
        answer = answer.replace(variable, variable + '+')
    print(answer)


def print_disjunctive_number_form(truth_table_answer: dict):
    answer = []
    for variant, mean in truth_table_answer.items():
        if mean == 1:
            answer.append(str(variant))
    print('v(', end='')
    a = ','.join(answer)
    print(a, end='')
    print(')')


def print_conjunctive_number_form(truth_table_answer: dict):
    answer = []
    for variant, mean in truth_table_answer.items():
        if mean == 0:
            answer.append(str(variant))
    print('∧(', end='')
    a = ','.join(answer)
    print(a, end='')
    print(')')

def print_disjunctive_index_form(truth_table_answer: dict):
    degree = len(truth_table_answer)
    weights = []
    for variant, mean in truth_table_answer.items():
        if mean == 1:
            weights.append(2 ** degree)
        degree -= 1
    return sum(weights)

def print_conjunctive_index_form(truth_table_answer: dict):
    degree = len(truth_table_answer)
    weights = []
    for variant, mean in truth_table_answer.items():
        if mean == 0:
            weights.append(2 ** degree)
        degree -= 1
    return sum(weights)


if __name__ == "__main__":
    infunc = input('Enter your function: ')
    infunc = infunc.replace("=", "==")
    variables = sorted(set(re.findall(r"[A-Za-z]", infunc)))
    vars_for_table = vars_for_truth_table(variables)
    truth_table_answer = calculate_truth_table(infunc[:], vars_for_table, variables)
    print_table(vars_for_table, truth_table_answer, variables)
    print('Disjunctive_normal_form')
    print_disjunctive_normal_form(vars_for_table, truth_table_answer)
    print('Conjunctive_normal_form')
    print_conjunctive_normal_form(vars_for_table, truth_table_answer)
    print('Disjunctive_number_form')
    print_disjunctive_number_form(truth_table_answer)
    print('Conjunctive_number_form')
    print_conjunctive_number_form(truth_table_answer)
    print('Index form disjunctive')

    ans = print_disjunctive_index_form(truth_table_answer)
    print(f'F {ans} сднф')
    print('Index form conjunctive')
    ans = print_conjunctive_index_form(truth_table_answer)
    print(f'F {ans} скнф')