
def int2list(integ):
    return integ

#parse int to bin_list without 0b pefix
def parse2bin(perm, length):
    reversePerm = list(reversed(bin(perm)[2:].zfill(length)));
    res = []
    for i in range(0, length):
        res += reversePerm[i];
    return res;

#counts occurences of "1" in given permutation
def count_ones(perm):
    return len([bit for bit in perm if bit == "1"]);

def diff_key_elems(key1, key2, length):
    key1list = sorted(key1);
    key2list = sorted(key2);
    for elem1 in key1list:
        if elem1 in key2list:
            return False;
    return True;

def is_subset_key(key1, key2):
    if isinstance(key1, int) and isinstance(key2, int):
        if key1 != key2:
            return False;
    elif isinstance(key2, tuple) and isinstance(key1, int):
        key2list = sorted(key2);
        if key1 not in key2list:
            return False;

    elif isinstance(key2, tuple) and isinstance(key1, tuple):
        key1list = sorted(key1);
        key2list = sorted(key2);
        if len(key1list) <= len(key1list):
            for elem1 in key1list:
                if elem1 not in key2list:
                    return False;
    return True;


def diff_expr(expr1, expr2, length):
    diff_count = 0;
    idx = -1
    for i in range(0, length):
        if expr1[i] != expr2[i] and (expr1[i] != "-" or expr2[i] != "-"):
            if diff_count == 0:
                idx = i;
            diff_count +=1

    return (diff_count, idx)


def nextStepMinimization(matched, var_counter):
    matched_key_len = len(matched.keys());
    furtherMatched = dict();
    checked = dict();
    for key in matched.keys():
        checked[key] = False;

    groups = [[] for i in range(0, var_counter + 1)]
    [groups[count_ones(matched.get(key))].append(key) for key in matched.keys()];
    #print("Groups: " + str(groups))
    if len(groups[0]) == matched_key_len:
        return (matched, {x: matched.get(x) for x in checked});

    for i in range(0, var_counter):
        if groups[i+1] != []:
            for key1 in groups[i]:
                for key2 in groups[i+1]:
                    if diff_key_elems(key1, key2, len(key1)):
                        expr1 = matched.get(key1);
                        expr2 = matched.get(key2);
                        (diff_counter, idx) = diff_expr(expr1, expr2, var_counter);
                        if diff_counter == 1:
                            checked[key1] = True;
                            checked[key2] = True;
                            expr1[idx] = "-";
                            newKey = tuple(sorted(key1 + key2));
                            if furtherMatched.get(newKey, lambda x : None) != None:
                                furtherMatched[newKey] = expr1;

    notChecked = {x : matched.get(x) for x in checked.keys() if checked[x] == False}
    return (furtherMatched, notChecked);

