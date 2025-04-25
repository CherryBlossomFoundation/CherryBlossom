
# Cherry Blossom
![Titelloses 62_20250412233842](https://github.com/user-attachments/assets/75eabf75-6376-4b70-9efd-837ef50059b5)

[![Build Cherry Blossom Compiler](https://github.com/CherryBlossomFoundation/CherryBlossom/actions/workflows/build-release.yml/badge.svg)](https://github.com/CherryBlossomFoundation/CherryBlossom/actions/workflows/build-release.yml)
[![Build Snapshot Cherry](https://github.com/CherryBlossomFoundation/CherryBlossom/actions/workflows/build-snapshot.yml/badge.svg)](https://github.com/CherryBlossomFoundation/CherryBlossom/actions/workflows/build-snapshot.yml)

**Cherry Blossom** is a statically-typed, compiled programming language that treats code as an art form. Designed with strict type discipline and elegant syntax, it prioritizes beauty and safety equally.

- **Strict typing** — no type inference allowed.
- **Beautiful syntax** — every line of code should look like a work of art.
- **Result type with `fall`** — graceful error handling.
- **Safe by design** — no hidden behavior or implicit conversions.

```cb
f greet(name: str) -> str {
    "Hello, " + name + "!";
}

begin main

printnl(greet("world"))
    
end
```

## Features

- `branch` expressions instead of `match`.

## Philosophy

> Code should be as beautiful as cherry blossoms.  
> — Cherry Blossom Design Principle

Cherry Blossom avoids type inference on purpose. Every type must be explicitly stated, encouraging clear, maintainable, and robust code.

## Getting Started

### Requirements

- `gcc` for backend compilation

### Build and Run

```bash
cherry <target.cb>
