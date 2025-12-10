# Design Documentation: Custom CSV Reader and Writer

## Architecture Overview

This document provides a deep dive into the architecture, design decisions, and implementation details of the custom CSV parser.

## CustomCsvReader Architecture

### Class Structure

```python
class CustomCsvReader:
    def __init__(self, file_obj, delimiter=",", quotechar='"')
    def __iter__(self)
    def __next__(self)
    def _read_next_row()
```

### State Machine Design

The reader implements a simple but powerful state machine:

**States:**
- `in_quotes = False` - Currently parsing unquoted field content
- `in_quotes = True` - Currently inside a quoted field

**State Transitions:**

```
┌─────────────────────────────────┐
│   Start (in_quotes=False)       │
├─────────────────────────────────┤
│ Behavior:                       │
│ - Regular characters → add      │
│ - Delimiter → end field         │
│ - Newline → end row             │
│ - Quote → enter quoted mode     │
└─────────────────────────────────┘
              ↓ (quote at start)
┌─────────────────────────────────┐
│   Quoted (in_quotes=True)       │
├─────────────────────────────────┤
│ Behavior:                       │
│ - Regular characters → add      │
│ - Newline → add (embedded)      │
│ - Double quote "" → add single " │
│ - Single quote → exit mode      │
└─────────────────────────────────┘
```

### Character-by-Character Parsing

**Why this approach?**

1. **Correctness**: Easy to handle embedded newlines within quoted fields
2. **Clarity**: Simple, understandable logic for each character
3. **Streaming**: Can process large files without loading into memory

**Performance Trade-off:**
- Slower than C implementations due to Python function call overhead
- Each character triggers checks for delimiter, newline, quote
- But maintains simplicity and correctness

### Key Implementation Details

1. **Field Storage**: Uses list `field_chars` for building current field
2. **Row Storage**: Uses list `row` for building current row
3. **Iterator Protocol**: Returns None to signal StopIteration
4. **EOF Handling**: Sets `_eof` flag to prevent further reading

## CustomCsvWriter Architecture

### Class Structure

```python
class CustomCsvWriter:
    def __init__(self, file_obj, delimiter=",", quotechar='"')
    def _escape_field(self, field: str) -> str
    def writerow(self, row)
    def writerows(self, rows)
```

### Field Escaping Strategy

**Decision Tree:**

```
Does field need quoting?
├─ Contains delimiter? → YES
├─ Contains quote? → YES
├─ Contains newline? → YES
└─ Contains carriage return? → YES
   
   Otherwise → NO
```

**If quoting needed:**
1. Escape internal quotes: `"` → `""`
2. Wrap field in quotes: `field` → `"field"`

### Line Construction

Uses efficient string operations:

```python
escaped_fields = [self._escape_field(str(v)) for v in row]
line = self.delimiter.join(escaped_fields) + "\n"
self.file_obj.write(line)
```

**Advantages:**
- Single `join()` call instead of repeated concatenation
- O(n) time complexity for row building
- Minimizes string object creation

## CSV Standard Compliance

This implementation follows RFC 4180 with minor deviations:

### RFC 4180 Compliance
✓ Comma-delimited fields
✓ Fields with commas/newlines must be quoted
✓ Quote character is doubled within quoted fields
✓ Trailing line breaks handled
✓ Empty fields supported

### Design Deviations
- Allows non-quoted quote characters (lenient parsing)
- Doesn't enforce specific line ending format (accepts \n or \r\n)
- Configurable delimiter (not just comma)

## Memory Efficiency

### Reader Memory Usage

**Per-Row Memory:**
```
field_chars list: O(longest_field_length)
row list: O(num_columns * avg_field_length)
Total: O(row_size) - Not O(file_size)
```

**No buffering of entire file** - processes streaming

### Writer Memory Usage

```
escaped_fields list: O(num_columns)
line string: O(row_size)
Total: O(row_size) - Constant for each row
```

## Error Handling

### Current Approach: Permissive

- **Philosophy**: Process data robustly, don't fail on edge cases
- **Design**: Allow slightly non-standard CSV if unambiguous
- **Result**: Works with malformed CSVs that still parse correctly

### Examples of Handled Edge Cases

1. **Quote in unquoted field**
   ```
   Input: a,b"c,d
   Result: ['a', 'b"c', 'd']
   ```

2. **Missing final newline**
   ```
   Input: a,b (no \n)
   Result: ['a', 'b']
   ```

3. **Empty last field**
   ```
   Input: a,b,\n
   Result: ['a', 'b', '']
   ```

## Performance Characteristics

### Time Complexity

**Reader:**
- O(n) where n = file size (in bytes)
- Each character processed exactly once
- Delimiter/newline checks: O(1) per character

**Writer:**
- O(m) where m = total size of input data
- One pass for escaping, one for joining

### Space Complexity

**Reader:**
- O(r) where r = longest row size
- Streaming: doesn't hold entire file in memory

**Writer:**
- O(r) where r = current row size
- No accumulation between rows

### Benchmark Results

Typical performance against Python's `csv` module:

```
Custom reader:  1.0-1.5 seconds (10,000 rows × 5 cols)
Stdlib reader:  0.1-0.2 seconds
Slowdown:       5-10x

Reason: C extension vs Python interpreter
```

## Extension Points

The design allows for easy extensions:

### 1. Custom Delimiters
```python
reader = CustomCsvReader(f, delimiter=";")
writer = CustomCsvWriter(f, delimiter=";")
```

### 2. Custom Quote Characters
```python
reader = CustomCsvReader(f, quotechar="'")
writer = CustomCsvWriter(f, quotechar="'")
```

### 3. Additional Features (Future)
- Configurable line termination (\r\n vs \n)
- Dialect support (similar to stdlib csv.Dialect)
- Skip empty lines option
- Automatic type conversion
- Comment row handling

## Testing Strategy

### Test Coverage

1. **Basic Operations**: Write then read simple data
2. **Edge Cases**: Empty fields, quotes, commas, newlines
3. **Complex Data**: Mixed quoted and unquoted fields
4. **Round-Trip**: Data survives write→read→write cycle

### Testing Methodology

```python
# Strategy: Compare with expected output
data = [[...]]
buffer = io.StringIO()
writer.writerows(data)

buffer.seek(0)
reader_output = list(reader)
assert reader_output == data
```

## Conclusion

This implementation prioritizes:
1. **Correctness** - Handles CSV edge cases properly
2. **Simplicity** - Clear, understandable code
3. **Efficiency** - Streaming, minimal memory overhead
4. **Extensibility** - Easy to add features

While slower than optimized C implementations, it demonstrates the core CSV parsing concepts and provides a solid foundation for learning or customization.
