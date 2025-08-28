// Table Sorting with Search
class SortableTable {
    constructor(tableElement) {
        this.table = tableElement;
        this.tbody = this.table.querySelector('tbody');
        this.headers = this.table.querySelectorAll('thead th');
        this.originalRows = Array.from(this.tbody.rows);
        this.currentSort = { column: -1, direction: 'asc' };
        
        this.init();
    }
    
    init() {
        // Add click listeners to headers
        this.headers.forEach((header, index) => {
            header.addEventListener('click', () => this.sort(index));
        });
        
        // Add search functionality
        this.addSearchBox();
    }
    
    addSearchBox() {
        const tableContainer = this.table.closest('.research-table');
        if (!tableContainer) return;
        
        // Create search container
        const controlsDiv = document.createElement('div');
        controlsDiv.className = 'table-controls';
        
        // Search box
        const searchDiv = document.createElement('div');
        searchDiv.className = 'search-box';
        searchDiv.innerHTML = `
            <input type="text" placeholder="Search table..." class="table-search">
        `;
        
        // Table info
        const infoDiv = document.createElement('div');
        infoDiv.className = 'table-info';
        infoDiv.textContent = `Showing ${this.tbody.rows.length} entries`;
        
        controlsDiv.appendChild(searchDiv);
        controlsDiv.appendChild(infoDiv);
        
        // Insert before table
        tableContainer.insertBefore(controlsDiv, this.table);
        
        // Add search listener
        const searchInput = searchDiv.querySelector('.table-search');
        searchInput.addEventListener('input', (e) => this.search(e.target.value));
        
        this.infoDiv = infoDiv;
    }
    
    sort(columnIndex) {
        // Determine sort direction
        if (this.currentSort.column === columnIndex) {
            this.currentSort.direction = this.currentSort.direction === 'asc' ? 'desc' : 'asc';
        } else {
            this.currentSort.direction = 'asc';
        }
        this.currentSort.column = columnIndex;
        
        // Update header classes
        this.headers.forEach(header => {
            header.classList.remove('sort-asc', 'sort-desc');
        });
        this.headers[columnIndex].classList.add(`sort-${this.currentSort.direction}`);
        
        // Sort rows
        const sortedRows = Array.from(this.tbody.rows).sort((a, b) => {
            const aVal = this.getCellValue(a, columnIndex);
            const bVal = this.getCellValue(b, columnIndex);
            
            // Numeric comparison for numbers (including ± format)
            const aNum = this.parseNumber(aVal);
            const bNum = this.parseNumber(bVal);
            
            if (!isNaN(aNum) && !isNaN(bNum)) {
                return this.currentSort.direction === 'asc' ? aNum - bNum : bNum - aNum;
            }
            
            // String comparison
            const comparison = aVal.localeCompare(bVal, undefined, { numeric: true });
            return this.currentSort.direction === 'asc' ? comparison : -comparison;
        });
        
        // Reorder rows in DOM
        sortedRows.forEach(row => this.tbody.appendChild(row));
    }
    
    getCellValue(row, columnIndex) {
        return row.cells[columnIndex].textContent.trim();
    }
    
    parseNumber(str) {
        // Handle numbers with ± (e.g., "68.03±2.74")
        const match = str.match(/^(-?\d+\.?\d*)/);
        return match ? parseFloat(match[1]) : NaN;
    }
    
    search(query) {
        const searchTerm = query.toLowerCase();
        let visibleCount = 0;
        
        this.originalRows.forEach(row => {
            const text = Array.from(row.cells)
                .map(cell => cell.textContent.toLowerCase())
                .join(' ');
            
            if (text.includes(searchTerm)) {
                row.style.display = '';
                visibleCount++;
            } else {
                row.style.display = 'none';
            }
        });
        
        // Update info
        if (this.infoDiv) {
            const total = this.originalRows.length;
            if (searchTerm) {
                this.infoDiv.textContent = `Showing ${visibleCount} of ${total} entries (filtered)`;
            } else {
                this.infoDiv.textContent = `Showing ${total} entries`;
            }
        }
    }
}

// Initialize tables when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all sortable tables
    const tables = document.querySelectorAll('table.sortable');
    tables.forEach(table => new SortableTable(table));
    
    console.log(`Initialized ${tables.length} sortable tables`);
});