
# Compiladores-2020.4

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/b2473ced6948471386eb0d3564a336f2)](https://www.codacy.com/gh/lohhans/Compiladores-2020.4/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=lohhans/Compiladores-2020.4&amp;utm_campaign=Badge_Grade)

## Desenvolvido por

[![Armstrong L. M. G. Q.](https://avatars0.githubusercontent.com/u/30741312?s=64&v=4)](https://github.com/lohhans) |  [![Antônio A. S. N.](https://avatars1.githubusercontent.com/u/44072239?s=64&v=4)](https://github.com/laisy) |  
|-------------------|-------------------|-------------------|
| **Armstrong L. M. G. Q.** | **Laisy C. F. S.** |  |
| <a href="https://github.com/lohhans/Compiladores-2020.4/commits?author=lohhans" title="Code">💻 @lohhans</a> | <a href="https://github.com/lohhans/Compiladores-2020.4/commits?author=laisy" title="Code">💻 @laisy</a> |

---

## Projeto de Compiladores - 2020.4

Implementação de um compilador para a disciplina de "[Compiladores][COMP]", no curso de [Ciência da Computação na Universidade Federal do Agreste de Pernambuco][UFAPE]. Estruturas desenvolvidas conforme orientação da [Prof. Dra. Maria Aparecida A. Sibaldo][professora].

## Sobre o projeto

### Características da Gramática BNF

A gramática precisa ser LL(1).

Gramáticas LL(1) podem ser analisadas por um simples parser descentente recursivo e deve estar:

– Sem recursão a esquerda

– Fatorada a esquerda

– 1 símbolo de look-ahead

Além disso, a linguagem deve cobrir os seguintes aspectos:

    Declaração de variáveis de tipo inteiro e booleano

    Declaração de procedimentos e funções (sem e com parâmetros)

    Comandos de atribuição

    Chamada de procedimentos e funções

    Comando de desvio condicional (if e else)

    Comando de laço (while)

    Comando de retorno de valor

    Comandos de desvio incondicional (break e continue)

    Comando de impressão de constante e variável na tela

    Expressões aritméticas (+, -, * e /)

    Expressões booleanas (==, !=, >, >=, < e <=)

### Gramática BNF desenvolvida

Para acessar a gramática, [clique aqui][GRAM]

<!-- Links -->
[COMP]: https://sites.google.com/site/maasibaldo/home/compiladores-uag-ufrpe
[UFAPE]: http://www.ufape.edu.br/br/node/409
[professora]: https://sites.google.com/site/maasibaldo/home
[GRAM]: https://github.com/lohhans/Compiladores-2020.4/blob/main/Gram%C3%A1tica.bnf
