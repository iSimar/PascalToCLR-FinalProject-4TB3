# -*- coding: utf-8 -*-
"""
LAB 7 by Simarpreet Singh (1216728) and Jake Harwood (1226732)

Pascal0 Parser, Emil Sekerinski, February 2017,
Main program, type-checks, folds constants, calls scanner SC and code
generator CG, uses symbol table ST
"""

from sys import argv
import SC  #  used for SC.init, SC.sym, SC.val, SC.error
from SC import TIMES, DIV, MOD, AND, PLUS, MINUS, OR, EQ, NE, LT, GT, \
     LE, GE, PERIOD, COMMA, COLON, RPAREN, RBRAK, OF, THEN, DO, LPAREN, \
     LBRAK, NOT, BECOMES, NUMBER, IDENT, SEMICOLON, END, ELSE, IF, WHILE, \
     ARRAY, RECORD, CONST, TYPE, VAR, PROCEDURE, BEGIN, PROGRAM, EOF, \
     getSym, mark
import ST  #  used for ST.init
from ST import Var, Ref, Const, Type, Proc, StdProc, Int, Bool, Enum, \
     Record, Array, newObj, find, openScope, topScope, closeScope


# first and follow sets for recursive descent parsing

FIRSTFACTOR = {IDENT, NUMBER, LPAREN, NOT}
FOLLOWFACTOR = {TIMES, DIV, MOD, AND, OR, PLUS, MINUS, EQ, NE, LT, LE, GT, GE,
                COMMA, SEMICOLON, THEN, ELSE, RPAREN, RBRAK, DO, PERIOD, END}
FIRSTEXPRESSION = {PLUS, MINUS, IDENT, NUMBER, LPAREN, NOT}
FIRSTSTATEMENT = {IDENT, IF, WHILE, BEGIN}
FOLLOWSTATEMENT = {SEMICOLON, END, ELSE}
FIRSTTYPE = {IDENT, RECORD, ARRAY, LPAREN}
FOLLOWTYPE = {SEMICOLON}
FIRSTDECL = {CONST, TYPE, VAR, PROCEDURE}
FOLLOWDECL = {BEGIN}
FOLLOWPROCCALL = {SEMICOLON, END, ELSE}
STRONGSYMS = {CONST, TYPE, VAR, PROCEDURE, WHILE, IF, BEGIN, EOF}

from sys import stdout

MARKDOWN_OUTPUT = 0

if MARKDOWN_OUTPUT:
    indent = '&nbsp;'
else:
    indent = '  '

def write(s): stdout.write(s)
def writeln(): stdout.write('\n')

def bold(s):
    if MARKDOWN_OUTPUT:
        return '**'+s+'**'
    else:
        return s

def italic(s):
    if MARKDOWN_OUTPUT:
        return '*'+s+'*'
    else:
        return s



# parsing procedures

def selector(x):
    """
    Parses
        selector = {"." «write('.')» ident «write('*'+ident+'*')» | "[" write('[')» expression write(']')» "]"}.
    Assumes x is the entry for the identifier in front of the selector;
    generates code for the selector if no error is reported
    """
    while SC.sym in {PERIOD, LBRAK}:
        if SC.sym == PERIOD:  #  x.f
            write('.')
            getSym()
            if SC.sym == IDENT:
                if type(x.tp) == Record:
                    for f in x.tp.fields:
                        if f.name == SC.val:
                            write(italic(SC.val))
                            x = CG.genSelect(x, f); break
                    else: mark("not a field")
                    getSym()
                else: mark("not a record")
            else: mark("identifier expected")
        else:  #  x[y]
            write('[')
            getSym(); y = expression()
            if type(x.tp) == Array:
                if y.tp == Int:
                    if type(y) == Const and \
                       (y.val < x.tp.lower or y.val >= x.tp.lower + x.tp.length):
                        mark('index out of bounds')
                    else: x = CG.genIndex(x, y)
                else: mark('index not integer')
            else: mark('not an array')
            if SC.sym == RBRAK:
                write(']')
                getSym(); 
            else: mark("] expected")
    return x

