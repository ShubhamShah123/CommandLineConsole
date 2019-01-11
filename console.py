# Shah Shubham
# sbs8554
# 2018-09-08

#---------#---------#---------#---------#---------#--------#
# 2018-08-06:  Copied from https://github.com/dabeaz/ply
# 2018-09-08:  Added reading commands from file.
#---------#---------#---------#---------#---------#--------#

#---------#---------#---------#---------#---------#--------#
# Lexical analysis section.

tokens = (
		'NAME', 'NUMBER',
		'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS', 'MODULUS', 'EXPONENTIATION',
		'LPAREN', 'RPAREN',
)

# Tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_MODULUS = r'%'
t_EXPONENTIATION = r'\^'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'


def t_NUMBER(t):
		r'\d+'
		t.value = int(t.value)

		return t


# Ignored characters
t_ignore = ' \t'

# Eats characters from the # character to the of the input.


def t_comment(t):
		r'\#.*'


def t_newline(t):
		r'\n+'
		t.lexer.lineno += t.value.count("\n")


def t_error(t):
		print('Illegal character "%s".' % t.value[0])
		t.lexer.skip(1)


# Build the lexer
import ply.lex as lex
lexer = lex.lex()

#---------#---------#---------#---------#---------#--------#
# Syntactic section.

# Precedence rules for the arithmetic operators
precedence = (
		('left',  'PLUS', 'MINUS'),
		('left',  'TIMES', 'DIVIDE', 'MODULUS'),
		('right', 'EXPONENTIATION'),
		('right', 'UMINUS'),
)

# Dictionary of names (for storing variables)
names = dict()


def p_statement_assign(p):
		'statement : NAME EQUALS expression'
		names[p[1]] = p[3]


def p_statement_expr(p):
		'statement : expression'
		print(p[1])


def p_expression_binop(p):
		'''expression : expression PLUS expression
									| expression MINUS expression
									| expression TIMES expression
									| expression DIVIDE expression
									| expression MODULUS expression'''
		if p[2] == '+':
				p[0] = p[1] + p[3]
		elif p[2] == '-':
				p[0] = p[1] - p[3]
		elif p[2] == '*':
				p[0] = p[1] * p[3]
		elif p[2] == '/':
				p[0] = p[1] / p[3]
		elif p[2] == '%':
				p[0] = p[1] % p[3]


def p_expression_uminus(p):
		'expression : MINUS expression %prec UMINUS'
		p[0] = -p[2]

def p_expression_exponentiation(p):
		'expression : expression EXPONENTIATION expression'
		p[0] = p[1] ** p[3]

def p_expression_group(p):
		'expression : LPAREN expression RPAREN'
		p[0] = p[2]


def p_expression_number(p):
		'expression : NUMBER'
		p[0] = p[1]


def p_expression_name(p):
		'expression : NAME'

		try:
				p[0] = names[p[1]]

		except LookupError:
				print('Undefined name "%s".' % p[1])
				p[0] = 0


def p_error(p):
		if p is None:
				# If the input string is just a comment, ignore it.
				if len(lexer.lexdata) > 0 and lexer.lexdata[0] != '#':
						# Not just a comment, so wanted token and didn't get one.
						print('Syntax error: end of input.')

		else:
				# Saw unexpected token.  Punt.
				print('Syntax error at "%s".' % p.value)


# Build the parser
import ply.yacc as yacc
parser = yacc.yacc()

#---------#---------#---------#---------#---------#--------#


def _main(inputFile=None):
		if inputFile is None:
				# No input file, so get lines one-by-one from the console.
				index = 0

				while True:
						index += 1
						try:
								line = input('calc<%d> ' % index)

								# Get rid of leading/trailing whitespace.
								line = line.strip()

						except EOFError:
								# User terminated session with EOF.
								break

						# Process the line only if there are some characters.
						if len(line) > 0:
								parser.parse(line)

		else:
				# Get the contents of the input file as a list of
				# individual lines.  Strip out carriage-return
				# characters (file might have come from Windows).
				with open(inputFile, 'r') as fp:
						lines = fp.read().replace('\r', '').split('\n')

				# Process each line independently.  index is the line's
				# number (from the beginning of the file).
				for (index, line) in enumerate(lines, start=1):
						# Get rid of leading/trailing whitespace.
						line = line.strip()

						# Process the line only if there are some characters.
						if len(line) > 0:
								# Echo the string before processing it.
								print('calc<%d> %s' % (index, line))
								parser.parse(line)


#---------#---------#---------#
if __name__ == '__main__':
		import sys

		# User might have supplied a file of lines to process as
		# the first command-line argument.
		inputFile = sys.argv[1] if len(sys.argv) > 1 else None

		_main(inputFile)

#---------#---------#---------#---------#---------#--------#
