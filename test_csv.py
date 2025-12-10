"""Test suite for custom CSV reader and writer."""

import io
from custom_csv import CustomCsvReader, CustomCsvWriter


def test_basic_writing():
    """Test basic CSV writing."""
    data = [
        ['Name', 'Age', 'City'],
        ['Alice', '30', 'New York'],
        ['Bob', '25', 'San Francisco']
    ]
    
    buffer = io.StringIO()
    writer = CustomCsvWriter(buffer)
    writer.writerows(data)
    
    result = buffer.getvalue()
    assert 'Name,Age,City' in result
    assert 'Alice,30,New York' in result
    print("✓ test_basic_writing passed")


def test_quoted_fields():
    """Test writing and reading fields with special characters."""
    data = [
        ['Name', 'Description'],
        ['Product A', 'Item with, comma'],
        ['Product B', 'Item with "quotes"']
    ]
    
    buffer = io.StringIO()
    writer = CustomCsvWriter(buffer)
    writer.writerows(data)
    
    buffer.seek(0)
    reader = CustomCsvReader(buffer)
    rows = list(reader)
    
    assert rows[0] == ['Name', 'Description']
    assert rows[1] == ['Product A', 'Item with, comma']
    assert rows[2] == ['Product B', 'Item with "quotes"']
    print("✓ test_quoted_fields passed")


def test_embedded_newlines():
    """Test handling of embedded newlines."""
    data = [
        ['Name', 'Notes'],
        ['Alice', 'Line 1\nLine 2\nLine 3'],
        ['Bob', 'Single line']
    ]
    
    buffer = io.StringIO()
    writer = CustomCsvWriter(buffer)
    writer.writerows(data)
    
    buffer.seek(0)
    reader = CustomCsvReader(buffer)
    rows = list(reader)
    
    assert rows[0] == ['Name', 'Notes']
    assert rows[1] == ['Alice', 'Line 1\nLine 2\nLine 3']
    assert rows[2] == ['Bob', 'Single line']
    print("✓ test_embedded_newlines passed")


def test_empty_fields():
    """Test handling of empty fields."""
    data = [
        ['A', 'B', 'C'],
        ['', 'value', ''],
        ['value1', '', 'value3']
    ]
    
    buffer = io.StringIO()
    writer = CustomCsvWriter(buffer)
    writer.writerows(data)
    
    buffer.seek(0)
    reader = CustomCsvReader(buffer)
    rows = list(reader)
    
    assert rows[0] == ['A', 'B', 'C']
    assert rows[1] == ['', 'value', '']
    assert rows[2] == ['value1', '', 'value3']
    print("✓ test_empty_fields passed")


def test_complex_data():
    """Test with complex mixed data."""
    data = [
        ['ID', 'Email', 'Message', 'Status'],
        ['1', 'alice@example.com', 'Hello, world!', 'active'],
        ['2', 'bob@test.com', 'Multi\nline\nmessage', 'pending'],
        ['3', 'charlie@org.org', 'Has "quoted" text', 'inactive'],
        ['4', 'diana@mail.com', 'Comma, separated, values', 'active']
    ]
    
    buffer = io.StringIO()
    writer = CustomCsvWriter(buffer)
    writer.writerows(data)
    
    buffer.seek(0)
    reader = CustomCsvReader(buffer)
    rows = list(reader)
    
    assert len(rows) == 5
    assert rows[1][1] == 'alice@example.com'
    assert rows[2][2] == 'Multi\nline\nmessage'
    assert rows[3][2] == 'Has "quoted" text'
    assert rows[4][2] == 'Comma, separated, values'
    print("✓ test_complex_data passed")


def test_round_trip():
    """Test that data survives write -> read -> write -> read cycle."""
    original_data = [
        ['Name', 'Value', 'Notes'],
        ['Test1', 'value, with comma', 'Line1\nLine2'],
        ['Test2', 'normal', 'Has "quotes"']
    ]
    
    # First write
    buffer1 = io.StringIO()
    writer1 = CustomCsvWriter(buffer1)
    writer1.writerows(original_data)
    
    # First read
    buffer1.seek(0)
    reader1 = CustomCsvReader(buffer1)
    read_data1 = list(reader1)
    
    # Second write
    buffer2 = io.StringIO()
    writer2 = CustomCsvWriter(buffer2)
    writer2.writerows(read_data1)
    
    # Second read
    buffer2.seek(0)
    reader2 = CustomCsvReader(buffer2)
    read_data2 = list(reader2)
    
    # Both reads should match original
    assert read_data1 == original_data
    assert read_data2 == original_data
    print("✓ test_round_trip passed")


if __name__ == '__main__':
    print("Running test suite...")
    print()
    test_basic_writing()
    test_quoted_fields()
    test_embedded_newlines()
    test_empty_fields()
    test_complex_data()
    test_round_trip()
    print()
    print("All tests passed! ✓")