def factor():
    """
    Parses
        factor = ident «write('*'+ident+'*')» selector |
                 integer «write(iinteger)» |
                 "(" «write('(')» expression ")" «write(')')» |
                 "not" «write('**not** ') factor.
    Generates code for the factor if no error is reported
    """
    if SC.sym not in FIRSTFACTOR:
        mark("expression expected"); getSym()
        while SC.sym not in FIRSTFACTOR | STRONGSYMS | FOLLOWFACTOR:
            getSym()
    if SC.sym == IDENT:
        x = find(SC.val)
        if type(x) in {Var, Ref}: x = CG.genVar(x)
        elif type(x) == Const: x = Const(x.tp, x.val); x = CG.genConst(x)
        else: mark('expression expected')
        write(italic(SC.val)); getSym(); x = selector(x)
    elif SC.sym == NUMBER:
        x = Const(Int, SC.val); x = CG.genConst(x); write(str(SC.val)); getSym()
    elif SC.sym == LPAREN:
        write('('); getSym(); x = expression()
        if SC.sym == RPAREN: write(')'); getSym()
        else: mark(") expected")
    elif SC.sym == NOT:
        write(bold('not')+' '); getSym(); x = factor()
        if x.tp != Bool: mark('not boolean')
        elif type(x) == Const: x.val = 1 - x.val # constant folding
        else: x = CG.genUnaryOp(NOT, x)
    else: x = Const(None, 0)
    return x

def term():
    """
    Parses
        term = factor {("*" «write('*')» | "div" «write('**div**')» | "mod" «write('**mod**')» | "and" «write('**and**')») factor}.
    Generates code for the term if no error is reported
    """
    x = factor()
    while SC.sym in {TIMES, DIV, MOD, AND}:
        op = SC.sym
        if op == TIMES:
            write(' * ')
        elif op == DIV:
            write(' '+bold('div')+' ')
        elif op == MOD:
            write(' '+bold('mod')+' ')
        elif op == AND:
            write(' '+bold('and')+' ')
        getSym()
        if op == AND and type(x) != Const: x = CG.genUnaryOp(AND, x)
        y = factor() # x op y
        if x.tp == Int == y.tp and op in {TIMES, DIV, MOD}:
            if type(x) == Const == type(y): # constant folding
                if op == TIMES: x.val = x.val * y.val
                elif op == DIV: x.val = x.val // y.val
                elif op == MOD: x.val = x.val % y.val
            else: x = CG.genBinaryOp(op, x, y)
        elif x.tp == Bool == y.tp and op == AND:
            if type(x) == Const: # constant folding
                if x.val: x = y # if x is true, take y, else x
            else: x = CG.genBinaryOp(AND, x, y)
        else: mark('bad type')
    return x

def simpleExpression():
    """
    Parses
        simpleExpression = ["+" «write('+')» | "-" «write('-')»] term {("+" «write('+')» | "-" «write('-')» | "or" «write('**or**')») term}.
    Generates code for the simpleExpression if no error is reported
    """
    if SC.sym == PLUS:
        write('+') 
        getSym(); x = term()
    elif SC.sym == MINUS:
        write('-') 
        getSym(); x = term()
        if x.tp != Int: mark('bad type')
        elif type(x) == Const: x.val = - x.val # constant folding
        else: x = CG.genUnaryOp(MINUS, x)
    else: x = term()
    while SC.sym in {PLUS, MINUS, OR}:
        op = SC.sym; getSym()
        if op == OR: 
            write(bold('or')) 
        if op == OR and type(x) != Const: x = CG.genUnaryOp(OR, x)
        y = term() # x op y
        if x.tp == Int == y.tp and op in {PLUS, MINUS}:
            if type(x) == Const == type(y): # constant folding
                if op == PLUS:
                    write('+') 
                    x.val = x.val + y.val
                elif op == MINUS:
                    write('-') 
                    x.val = x.val - y.val
            else: x = CG.genBinaryOp(op, x, y)
        elif x.tp == Bool == y.tp and op == OR:
            if type(x) == Const: # constant folding
                if not x.val: x = y # if x is false, take y, else x
            else: x = CG.genBinaryOp(OR, x, y)
        else: mark('bad type')
    return x

