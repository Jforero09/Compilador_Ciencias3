import ply.lex as lex
import ply.yacc as yacc
import os

# Verificación de extensión de archivo
def verificar_extension(archivo):
    if not archivo.endswith('.zlang'):
        raise ValueError("Error: El archivo debe tener la extensión .zlang.")

# Definición de tokens para el lexer
tokens = (
    'NUMERO_ENTERO', 'NUMERO_FLOTANTE', 'IDENTIFICADOR', 'OPERADOR_ARITMETICO',
    'OPERADOR_COMPARACION', 'OPERADOR_LOGICO', 'PALABRA_CLAVE',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'COMMA', 'SEMICOLON'
)

# Reglas de expresiones regulares para tokens simples
t_OPERADOR_ARITMETICO = r'[+\-*/%]'
t_OPERADOR_COMPARACION = r'(==|!=|<=|>=|<|>)'
t_OPERADOR_LOGICO = r'(&&|\|\|)'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_SEMICOLON = r';'
t_ignore = ' \t'

def t_NUMERO_FLOTANTE(t):
    r'\d+\.\d* | \d*\.\d+'
    t.value = float(t.value)
    return t

def t_NUMERO_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in ('if', 'else', 'while', 'for', 'return', 'function'):
        t.type = 'PALABRA_CLAVE'
    return t

def t_error(t):
    raise SyntaxError(f"Error: Carácter no válido '{t.value[0]}' en la entrada.")
    t.lexer.skip(1)

lexer = lex.lex()

# Definición de la gramática
precedence = (
    ('left', 'OPERADOR_ARITMETICO'),
    ('left', 'OPERADOR_COMPARACION'),
    ('left', 'OPERADOR_LOGICO')
)

def p_expresion_binaria(p):
    '''expresion : expresion OPERADOR_ARITMETICO expresion
                 | expresion OPERADOR_COMPARACION expresion
                 | expresion OPERADOR_LOGICO expresion'''
    p[0] = ('BINOP', p[2], p[1], p[3])

def p_expresion_numero(p):
    '''expresion : NUMERO_ENTERO
                 | NUMERO_FLOTANTE'''
    p[0] = ('NUM', p[1])

def p_expresion_identificador(p):
    'expresion : IDENTIFICADOR'
    p[0] = ('VAR', p[1])

def p_sentencia_asignacion(p):
    'sentencia : IDENTIFICADOR "=" expresion SEMICOLON'
    p[0] = ('ASIGN', p[1], p[3])

def p_sentencia_if(p):
    'sentencia : PALABRA_CLAVE LPAREN expresion RPAREN LBRACE sentencias RBRACE'
    p[0] = ('IF', p[3], p[6])

def p_sentencia_while(p):
    'sentencia : PALABRA_CLAVE LPAREN expresion RPAREN LBRACE sentencias RBRACE'
    p[0] = ('WHILE', p[3], p[6])

def p_sentencia_for(p):
    'sentencia : PALABRA_CLAVE LPAREN sentencia expresion SEMICOLON expresion RPAREN LBRACE sentencias RBRACE'
    p[0] = ('FOR', p[3], p[4], p[6], p[9])

def p_sentencia_funcion(p):
    'sentencia : PALABRA_CLAVE IDENTIFICADOR LPAREN parametros RPAREN LBRACE sentencias RBRACE'
    p[0] = ('FUNC', p[2], p[4], p[7])

def p_parametros(p):
    '''parametros : IDENTIFICADOR
                  | IDENTIFICADOR COMMA parametros
                  | empty'''
    if len(p) == 2:
        p[0] = [p[1]] if p[1] else []
    else:
        p[0] = [p[1]] + p[3]

def p_sentencias(p):
    '''sentencias : sentencia
                  | sentencia sentencias'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_empty(p):
    'empty :'
    p[0] = None

def p_error(p):
    if p:
        raise SyntaxError(f"Error de sintaxis cerca de '{p.value}'")
    else:
        raise SyntaxError("Error de sintaxis: entrada inesperada.")

parser = yacc.yacc()

# Verificación de archivo y prueba
def analizar_archivo(archivo):
    verificar_extension(archivo)
    with open(archivo, 'r') as f:
        codigo = f.read()
    return parser.parse(codigo)

# Prueba
archivo_prueba = "C:\Users\Usuario\Desktop\Compilador_Ciencias 3\Ejemplos\ej1.zlang"
try:
    resultado = analizar_archivo(archivo_prueba)
    print("Análisis exitoso. Resultado:", resultado)
except Exception as e:
    print("Error durante el análisis:", e)