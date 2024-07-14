```markdown
# Kex Programming Language Documentation

Kex is a dynamically-typed, interpreted programming language designed for simplicity and ease of use. It supports basic arithmetic operations, variable assignments, and data structures like lists and dictionaries.

## Basic Syntax

### Data Types

Kex supports the following data types:
- **Integers**
- **Floats**
- **Strings** (enclosed in double quotes)
- **Booleans** (true and false)
- **Lists**
- **Dictionaries**

### Variables and Assignment

Variables in Kex are dynamically typed and can be assigned using the `=` operator:

```kex
x = 5
name = "Alice"
```

### Arithmetic Operations

Kex supports basic arithmetic operations:
- **Addition**: `+`
- **Subtraction**: `-`
- **Multiplication**: `*`
- **Division**: `/`

**Example:**

```kex
result = 10 + 5 * 2
```

### Lists

Lists are created using square brackets:

```kex
numbers = [1, 2, 3, 4, 5]
```

### Dictionaries

Dictionaries are created using curly braces:

```kex
person = {"name": "Bob", "age": 30}
```

### Comments

Kex supports both single-line and multi-line comments:

```kex
// This is a single-line comment

/*
This is a
multi-line comment
*/
```

## Language Features

- **Expression Evaluation**: Kex evaluates expressions and can handle nested arithmetic operations.
- **Variable Scope**: The language uses a simple symbol table for variable management, suggesting it has a global scope for variables.
- **Error Handling**: Basic error handling is implemented, including syntax errors and undefined variable errors.
- **Interactive Mode**: The language can be used in an interactive REPL (Read-Eval-Print Loop) mode.

## Limitations

Based on the current implementation, Kex has several limitations:
- No control structures (if/else, loops) are implemented.
- Functions are not supported.
- There's no module or import system.

## Usage

To use Kex, run the interpreter and input expressions or statements at the prompt:

```sh
kex> x = 10
kex> y = 20
kex> x + y
30
```

## Future Plans

- **Immediate (I)**: 
  - Feature Addition: Conditional Operators

- **Short Period (S)**: 
  - Feature Addition: Control Flow Statements
  - Feature Addition: Add Documentation Capability (docstring)

- **Long Run (L)**:
  - Feature Addition: File Handling
  - Feature Addition: Exception Handling
```

This markdown syntax provides a structured and clear README file for your Kex programming language. It includes headings, subheadings, and code snippets formatted using triple backticks for readability.
