"""Custom CSV Reader and Writer Implementation.

This module provides custom CSV reader and writer classes.
"""


class CustomCsvReader:
    """Custom CSV reader implemented as an iterator."""

    def __init__(self, file_obj, delimiter=",", quotechar='"'):
        self.file_obj = file_obj
        self.delimiter = delimiter
        self.quotechar = quotechar
        self._eof = False

    def __iter__(self):
        return self

    def __next__(self):
        row = self._read_next_row()
        if row is None:
            raise StopIteration
        return row

    def _read_next_row(self):
        """Parse and return the next CSV row as a list of strings."""
        if self._eof:
            return None

        in_quotes = False
        field_chars = []
        row = []

        while True:
            ch = self.file_obj.read(1)

            if ch == "":
                if in_quotes:
                    row.append("".join(field_chars))
                elif field_chars or row:
                    row.append("".join(field_chars))
                else:
                    self._eof = True
                    return None
                self._eof = True
                return row

            if ch == self.quotechar:
                if in_quotes:
                    next_ch = self.file_obj.read(1)
                    if next_ch == self.quotechar:
                        field_chars.append(self.quotechar)
                    else:
                        in_quotes = False
                        if next_ch == self.delimiter:
                            row.append("".join(field_chars))
                            field_chars = []
                        elif next_ch in ("\n", "\r"):
                            row.append("".join(field_chars))
                            return row
                        elif next_ch == "":
                            row.append("".join(field_chars))
                            self._eof = True
                            return row
                        else:
                            field_chars.append(next_ch)
                else:
                    if not field_chars:
                        in_quotes = True
                    else:
                        field_chars.append(ch)
                continue

            if ch == self.delimiter and not in_quotes:
                row.append("".join(field_chars))
                field_chars = []
                continue

            if ch in ("\n", "\r") and not in_quotes:
                row.append("".join(field_chars))
                return row

            field_chars.append(ch)


class CustomCsvWriter:
    """Custom CSV writer for lists of lists."""

    def __init__(self, file_obj, delimiter=",", quotechar='"'):
        self.file_obj = file_obj
        self.delimiter = delimiter
        self.quotechar = quotechar

    def _escape_field(self, field: str) -> str:
        """Return field with proper quoting and escaping applied."""
        needs_quotes = (
            self.delimiter in field
            or self.quotechar in field
            or "\n" in field
            or "\r" in field
        )
        if needs_quotes:
            escaped = field.replace(self.quotechar, self.quotechar * 2)
            return f'{self.quotechar}{escaped}{self.quotechar}'
        return field

    def writerow(self, row):
        """Write a single CSV row."""
        escaped_fields = [self._escape_field(str(value)) for value in row]
        line = self.delimiter.join(escaped_fields) + "\n"
        self.file_obj.write(line)

    def writerows(self, rows):
        """Write multiple CSV rows."""
        for row in rows:
            self.writerow(row)