def expression():
    """
    Parses
        expression = simpleExpression
                     {("=" «write(' = ')» | "<>" «write(' <> ')» | "<" «write(' < ')» | "<=" «write(' <= ')» | ">" «write(' > ')» | ">=" «write(' >= ')») simpleExpression}.
    Generates code for the expression if no error is reported
    """
    x = simpleExpression()
    while SC.sym in {EQ, NE, LT, LE, GT, GE}:
        op = SC.sym
        if op == EQ:
            write(' = ')
        elif op == NE:
            write(' <> ')
        elif op == LT:
            write(' < ')
        elif op == LE:
            write(' <= ')
        elif op == GT:
            write(' > ')
        elif op == GE:
            write(' >= ')
        getSym(); y = simpleExpression() # x op y
        if x.tp == Int == y.tp:
            x = CG.genRelation(op, x, y)
        else: mark('bad type')
    return x

def compoundStatement(l):
    """
    Parses
        compoundStatement(l) =
            "begin" «writeln; write(l * indent + '**begin**')»
            statement(l + 1) {";" «write(';')» statement(l + 1)}
            "end" «writeln; write(l * ident + '**end**')»
    Generates code for the compoundStatement if no error is reported
    """
    if SC.sym == BEGIN: writeln(); write(l * indent + bold('begin')); getSym(l, indent)
    else: mark("'begin' expected")
    x = statement(l + 1)
    while SC.sym == SEMICOLON or SC.sym in FIRSTSTATEMENT:
        if SC.sym == SEMICOLON: write(';'); getSym(l, indent)
        else: mark("; missing")
        y = statement(l + 1); x = CG.genSeq(x, y)
    if SC.sym == END: writeln(); write(l * indent + bold('end')); getSym(l, indent)
    else: mark("'end' expected")
    return x

def statement(l):
    """
    Parses
        statement =
            ident «writeln; write(l * indent + ident)» selector ":=" «write(' := ')» expression |
            ident «write(l * indent + ident)» "(" «write('(')» [expression
                {"," «write(', ')» expression}] ")" «write(')')» |
            compoundStatement(l) |
            "if" «writeln; write(l * indent + '**if** ')» expression
                "then" «write(' **then**')» statement(l + 1)
                ["else" «writeln; write(l * indent + '**else**')» statement(l + 1)] |
           "while" «writeln; write((l*indent)+'**while** ')» expression "do" «write('**do**')»  statement.
    Generates code for the statement if no error is reported
    """
    if SC.sym not in FIRSTSTATEMENT:
        mark("statement expected"); getSym(l, indent)
        while SC.sym not in FIRSTSTATEMENT | STRONGSYMS | FOLLOWSTATEMENT:
            getSym(l, indent)
    if SC.sym == IDENT:
        x = find(SC.val)
        writeln()
        if type(x) != StdProc and x.name != 'read' and x.name != 'write' and x.name != 'writeln':
            write(l * indent + SC.val)
        getSym(l, indent)
        x = CG.genVar(x)
        if type(x) in {Var, Ref}:
            x = selector(x)
            if SC.sym == BECOMES:
                write(' := ')
                getSym(l, indent); y = expression()
                if x.tp == y.tp in {Bool, Int}: # and not SC.error: type(y) could be Type 
                    #if type(x) == Var: ### and type(y) in {Var, Const}: incomplete, y may be Reg
                        x = CG.genAssign(x, y)
                    #else: mark('illegal assignment')
                else: mark('incompatible assignment')
            elif SC.sym == EQ:
                mark(':= expected'); getSym(l, indent); y = expression()
            else: mark(':= expected')
        elif type(x) in {Proc, StdProc}:

            if type(x) == StdProc:
                if x.name == 'read':
                    write(l * indent + italic(x.name))
                elif x.name == 'write':
                    write(l * indent + italic(x.name))
                elif x.name == 'writeln':
                    write(l * indent + italic(x.name))

            fp, i = x.par, 0  #  list of formals, count of actuals
            if SC.sym == LPAREN:
                write('('); getSym(l, indent)
                if SC.sym in FIRSTEXPRESSION:
                    y = expression()
                    if i < len(fp):
                        if (type(fp[i]) == Var or type(y) == Var) and \
                           fp[i].tp == y.tp:
                            if type(x) == Proc: CG.genActualPara(y, fp[i], i)
                            i = i + 1
                        else: mark('illegal parameter mode')
                    else: mark('extra parameter')
                    while SC.sym == COMMA:
                        write(', '); getSym(l, indent)
                        y = expression()
                        if i < len(fp):
                            if (type(fp[i]) == Var or type(y) == Var) and \
                               fp[i].tp == y.tp:
                                if type(x) == Proc: CG.genActualPara(y, fp[i], i)
                                i = i + 1
                            else: mark('illegal parameter mode')
                        else: mark('extra parameter')
                if SC.sym == RPAREN: write(')'); getSym(l, indent)
                else: mark("')' expected")
            if i < len(fp): mark('too few parameters')
            if type(x) == StdProc:
                if x.name == 'read': x = CG.genRead(y)
                elif x.name == 'write': x = CG.genWrite(y)
                elif x.name == 'writeln': x = CG.genWriteln()
            else: x = CG.genCall(x)
        else: mark("variable or procedure expected")
    elif SC.sym == BEGIN: x = compoundStatement(l + 1)
    elif SC.sym == IF:
        writeln(); write(l * indent + bold('if') + ' '); getSym(l, indent); x = expression()
        if x.tp == Bool: x = CG.genCond(x)
        else: mark('boolean expected')
        if SC.sym == THEN: write(' '+bold('then')); getSym(l, indent)
        else: mark("'then' expected")
        y = statement(l + 1)
        if SC.sym == ELSE:
            if x.tp == Bool: y = CG.genThen(x, y)
            writeln(); write(l * indent + bold('else')); getSym(l, indent)
            z = statement(l + 1)
            if x.tp == Bool: x = CG.genIfElse(x, y, z)
        else:
            if x.tp == Bool: x = CG.genIfThen(x, y)
    elif SC.sym == WHILE:
        writeln()
        write((l*indent)+bold('while')+' ')
        getSym(l, indent); t = CG.genTarget(); x = expression()
        if x.tp == Bool: x = CG.genCond(x)
        else: mark('boolean expected')
        if SC.sym == DO:
            write(' '+bold('do'))
            getSym(l, indent)
        else: mark("'do' expected")
        y = statement(l+1)
        if x.tp == Bool: x = CG.genWhile(t, x, y)
    else: x = None
    return x

