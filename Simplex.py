import copy

def input_data():
    #print("Введите уравнение, которое нужно оптимизировать. Пример: 1 4. То есть уравнение выглядит так: F = x_1 + 4*x_2")
    free_vars = [4,5]
    #print("Выберите решим оптимизации: min или max")
    regime = "max"
    if regime == "min":
        free_vars = [-1*i for i in free_vars]
    #print("Введите количество ограничивающих условий")
    lim_conditions = 2
    limits = [[1, 1, 1,0,0,0,0,100],
              [3, 1, 0,1,0,0,0, 50], [2, 3, 0,0,1,0,0,20],
              [1,0,0,0,0,1,0,50], [0,1,0,0,0,0,1,23]]
    index_line = [-1*i for i in free_vars]
    for _ in range(len(limits[0]) - 1 - len(free_vars)):
        index_line.append(0)
    costs = {}
    for id, cost in enumerate(index_line):
        if regime == "max":
            costs[id] = -1*cost
        else:
            costs[id] = cost
    basis_ids = [i+len(free_vars) for i in range(len(limits[0]) - 1 - len(free_vars))]
    return (free_vars, limits, index_line, costs, basis_ids, regime)
    
def findmin(mas):
    min_id = 0
    min_val = float("inf")
    for i in range(len(mas)):
        if mas[i] < min_val:
            min_val = mas[i]
            min_id = i
    return (min_id, min_val)

def findmax(mas):
    min_id = 0
    min_val = float("-inf")
    for i in range(len(mas)):
        if mas[i] > min_val:
            min_val = mas[i]
            min_id = i
    return (min_id, min_val)

free_vars, limits, index_line, costs, basis_ids, regime = input_data()
print()
def iteration(free_vars, limits, index_line, costs, basis_ids):
    len_fv = len(free_vars)
    for _ in range(len(limits[0]) - 1 - len_fv):
        free_vars.append(0)
    #Определяем разрешающий элемент
    k, k_val, r, r_val = None, None, None, None
    if regime == "max":
        k, k_val = findmin(index_line)
        r, r_val = float('inf'), float('inf')
    else:
        k, k_val = findmax(index_line)
        r, r_val = float('inf'), float('inf')

    for i in range(len(limits)):
        if limits[i][k] != 0:
            prob_r = limits[i][-1]/limits[i][k]
            if prob_r < r_val and prob_r > 0:
                r = i
                r_val = prob_r
        else:
            continue

    prob_r = prob_r*limits[r][k]
    razresh_elem =  limits[r][k]
    basis_ids[r] = k #Смена базиса
    #Пересчитываем ресурсы 
    prev = limits[r][-1]
    for i in range(len(basis_ids)):
        if i == r:
            limits[i][-1] = limits[i][-1]/razresh_elem
        else:
            limits[i][-1] = limits[i][-1] - (prev/razresh_elem)*limits[i][k]
    #Пересчитываем переменные
    prev_limits = copy.deepcopy(limits)
    for i in range(len(limits)):
        for j in range(len(limits[0])-1):
            if i == r:
                limits[i][j] = prev_limits[i][j]/razresh_elem
            else:
                limits[i][j] = prev_limits[i][j] - (prev_limits[r][j]/razresh_elem)*prev_limits[i][k]
    #Пересчитываем цены
    basis_costs = [costs[i] for i in basis_ids]
    #Рассчитываем индексную строку
    for i in range(len(basis_ids)):
        id_sum = 0
        for j in range(len(basis_costs)):
            id_sum += basis_costs[j]*limits[j][i]
        index_line[i] = id_sum - free_vars[i]

    return basis_costs

def simplex_method():
    basis_costs_ans = None
    if regime == "max":
        while min(index_line) < 0:
            basis_costs = iteration(free_vars, limits, index_line, costs, basis_ids)
            basis_costs_ans = copy.deepcopy(basis_costs)
    else:
        while max(index_line) > 0:
            basis_costs = iteration(free_vars, limits, index_line, costs, basis_ids)
            basis_costs_ans = copy.deepcopy(basis_costs)
    print("Оптимальный план:")
    sum = 0
    for i in range(len(basis_ids)):
        if basis_ids[i] in range(len(limits)):
            id = basis_ids[i]
            cnt = limits[basis_ids[i]][-1]
            print(f"Товар с индексом {id} по цене {basis_costs_ans[id]} нужен в количестве {cnt}")
            sum += basis_costs_ans[basis_ids[i]]*limits[basis_ids[i]][-1]
            print(f"{basis_costs_ans[basis_ids[i]]}*{limits[basis_ids[i]][-1]} = {basis_costs_ans[basis_ids[i]]*limits[basis_ids[i]][-1]}")
    print(f"Итоговая сумма: {sum}")

simplex_method()