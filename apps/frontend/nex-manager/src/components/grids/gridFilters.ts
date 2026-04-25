// Grid Filters - shared filter functions for all grids

/**
 * String filter - case insensitive startsWith
 */
export const stringFilter = (row: any, columnId: string, filterValue: string): boolean => {
  const value = row.getValue(columnId);
  if (value == null) return false;
  return String(value).toLowerCase().startsWith(filterValue.toLowerCase());
};

/**
 * Numeric filter - supports exact match and ranges
 * Usage: "21" (exact), ">20", "<10", ">=5", "<=100", "10-50" (range)
 */
export const numericFilter = (row: any, columnId: string, filterValue: string): boolean => {
  const cellValue = row.getValue(columnId);
  if (cellValue == null) return false;

  const numValue = typeof cellValue === 'number' ? cellValue : parseFloat(String(cellValue));
  if (isNaN(numValue)) return false;

  const filter = filterValue.trim();
  if (!filter) return true;

  // Range: "10-50"
  const rangeMatch = filter.match(/^(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)$/);
  if (rangeMatch) {
    const min = parseFloat(rangeMatch[1]);
    const max = parseFloat(rangeMatch[2]);
    return numValue >= min && numValue <= max;
  }

  // Comparison operators: >=, <=, >, <
  const compMatch = filter.match(/^([><]=?)\s*(\d+(?:\.\d+)?)$/);
  if (compMatch) {
    const op = compMatch[1];
    const compareValue = parseFloat(compMatch[2]);
    switch (op) {
      case '>': return numValue > compareValue;
      case '>=': return numValue >= compareValue;
      case '<': return numValue < compareValue;
      case '<=': return numValue <= compareValue;
    }
  }

  // Exact match
  const exactValue = parseFloat(filter);
  if (!isNaN(exactValue)) {
    return numValue === exactValue;
  }

  return false;
};

/**
 * Date filter - supports exact date and ranges
 * Usage: "25.12.2024" (exact), ">01.12.2024", "01.12.2024-31.12.2024" (range)
 */
export const dateFilter = (row: any, columnId: string, filterValue: string): boolean => {
  const cellValue = row.getValue(columnId);
  if (cellValue == null) return false;

  const cellDate = new Date(cellValue);
  if (isNaN(cellDate.getTime())) return false;

  const filter = filterValue.trim();
  if (!filter) return true;

  // Parse Slovak date format (dd.mm.yyyy)
  const parseDate = (str: string): Date | null => {
    const match = str.match(/^(\d{1,2})\.(\d{1,2})\.(\d{4})$/);
    if (!match) return null;
    const date = new Date(parseInt(match[3]), parseInt(match[2]) - 1, parseInt(match[1]));
    return isNaN(date.getTime()) ? null : date;
  };

  // Range: "01.12.2024-31.12.2024"
  const rangeMatch = filter.match(/^(.+?)\s*-\s*(.+)$/);
  if (rangeMatch) {
    const minDate = parseDate(rangeMatch[1]);
    const maxDate = parseDate(rangeMatch[2]);
    if (minDate && maxDate) {
      return cellDate >= minDate && cellDate <= maxDate;
    }
  }

  // Comparison
  const compMatch = filter.match(/^([><]=?)\s*(.+)$/);
  if (compMatch) {
    const op = compMatch[1];
    const compareDate = parseDate(compMatch[2]);
    if (compareDate) {
      switch (op) {
        case '>': return cellDate > compareDate;
        case '>=': return cellDate >= compareDate;
        case '<': return cellDate < compareDate;
        case '<=': return cellDate <= compareDate;
      }
    }
  }

  // Exact match
  const exactDate = parseDate(filter);
  if (exactDate) {
    return cellDate.toDateString() === exactDate.toDateString();
  }

  return false;
};

/**
 * Boolean filter - "áno", "nie", "1", "0", "true", "false"
 */
export const booleanFilter = (row: any, columnId: string, filterValue: string): boolean => {
  const value = row.getValue(columnId);
  if (value == null) return false;

  const filter = filterValue.trim().toLowerCase();
  if (!filter) return true;

  const trueValues = ['áno', 'ano', 'yes', 'true', '1', '✓'];
  const falseValues = ['nie', 'no', 'false', '0', '✗'];

  if (trueValues.includes(filter)) return value === true;
  if (falseValues.includes(filter)) return value === false;

  return false;
};

/**
 * Enum/Select filter - exact match from list
 */
export const enumFilter = (row: any, columnId: string, filterValue: string): boolean => {
  const value = row.getValue(columnId);
  if (value == null) return false;
  return String(value).toLowerCase() === filterValue.toLowerCase();
};
