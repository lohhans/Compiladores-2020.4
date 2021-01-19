# Compiladores-2020.4

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/b2473ced6948471386eb0d3564a336f2)](https://www.codacy.com/gh/lohhans/Compiladores-2020.4/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=lohhans/Compiladores-2020.4&amp;utm_campaign=Badge_Grade)

## Desenvolvido por

[![Armstrong L. M. G. Q.](https://avatars0.githubusercontent.com/u/30741312?s=64&v=4)](https://github.com/lohhans) |  [![Antônio A. S. N.](https://avatars1.githubusercontent.com/u/44072239?s=64&v=4)](https://github.com/laisy) |  
|-------------------|-------------------
| **Armstrong L. M. G. Q.** | **Laisy C. F. S.** |  |
| <a href="https://github.com/lohhans/Compiladores-2020.4/commits?author=lohhans" title="Commits de @lohhans">💻 @lohhans</a> | <a href="https://github.com/lohhans/Compiladores-2020.4/commits?author=laisy" title="Commits de @laisy">💻 @laisy</a> |

---

## Projeto de Compiladores - 2020.4

Implementação de um compilador para a disciplina de "[Compiladores][compiladores]", no curso de [Ciência da Computação na Universidade Federal do Agreste de Pernambuco][ufape]. Estruturas desenvolvidas conforme orientação da [Prof. Dra. Maria Aparecida A. Sibaldo][professora].

## Sobre o projeto

### Características da Gramática BNF

A gramática precisa ser LL(1).

Gramáticas LL(1) podem ser analisadas por um simples parser descentente recursivo e deve estar:

– Sem recursão a esquerda

– Fatorada a esquerda

– 1 símbolo de look-ahead

Além disso, a linguagem deve cobrir os seguintes aspectos:

- [x] Declaração de variáveis de tipo inteiro e booleano

- [x] Declaração de procedimentos e funções (sem e com parâmetros)

- [x] Comandos de atribuição

- [x] Chamada de procedimentos e funções

- [x] Comando de desvio condicional (if e else)

- [x] Comando de laço (while)

- [x] Comando de retorno de valor

- [x] Comandos de desvio incondicional (break e continue)

- [x] Comando de impressão de constante e variável na tela

- [ ] Expressões aritméticas (+, -, * e /)

- [x] Expressões booleanas (==, !=, >, >=, < e <=)

### Gramática BNF desenvolvida para o projeto

Para acessar a gramática, [clique aqui][gramatica]

<!-- Links -->
[compiladores]: https://sites.google.com/site/maasibaldo/home/compiladores-uag-ufrpe
[ufape]: http://www.ufape.edu.br/br/node/409
[professora]: https://sites.google.com/site/maasibaldo/home
[gramatica]: https://github.com/lohhans/Compiladores-2020.4/blob/main/Gram%C3%A1tica.bnf