def combination_reduction(variables, permutations, notChecked):
    var_count = len(variables);
    expressions = [];
    coverByExpr = [];
    exprPermCoverCount = [];
    permCovered = { perm : False for perm in permutations };
    coverByPerm = {perm : [] for perm in permutations};
    for key, elem in notChecked.items():
        expr = str();
        for i in range(0, var_count):
            if i != 0 and elem[i] != "-" and len(expr) > 0:
                expr += "& "
            if elem[i] == "1":
                expr += str(variables[i] + " ");
            elif elem[i] == '0':
                expr += str("!" + variables[i] + " ");

        expressions.append(expr);
        if isinstance(key, tuple):
            keylist = list(tuple(key))
            coverByExpr.append(keylist);
            exprPermCoverCount.append(len(keylist));
        elif isinstance(key, int):
            tmpList = [];
            tmpList.append(key);
            coverByExpr.append(tmpList);
            exprPermCoverCount.append(1);

    expressions_len = len(expressions);
    usedExpr = [False for expr in expressions];

    for i in range(0, expressions_len):
        for perm in coverByExpr[i]:
            prev = coverByPerm.get(perm);
            tmpList = [];
            tmpList.append(i);
            coverByPerm[perm] = prev + tmpList;

    for key, val in coverByPerm.items():
        if val == []:
            return "";
        elif len(val) == 1:
            usedExpr[val[0]] = True;
            for perm in coverByExpr[val[0]]:
                if not permCovered[perm]:
                    permCovered[perm] = True;

        for i in range(0, expressions_len):
            if not usedExpr[i]:
                count = 0;
                for perm in coverByExpr[i]:
                    if not permCovered[perm]:
                        count += 1;
                exprPermCoverCount[i] = count;

    while False in permCovered.values():
        curr_max_idx = -1;
        for i in range(0, expressions_len):
            if not usedExpr[i]:
                curr_max_idx = i;
        for i in range(0, expressions_len):
            if not usedExpr[i] and exprPermCoverCount[curr_max_idx] < exprPermCoverCount[i]:
                curr_max_idx = i;
        usedExpr[curr_max_idx] = True;
        for perm in coverByExpr[curr_max_idx]:
            permCovered[perm] = True;
        for i in range(0, expressions_len):
            if not usedExpr[i]:
                count = 0;
                for perm in coverByExpr[i]:
                    if not permCovered[perm]:
                        count += 1;
                exprPermCoverCount[i] = count;
        print(usedExpr, exprPermCoverCount);

    result = str();
    for i in range(0, expressions_len):
        if usedExpr[i] is True:
            if i != 0 and len(result) > 0:
                result += "| ";
            result += expressions[i];

    return result;

# ( list_of_all_variables, list_of_permutations_where_expression_is_true )
def simplify(variables, permutations):
    var_count = len(variables);
    groups = [[] for i in range(0, var_count + 1)];
    if len(permutations) == 1:
        res = str();
        binary = parse2bin(permutations[0], var_count)
        for i in range(0, var_count):
            if i != 0 and len(res) > 0:
                res += "& "
            if binary[i] == "1":
                res += str(variables[i] + " ");
            elif binary[i] == '0':
                res += str("!" + variables[i] + " ");
        return res;

    [groups[count_ones(bin(perm))].append(perm) for perm in permutations];
    for group in groups:
        if len(group) == len(permutations):
            res = str();
            binary = parse2bin(permutations[0], var_count)
            for i in range(0, var_count):
                if i != 0 and len(res) > 0:
                    res += "& "
                if binary[i] == "1":
                    res += str(variables[i] + " ");
                elif binary[i] == '0':
                    res += str("!" + variables[i] + " ");
            return res;

    checked = dict();
    for perm in permutations:
        checked[perm] = False;
    matched = dict();

    for i in range(0, var_count):
        if groups[i+1] != []:
            for perm1 in groups[i]:
                for perm2 in groups[i+1]:
                    bit_diff = perm1 ^ perm2
                    if count_ones(bin(bit_diff)) == 1:
                        checked[perm1] = True;
                        checked[perm2] = True;
                        idx = 0;
                        matchedExpr = parse2bin(perm1, var_count);
                        tmpPerm2 = parse2bin(perm2, var_count);
                        while tmpPerm2[idx] == matchedExpr[idx] and idx < var_count:
                            idx += 1;
                        matchedExpr[idx] = "-";
                        matched[(perm1, perm2)] = matchedExpr;

    notChecked = {x : parse2bin(x, var_count) for x in list(filter(lambda x : not checked[x], permutations))}
    is_minimized = False;
    while not is_minimized:
        (furtherMinimized, additionalNotChecked) = nextStepMinimization(matched, var_count);
        if matched.keys() == furtherMinimized.keys():
            is_minimized = True;
        else:
            matched = furtherMinimized;
        notChecked.update(additionalNotChecked);

    notCheckedUp = dict();
    for key in notChecked.keys():
        canAdd = True;
        for sndKey in notChecked.keys():
            if key != sndKey and is_subset_key(key, sndKey):
                canAdd = False
        if canAdd:
            notCheckedUp[key] = notChecked[key];

    #print(notCheckedUp)

    return combination_reduction(variables, permutations, notCheckedUp);

if __name__ == "__main__":
    simplify = simplify;