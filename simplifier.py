import quinemccluskey

L_PAREN = '(';
R_PAREN = ')';
TRUE = "1";
FALSE = "0";
NOT = "!";
AND = "&";
OR = "|";
XOR = "^";
IMPL = ">";
EQ = "=";

operators = [NOT, AND, OR, XOR, IMPL, EQ];

def isOperator(character):
    if character not in operators:
        return False;
    return True;

def getAllVariables(expr):
    return sorted(set([i for i in expr if not isOperator(i) and i != TRUE and i != FALSE]));

#generate permutation
def genPermutations(variable_count):
    return [i for i in range(0, 2**variable_count)];

def operation2arg(operation, val1, val2):
    if operation is AND:
        return val1 and val2;
    elif operation is OR:
        return val1 or val2;
    elif operation is XOR:
        return val1 != val2;
    elif operation is IMPL:
        return (not val1) or val2;
    elif operation is EQ:
        return val1 == val2;

def getPriority(operation):
    if operation is NOT:
        return 5;
    elif operation is AND:
        return 3;
    elif operation is OR:
        return 2;
    elif operation is XOR:
        return 4;
    elif operation is IMPL:
        return 1;
    elif operation is EQ:
        return 0;

def rpn(expr):
    #  !a&b|(c>d|a)&b
    result = [];
    operators = [];
    for elem in expr:
        if elem == L_PAREN:
            operators.append(elem);
        elif elem == R_PAREN:
            top = operators.pop();
            while top != L_PAREN:
                result.append(top);
                top = operators.pop();
        elif isOperator(elem):
            if len(operators) != 0:
                top = operators.pop();
                if top == L_PAREN or getPriority(top) < getPriority(elem):
                    operators.append(top);
                else:
                    drawnAgain = False;
                    if len(operators) == 0:
                        result.append(top);
                    while len(operators) != 0 and top != L_PAREN and getPriority(top) > getPriority(elem):
                        drawnAgain = True;
                        result.append(top);
                        top = operators.pop();
                    if top == L_PAREN:
                        operators.append(top);
                    elif drawnAgain and getPriority(top) <= getPriority(elem):
                        operators.append(top);
                    elif drawnAgain:
                        result.append(top);


            operators.append(elem);
        else:
            result.append(elem);

    while operators != []:
        result.append(operators.pop());

    return result;

def evaluate(expr, variables, permutation):
    values = dict();
    for var in variables:
        values[var] = permutation % 2;
        permutation = permutation // 2;

    expression = [values.get(i, i) for i in expr];
    stack = [];
    for element in expression:
        if isOperator(element):
            if element == '!':
                val = bool(stack.pop());
                stack.append(not val);
            else:
                val2 = bool(stack.pop());
                val1 = bool(stack.pop());
                stack.append(operation2arg(element, val1, val2));
        else:
            stack.append(element);

    return bool(stack.pop());

def parseToList(expr):
    parsed = [];
    expr = "".join(list(filter(None, expr.split(" "))));
    prev = None;
    for c in expr:
        if isOperator(c):
            if prev != None:
                parsed.append(prev);
                prev = None;
            parsed.append(c);
        elif c == L_PAREN or c == R_PAREN:
            if prev != None:
                parsed.append(prev);
                prev = None;
            parsed.append(c);
        elif ( c == TRUE or c == FALSE ) and prev == None:
            parsed.append(c);
        else:
            if prev == None:
                prev = c;
            else:
                prev = prev + c;

    if prev != None:
        parsed.append(prev);

    return parsed;

if __name__ == "__main__":
    try:
        expr = parseToList(str(input()));
        rpnExpr = rpn(expr);
        print(rpnExpr);
        variables = getAllVariables(rpnExpr);
        permutations = genPermutations(len(variables));
        exprIsTruePerms = [perm for perm in permutations if evaluate(rpnExpr, variables, perm) is True];
        print(exprIsTruePerms);
        simplified = quinemccluskey.simplify(variables, exprIsTruePerms);
        print(simplified);
    except:
        print("Error - invalid expression..")