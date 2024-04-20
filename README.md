# logcomp-2024-1

Jerônimo de Abreu Afrange

![git status](http://3.129.230.99/svg/jeronimo-a/logcomp-2024-1)

## EBNF
```
digit = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9";

letter = "A" | "B" | "C" | "D" | "E" | "F" | "G"
       | "H" | "I" | "J" | "K" | "L" | "M" | "N"
       | "O" | "P" | "Q" | "R" | "S" | "T" | "U"
       | "V" | "W" | "X" | "Y" | "Z" | "a" | "b"
       | "c" | "d" | "e" | "f" | "g" | "h" | "i"
       | "j" | "k" | "l" | "m" | "n" | "o" | "p"
       | "q" | "r" | "s" | "t" | "u" | "v" | "w"
       | "x" | "y" | "z" ;

symbol = "[" | "]" | "{" | "}" | "(" | ")" | "<" | ">"
       | "'" | '"' | "=" | "|" | "." | "," | ";" | "-" 
       | "+" | "*" | "?" | "\n" | "\t" | "\r" | "\f" | "\b" ;

num   = digit, {digit};
ident = letter, {digit | letter | "_"};
str   = {digit | letter | symbol};

BLOCK = {STAT};

FACTOR = num | str | ident | ("+" | "-" | "not", FACTOR) | ("(", B_EXPRESSION, ")") | ("read", "(", ")");

TERM         = FACTOR, {("/" | "*"), FACTOR};
EXPPRESSION  = TERM, {("+" | "-" | ".."), TERM};
R_EXPRESSION = EXPRESSION, {("==" | ">" | "<"), EXPRESSION};
B_TERM       = R_EXPRESSION, {"and", R_EXPRESSION};
B_EXPRESSION = B_TERM, {"or", B_TERM};

STAT_IDENT    = ident, "=", B_EXPRESSION;
STAT_PRINT    = "print", "(", B_EXPRESSION, ")";
STAT_WHILE    = "while", B_EXPRESSION, "do", "\n", {STAT};
STAT_IF       = "if", B_EXPRESSION, "then", "\n", {STAT}, ["else", "\n", {STAT}];
STAT_LOCAL    = "local", ident, ["=", B_EXPRESSION];

STAT = [STAT_IDENT | STAT_PRINT | ((STAT_WHILE | STAT_IF), "end") | STAT_LOCAL], "\n";
```

## Diagrama Sintático
![image](diagrama_sintatico.png)