def typ(l = 1):
    """
    Parses
        type = ident «write('*'+ident+'*')» |
               "array" «writeln; write((l*indent)+'**array** ')» "[" «write('[')» expression ".." «write(' .')» «write('. ')» expression "]" «write(']')» "of" «write(' **of** ')» type |
               "record" «writeln; write((l*indent)+'**record** ') writeln;» typedIds {";" «write(';') writeln;» typedIds} "end" «writeln; write((l*indent)+'**end**')».
    Returns a type descriptor 
    """
    if SC.sym not in FIRSTTYPE:
        getSym(l, indent); mark("type expected")
        while SC.sym not in FIRSTTYPE | STRONGSYMS | FOLLOWTYPE:
            getSym(l, indent)
    if SC.sym == IDENT:
        ident = SC.val; write(italic(ident)); x = find(ident); getSym(l, indent)
        if type(x) == Type:
            x = Type(x.tp)
        else: mark('not a type'); x = Type(None)
    elif SC.sym == ARRAY:
        writeln()
        write((l*indent)+bold('array')+' ')
        getSym(l, indent)
        if SC.sym == LBRAK:
            write('[')
            getSym(l, indent)
        else: mark("'[' expected")
        x = expression()
        if SC.sym == PERIOD:
            write(' .')
            getSym(l, indent)
        else: mark("'.' expected")
        if SC.sym == PERIOD:
            write('. ')
            getSym(l, indent)
        else: mark("'.' expected")
        y = expression()
        if SC.sym == RBRAK:
            write(']')
            getSym(l, indent)
        else: mark("']' expected")
        if SC.sym == OF:
            write(' '+bold('of')+' ')
            getSym(l, indent)
        else: mark("'of' expected")
        z = typ(l+1).tp
        if type(x) != Const or x.val < 0:
            mark('bad lower bound'); x = Type(None)
        elif type(y) != Const or y.val < x.val:
            mark('bad upper bound'); y = Type(None)
        else: x = Type(CG.genArray(Array(z, x.val, y.val - x.val + 1)))
    elif SC.sym == RECORD:
        writeln()
        write((l*indent)+bold('record')+' ')
        writeln()
        getSym(l, indent); openScope(); typedIds(Var, l+1)
        while SC.sym == SEMICOLON:
            write(';')
            writeln()
            getSym(l, indent); typedIds(Var, l+1)
        if SC.sym == END:
            writeln()
            write((l*indent)+bold('end'))
            getSym(l, indent)
        else: mark("'end' expected")
        r = topScope(); closeScope()
        x = Type(CG.genRec(Record(r)))
    else: x = Type(None)
    return x

