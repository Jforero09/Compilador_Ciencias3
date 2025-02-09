import os

# Verificación de extensión de archivo
def verificar_extension(archivo):
    print(f"Verificando extensión del archivo: {archivo}")
    if not archivo.endswith('.zlang'):
        raise ValueError("Error: El archivo debe tener la extensión .zlang.")

# Definición de tokens para el lexer
tokens = (
    'NUMERO_ENTERO', 'NUMERO_FLOTANTE', 'IDENTIFICADOR', 'OPERADOR_ARITMETICO',
    'OPERADOR_COMPARACION', 'OPERADOR_LOGICO', 'PALABRA_CLAVE',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'COMMA', 'SEMICOLON', 'ASIGNACION'
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
t_ASIGNACION = r'='
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
    print(f"Error léxico: Carácter no válido '{t.value[0]}' en la entrada.")
    raise SyntaxError(f"Error: Carácter no válido '{t.value[0]}' en la entrada.")
    t.lexer.skip(1)

# Implementación manual del lexer
class Lexer:
    def __init__(self, input_text):
        self.text = input_text
        self.position = 0
    
    def get_next_token(self):
        while self.position < len(self.text) and self.text[self.position].isspace():
            self.position += 1
        if self.position >= len(self.text):
            return None
        char = self.text[self.position]
        self.position += 1
        print(f"Analizando carácter: {char}")
        if char.isdigit():
            num = char
            while self.position < len(self.text) and self.text[self.position].isdigit():
                num += self.text[self.position]
                self.position += 1
            print(f"Token encontrado: NUMERO_ENTERO ({num})")
            return ('NUMERO_ENTERO', int(num))
        elif char.isalpha():
            ident = char
            while self.position < len(self.text) and self.text[self.position].isalnum():
                ident += self.text[self.position]
                self.position += 1
            if ident in ('if', 'else', 'while', 'for', 'return', 'function'):
                print(f"Token encontrado: PALABRA_CLAVE ({ident})")
                return ('PALABRA_CLAVE', ident)
            print(f"Token encontrado: IDENTIFICADOR ({ident})")
            return ('IDENTIFICADOR', ident)
        elif char == '=':
            print("Token encontrado: ASIGNACION (=)")
            return ('ASIGNACION', '=')
        elif char in '+-*/%':
            print(f"Token encontrado: OPERADOR_ARITMETICO ({char})")
            return ('OPERADOR_ARITMETICO', char)
        elif char == '(':
            return ('LPAREN', '(')
        elif char == ')':
            return ('RPAREN', ')')
        elif char == '{':
            return ('LBRACE', '{')
        elif char == '}':
            return ('RBRACE', '}')
        elif char == ',':
            return ('COMMA', ',')
        elif char == ';':
            return ('SEMICOLON', ';')
        else:
            print(f"Error léxico: Carácter inesperado '{char}'")
            raise SyntaxError(f"Error: Carácter no válido '{char}' en la entrada.")

# Implementación mejorada del parser
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        print(f"Primer token: {self.current_token}")
    
    def eat(self, token_type):
        print(f"Esperando token: {token_type}, Token actual: {self.current_token}")
        if self.current_token and self.current_token[0] == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise SyntaxError(f"Error de sintaxis: se esperaba '{token_type}'")
    
    def parse_parametros(self):
        parametros = []
        while self.current_token and self.current_token[0] == 'IDENTIFICADOR':
            parametros.append(self.current_token[1])
            self.eat('IDENTIFICADOR')
            if self.current_token and self.current_token[0] == 'COMMA':
                self.eat('COMMA')
            else:
                break
        return parametros
    
    def parse_bloque(self):
        print("Analizando bloque de código")
        while self.current_token and self.current_token[0] != 'RBRACE':
            print(f"Sentencia dentro del bloque: {self.current_token}")
            self.eat(self.current_token[0])
        self.eat('RBRACE')
    
    def parse_sentencia(self):
        if not self.current_token:
            raise SyntaxError("Error de sintaxis: sentencia inesperadamente vacía")
        print(f"Analizando sentencia con token: {self.current_token}")
        if self.current_token[0] == 'PALABRA_CLAVE' and self.current_token[1] == 'function':
            self.eat('PALABRA_CLAVE')
            nombre_funcion = self.current_token[1]
            self.eat('IDENTIFICADOR')
            self.eat('LPAREN')
            parametros = self.parse_parametros()
            self.eat('RPAREN')
            self.eat('LBRACE')
            self.parse_bloque()
            return ('FUNC_DEF', nombre_funcion, parametros)
        else:
            raise SyntaxError("Error de sintaxis en la sentencia")

# Verificación de archivo y prueba
def analizar_archivo(archivo):
    verificar_extension(archivo)
    with open(archivo, 'r') as f:
        codigo = f.read()
    print("Código cargado:")
    print(codigo)
    lexer = Lexer(codigo)
    parser = Parser(lexer)
    return parser.parse_sentencia()

# Prueba
archivo_prueba = "Ejemplos/ej1.zlang"
try:
    resultado = analizar_archivo(archivo_prueba)
    print("Análisis exitoso. Resultado:", resultado)
except Exception as e:
    print("Error durante el análisis:", e)