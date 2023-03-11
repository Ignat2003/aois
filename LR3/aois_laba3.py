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


def get_disjunctive_normal_form(vars_for_table: dict, truth_table_answer: dict):
    disjunctive_normal_form = []
    for variant, mean in truth_table_answer.items():
        if mean == 1:
            disjunctive_normal_form.append(vars_for_table[variant])

    return disjunctive_normal_form


def get_conjunctive_normal_form(vars_for_table: dict, truth_table_answer: dict):
    conjunctive_normal_form = []
    for variant, mean in truth_table_answer.items():
        if mean == 0:
            conjunctive_normal_form.append(vars_for_table[variant])

    return conjunctive_normal_form


def sub_gluing(first_element:dict, second_element:dict):
    ans = []
    count_of_equal = 0
    length = len(first_element)
    for i, j in zip(first_element.items(), second_element.items()):
        el1, mean1 = i
        el2, mean2 = j
        if el1 == el2 and mean1 == mean2:
            count_of_equal += 1
            ans.append((el1, mean1))

    if len(ans) == length-1:
        return dict(ans)
    else:
        return None


def gluing(disjunctive_form):
    ans = []
    for i in range(len(disjunctive_form)-1):
        first_element = disjunctive_form[i]
        for j in range(i+1, len(disjunctive_form)):
            second_element = disjunctive_form[j]
            result = sub_gluing(first_element, second_element)
            if result is not None and result not in ans:
                ans.append(result)
    ans = drop_duplicates_in_list(ans)
    return ans


def drop_duplicates_in_list(sam_list):
    result = []
    for i in sam_list:
        if i not in result:
            result.append(i)
    return result

def get_variable_that_not_in_impicant(implicant:dict, variables:list):
    a = list(set(variables.copy()) - set(implicant.copy().keys()))
    return ''.join(a)


def drop_extra_impicants(disjunctive_form: list, variables: list):
    func = ''
    ans = []
    for implicant in disjunctive_form:
        for variable, mean in implicant.items():
            func += variable if mean == 'True' else f'!{variable}'

        func += ' + '
    func = func[:-3]
    for implicant in disjunctive_form:
        variable_that_not_in_impicant = get_variable_that_not_in_impicant(implicant, variables)
        tmp_func = ''
        for variable, mean in implicant.items():
            tmp_func += variable if mean == 'True' else f'!{variable}'

        main_func = func.replace(tmp_func, '', 1)

        for variable, mean in implicant.items():
            mean = '1' if mean == 'True' else '0'
            main_func = main_func.replace(variable, mean)
            main_func = main_func.replace(f'!0', '')
            main_func = main_func.replace(f'!1', '0')
            main_func = main_func.replace(f'1', '')
        test = main_func.split('+')[1:]
        test = list(filter(lambda x: '0' not in x,  test))
        main_func = ''.join(test)
        count_positive = main_func.count(f' {variable_that_not_in_impicant} ')
        count_negative = main_func.count(f' !{variable_that_not_in_impicant} ')
        if count_negative == count_positive:
            ans.append(implicant.copy())

    return ans


if __name__ == "__main__":
    # infunc = input('Enter your function: ')
    infunc = '((a+b)*(c+d))'
    infunc = infunc.replace("=", "==")
    variables = sorted(set(re.findall(r"[A-Za-z]", infunc)))
    vars_for_table = vars_for_truth_table(variables)
    truth_table_answer = calculate_truth_table(infunc[:], vars_for_table, variables)

    disjunctive_normal_form = get_disjunctive_normal_form(vars_for_table, truth_table_answer)
    conjunctive_normal_form = get_conjunctive_normal_form(vars_for_table, truth_table_answer)

    a = gluing(disjunctive_normal_form)
    b = drop_extra_impicants(a, variables)
    print(b)