def typedIds(kind, l = 1):
    """
    Parses
        typedIds = «write(l*indent)» ident «write('*'+indent+'*')» {"," ident «write('*'+indent+'*')»} ":" type.
    Updates current scope of symbol table
    Assumes kind is Var or Ref and applies it to all identifiers
    Reports an error if an identifier is already defined in the current scope
    """
    write(l*indent)
    if SC.sym == IDENT: 
        tid = [SC.val]
        write(italic(SC.val)) 
        getSym(l, indent)
    else: mark("identifier expected"); tid = []
    while SC.sym == COMMA:
        getSym(l, indent)
        write(', ')
        if SC.sym == IDENT:
            write(italic(SC.val)) 
            tid.append(SC.val)
            getSym(l, indent)
        else: mark('identifier expected')
    if SC.sym == COLON:
        write(': ')
        getSym(l, indent); tp = typ(l+1).tp
        if tp != None:
            for i in tid: newObj(i, kind(tp))
    else: mark("':' expected")

def declarations(allocVar, l = 1):
    """
    Parses
        declarations =
            {"const" «writeln; write(l*indent + '**const**')» ident «writeln; write((l+1)*indent+'*'+ident+'*')» "=" «write(' = ')» expression ";" «write(';')»}
            {"type" «writeln; write(l*indent + '**type**')» ident «writeln; write((l+1)*indent + ident)»  "=" «write(' = ')» type ";" «write(';')»}
            {"var" «writeln; write(l*indent + '**var**') writeln;» typedIds ";" «write(';')»}
            {"procedure" «writeln; write((l*indent)+'**procedure** ')» ident «write(ident)» ["(" «write('(')» [["var" «write('var ')»] typedIds {";" «write('; ')» ["var" «write('var ')»] typedIds}] ")" «write(')')»] ";" «write(';')»
                declarations compoundStatement ";" «write(';')»}.
    Updates current scope of symbol table.
    Reports an error if an identifier is already defined in the current scope.
    For each procedure, code is generated
    """
    if SC.sym not in FIRSTDECL | FOLLOWDECL:
        getSym(l, indent); mark("'begin' or declaration expected")
        while SC.sym not in FIRSTDECL | STRONGSYMS | FOLLOWDECL: getSym(l, indent)
    while SC.sym == CONST:
        writeln()
        write(l*indent + bold('const'))
        getSym(l, indent)
        if SC.sym == IDENT:
            ident = SC.val
            writeln()
            write((l+1)*indent+italic(ident))
            getSym(l, indent)
            if SC.sym == EQ: 
                write(' = ')
                getSym(l, indent)
            else: mark("= expected")
            x = expression()
            if type(x) == Const: newObj(ident, x)
            else: mark('expression not constant')
        else: mark("constant name expected")
        if SC.sym == SEMICOLON:
            write(';')
            getSym(l, indent)
        else: mark("; expected")
    while SC.sym == TYPE:
        writeln()
        write(l*indent + bold('type'))
        getSym(l, indent)
        if SC.sym == IDENT:
            ident = SC.val
            writeln()
            write((l+1)*indent + ident)
            getSym(l, indent)
            if SC.sym == EQ:
                write(' = ')
                getSym(l, indent)
            else: mark("= expected")
            x = typ(l+2)
            newObj(ident, x)  #  x is of type ST.Type
            if SC.sym == SEMICOLON:
                write(';')
                getSym(l, indent)
            else: mark("; expected")
        else: mark("type name expected")
    start = len(topScope())
    while SC.sym == VAR:
        writeln()
        write(l*indent + bold('var'))
        writeln()
        getSym(l, indent); typedIds(Var, l+1)
        if SC.sym == SEMICOLON:
            write(';')
            getSym(l, indent)
        else: mark("; expected")
    varsize = allocVar(topScope(), start)
    while SC.sym == PROCEDURE:
        writeln()
        write((l*indent)+bold('procedure')+' ')
        getSym(l, indent)
        if SC.sym == IDENT:
            getSym(l, indent)
        else: mark("procedure name expected")
        ident = SC.val
        write(ident)
        newObj(ident, Proc([])) #  entered without parameters
        sc = topScope()
        CG.procStart(); openScope() # new scope for parameters and body
        if SC.sym == LPAREN:
            write('(')
            getSym(l, indent)
            if SC.sym in {VAR, IDENT}:
                if SC.sym == VAR:
                    write('var ')
                    getSym(l, indent); typedIds(Ref, 0)
                else: typedIds(Var, 0)
                while SC.sym == SEMICOLON:
                    write('; ')
                    getSym(l, indent)
                    if SC.sym == VAR:
                        write('var ')
                        getSym(l, indent); typedIds(Ref, 0)
                    else: typedIds(Var, 0)
            else: mark("formal parameters expected")
            fp = topScope()
            sc[-1].par = fp[:] #  procedure parameters updated
            if SC.sym == RPAREN:
                write(')')
                getSym(l, indent)
            else: mark(") expected")
        else: fp = []
        parsize = CG.genFormalParams(fp)
        if SC.sym == SEMICOLON:
            write(';')
            getSym(l, indent)
        else: mark("; expected")
        localsize = declarations(CG.genLocalVars, l+1)
        CG.genProcEntry(ident, parsize, localsize)
        x = compoundStatement(l+1); CG.genProcExit(x, parsize, localsize)
        closeScope() #  scope for parameters and body closed
        if SC.sym == SEMICOLON:
            write(';')
            getSym(l, indent)
        else: mark("; expected")
    return varsize

