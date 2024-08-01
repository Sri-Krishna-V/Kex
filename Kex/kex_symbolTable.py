class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def get(self, name):
        return self.symbols.get(name)

    def set(self, name, value):
        self.symbols[name] = value

    def delete(self, name):
        return self.symbols.pop(name, None)

    def __repr__(self):
        return f'SymbolTable({self.symbols})'

    def __str__(self):
        return str(self.symbols)

    def __len__(self):
        return len(self.symbols)

    def __iter__(self):
        return iter(self.symbols)

    def __contains__(self, name):
        return name in self.symbols

    def __getitem__(self, name):
        return self.get(name)

    def __setitem__(self, name, value):
        self.set(name, value)

    def __delitem__(self, name):
        del self.symbols[name]

    def __eq__(self, other):
        if isinstance(other, SymbolTable):
            return self.symbols == other.symbols
        return False

    def __ne__(self, other):
        return not self == other

    def __bool__(self):
        return bool(self.symbols)

    def clear(self):
        self.symbols.clear()

    def copy(self):
        new_table = SymbolTable()
        new_table.symbols = self.symbols.copy()
        return new_table

    def update(self, other):
        if isinstance(other, SymbolTable):
            self.symbols.update(other.symbols)
        elif isinstance(other, dict):
            self.symbols.update(other)
        else:
            raise TypeError("Can only update from SymbolTable or dict")
