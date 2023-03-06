import re


infunc = input('Enter your function: ')
infunc = infunc.replace("=", "==")
infunc = infunc.replace('>', '<=')

variables = sorted(set(re.findall(r"[A-Za-z]", infunc)))

# просто красивое оформление для таблицы
header = [""] * 2
for key in variables:
    header[0] += "-" * 7 + "+"
    header[1] += f"   {key}   |"
header[0] += "-+" + "-" * 7
header[1] += " | Result"
print("\n".join(header + header[0:1]))

vars_for_eval = {}
disjunctive_normal_form_safe = []
conjunctive_normal_form = []

# вариантов входных значений для таблицы - 2 в степени кол-ва переменных
for variant in range(1 << len(variables)):
    # заполняем входной словарь c представлением переменных
    # key идут в прямом порядке, а i - в обратном
    for i, key in reversed(list(enumerate(reversed(variables)))):
        # используем биты этого числа для инициализыции булевых значений
        vars_for_eval[key] = bool(variant & (1 << i))
        # вывод строки таблицы истинности
        print(f" {vars_for_eval[key]:<5}", end=" |")
    # вычисляем результат
    infunc = infunc.replace('-', 'not ')
    infunc = infunc.replace('+', ' or ')

    func = infunc[:]
    for variable, is_true in vars_for_eval.items():
        is_true = str(bool(is_true))
        func = func.replace(variable, is_true)

    result = eval(func)
    result = 1 if result > 0 else 0
    if result:
        disjunctive_normal_form_safe.append(vars_for_eval.copy())
    else:
        conjunctive_normal_form.append(vars_for_eval.copy())

    print(f" | {result:<5}")
print(header[0])

print('Disjunctive_normal_form')
answer = ''

for form in disjunctive_normal_form_safe:
    for variable, is_true in form.items():
        print(' ' if is_true else '-',  end='')
        answer += variable
    print('   ', end='')
    answer += ' ∨ '
print()
print(''.join(answer[:-2]))

print()
print('Conjunctive_normal_form')
answer = ''
for form in conjunctive_normal_form:
    answer += '('
    print(' ', end='')

    for variable, is_true in form.items():
        print('- ' if is_true else '  ',  end='')
        answer += variable

    print(' ', end='')
    answer += ')∧'
print()
answer = ''.join(answer[:-1])

for variable in variables[:-1]:
    answer = answer.replace(variable, variable + '+')
print(answer)