def program():
    """
    Parses
        program = "program" «write('**program** ')» ident «write('*'+ident+'*')»
            ";" «write(';')» declarations compoundStatement(1).
    Generates code if no error is reported
    """
    newObj('boolean', Type(Bool)); Bool.size = 4
    newObj('integer', Type(Int)); Int.size = 4
    newObj('true', Const(Bool, 1))
    newObj('false', Const(Bool, 0))
    newObj('read', StdProc([Ref(Int)]))
    newObj('write', StdProc([Var(Int)]))
    newObj('writeln', StdProc([]))
    CG.progStart()
    if SC.sym == PROGRAM: write(bold('program')+' '); getSym()
    else: mark("'program' expected")
    ident = SC.val
    if SC.sym == IDENT: write(italic(ident)); getSym()
    else: mark('program name expected')
    if SC.sym == SEMICOLON: write(';'); getSym()
    else: mark('; expected')
    declarations(CG.genGlobalVars); CG.progEntry(ident)
    x = compoundStatement(1)
    return CG.progExit(x)

def compileString(src, dstfn = None, target = 'mips'):
    """Compiles string src; if dstfn is provided, the code is written to that
    file, otherwise printed on the screen"""
    global CG
    #  used for init, genRec, genArray, progStart, genGlobalVars, \
    #  progEntry, progExit, procStart, genFormalParams, genActualPara, \
    #  genLocalVars, genProcEntry, genProcExit, genSelect, genIndex, \
    #  genVar, genConst, genUnaryOp, genBinaryOp, genRelation, genSeq, \
    #  genAssign, genCall, genRead, genWrite, genWriteln, genCond, \
    #  genIfThen, genThen, genIfElse, genTarget, genWhile
    if target == 'mips': import CGmips as CG
    elif target == 'ast': import CGast as CG
    elif target == 'pretty': import CGpretty as CG
    else: print('unknown target'); return
    SC.init(src)
    ST.init()
    CG.init()
    p = program()
    if p != None and not SC.error:
        if dstfn == None: print(p)
        else:
            with open(dstfn, 'w') as f: f.write(p);

def compileFile(srcfn):
    if srcfn.endswith('.p'):
        with open(srcfn, 'r') as f: src = f.read()
        dstfn = srcfn[:-2] + '.s'
        compileString(src, dstfn)
    else: print("'.p' file extension expected")

# sampe usage:
# import os
# os.chdir('/path/to/my/directory')
# compileFile('myprogram.p')
