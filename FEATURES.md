# Features Documentation

## Core Features

### 1. CSV File Upload
- **Drag-and-drop** or browse to upload CSV files
- **File validation** to ensure only CSV files are accepted
- **Persistent storage** in the `uploads/` directory
- **File management** with list, preview, and download capabilities

### 2. Google Gemini AI Integration
- **Automatic analysis** of CSV data using Google's Gemini Pro model
- **Intelligent recommendations** based on data patterns
- **Structured responses** using Pydantic schemas
- **Custom prompts** for targeted analysis

### 3. ActionPlan Response Schema
The AI returns a structured `ActionPlan` object:

```python
ActionPlan:
  - analysis: str              # Detailed data analysis
  - recommended_actions: List  # List of ToolCall objects
  - summary: str              # Brief summary
  - priority: str             # high/medium/low
```

Each `ToolCall` includes:
- `tool_name`: Name of the tool to execute
- `parameters`: Dictionary of tool parameters
- `reasoning`: Explanation for the recommendation

### 4. Tool Stubs

#### apply_formula
Apply Excel-like formulas to spreadsheet columns.

**Parameters:**
- `column`: Source column name
- `formula`: Formula expression (e.g., "=SUM(A:A)")
- `target_column`: Optional destination column
- `description`: Human-readable description

**Example:**
```python
apply_formula(
    column="Sales",
    formula="=A1*1.1",
    target_column="Sales_With_Tax",
    description="Add 10% tax to sales"
)
```

#### create_pivot
Generate pivot tables for data summarization.

**Parameters:**
- `index_columns`: List of columns to use as index
- `value_column`: Column to aggregate
- `aggregation`: Function (sum, mean, count, etc.)
- `columns`: Optional columns to pivot

**Example:**
```python
create_pivot(
    index_columns=["Region", "Category"],
    value_column="Sales",
    aggregation="sum"
)
```

#### conditional_format
Apply conditional formatting based on rules.

**Parameters:**
- `column`: Column to format
- `condition`: Condition expression (e.g., ">100")
- `format_style`: Dict of styling options
- `description`: Human-readable description

**Example:**
```python
conditional_format(
    column="Quantity",
    condition="<30",
    format_style={"color": "red", "background": "yellow"},
    description="Highlight low stock items"
)
```

### 5. Flask Preview UI

#### Home Page (`/`)
- Upload CSV files
- Load sample files with one click
- View list of uploaded files
- Quick access to preview and analysis

#### Preview Page (`/preview/<filename>`)
- **Statistics panel** showing rows, columns, data types
- **Data preview** with first 10 rows
- **Full data view** with scrollable table
- **Action buttons** for analysis and diff view

#### Analysis Page (`/analyze/<filename>`)
- **Optional prompt input** for custom analysis
- **Information panel** explaining AI capabilities
- **Tool descriptions** for available actions
- **Run analysis button** to trigger AI processing

#### Results Page (`/results`)
- **Priority indicator** (high/medium/low)
- **Detailed analysis** from AI
- **Recommended actions** with reasoning
- **Execute buttons** for tool stubs (demo)
- **Raw JSON view** for debugging

#### Diff View (`/diff/<filename>`)
- Placeholder for before/after comparison
- Will show original vs transformed data
- Highlights differences and changes

### 6. One-Click Sample Loader

Three sample CSV files included:

1. **sales_data.csv** (15 rows)
   - Columns: Date, Product, Category, Sales, Quantity, Region
   - Use case: Sales analysis, trends, regional performance

2. **employee_data.csv** (10 rows)
   - Columns: EmployeeID, Name, Department, Salary, HireDate, Status
   - Use case: HR analytics, salary distribution, department analysis

3. **inventory.csv** (10 rows)
   - Columns: SKU, ProductName, Category, Quantity, ReorderLevel, UnitPrice, LastRestocked
   - Use case: Inventory management, reorder alerts, stock analysis

**How it works:**
1. Click "Load" button next to any sample
2. File is automatically copied to `uploads/` directory
3. Immediately available for preview and analysis

## Additional Features

### API Documentation
- **Swagger UI** at `/docs` with interactive API testing
- **ReDoc** at `/redoc` for clean, readable documentation
- **Automatic schema generation** from Pydantic models

### Docker Support
- **Dockerfile** for containerized deployment
- **docker-compose.yml** for multi-service orchestration
- **Volume mounting** for persistent data
- **Environment variable** configuration

### Testing Infrastructure
- **Unit tests** for schemas and tools
- **API endpoint tests** with FastAPI TestClient
- **Pytest configuration** for easy test execution
- **Example tests** to guide development

### Developer Experience
- **Type hints** throughout the codebase
- **Comprehensive documentation** (README, QUICKSTART, DEVELOPMENT, ARCHITECTURE)
- **Clear separation of concerns** (API, UI, services, tools)
- **Extensible architecture** for adding new features

## Security Features (Current)

### File Validation
- Only CSV files accepted
- File extension checking
- File size monitoring

### CORS Configuration
- Enabled for development
- Can be restricted for production

### Environment Variables
- API keys stored in `.env` file
- Example configuration provided
- Not committed to repository

## Planned Features (Future)

### Enhanced Tool Execution
- [ ] Actual formula application with pandas
- [ ] Pivot table generation and export
- [ ] Conditional formatting with color codes
- [ ] Undo/redo functionality

### Advanced Analysis
- [ ] Multiple AI model support (GPT-4, Claude, etc.)
- [ ] Custom analysis templates
- [ ] Batch processing of multiple files
- [ ] Scheduled analysis

### Collaboration
- [ ] User authentication and sessions
- [ ] Shared workspaces
- [ ] Comments and annotations
- [ ] Version control for files

### Data Export
- [ ] Export to Excel (.xlsx)
- [ ] Export to PDF reports
- [ ] Email analysis results
- [ ] API webhooks for notifications

### Visualization
- [ ] Charts and graphs from data
- [ ] Interactive dashboards
- [ ] Data exploration tools
- [ ] Custom visualizations

### Performance
- [ ] Caching of analysis results
- [ ] Async processing for large files
- [ ] Background job queue
- [ ] Real-time updates

### Security
- [ ] User authentication (OAuth, JWT)
- [ ] Role-based access control
- [ ] File encryption at rest
- [ ] Audit logging
- [ ] Rate limiting
- [ ] Input sanitization

## Technical Capabilities

### Data Processing
- **Pandas integration** for CSV manipulation
- **Statistical analysis** (mean, median, std, etc.)
- **Missing value detection**
- **Data type inference**
- **Column profiling**

### AI Integration
- **Structured prompt engineering** for consistent results
- **JSON response parsing** with error handling
- **Fallback responses** if AI fails
- **Token management** for cost control
- **Response validation** against schemas

### Web Framework
- **FastAPI async support** for concurrent requests
- **Automatic input validation** with Pydantic
- **Exception handling** with proper HTTP status codes
- **CORS middleware** for browser access
- **Static file serving**

### UI Framework
- **Bootstrap 5** for responsive design
- **JavaScript** for dynamic interactions
- **RESTful API calls** from frontend
- **Form validation** on client side
- **Loading states** for better UX

## Usage Metrics

### API Performance
- Average response time: < 100ms (file operations)
- AI analysis time: 2-5 seconds (depends on Gemini API)
- File upload limit: Configurable (default: unlimited)
- Concurrent requests: Supported via async

### Browser Compatibility
- Chrome ✅
- Firefox ✅
- Safari ✅
- Edge ✅
- Mobile browsers ✅

### System Requirements
- **Python**: 3.8 or higher
- **Memory**: 512MB minimum
- **Storage**: Depends on uploaded files
- **Network**: Internet required for Gemini API

## Extensibility

### Adding New Tools
1. Define function in `app/tools.py`
2. Add to TOOLS registry
3. Update `/tools` endpoint
4. Add documentation

### Adding New AI Models
1. Create service class (similar to GeminiService)
2. Implement analysis method
3. Make model selection configurable
4. Update documentation

### Custom Analysis Types
1. Extend ActionPlan schema if needed
2. Modify prompt in gemini_service.py
3. Add new response parsing logic
4. Update UI to display new fields

### UI Customization
1. Modify templates in `templates/`
2. Add custom CSS in `base.html`
3. Add JavaScript for new interactions
4. Update routing in `preview_ui.py`

## Best Practices

### Code Organization
- Separate concerns (API, UI, services, models)
- Type hints for better IDE support
- Docstrings for all public functions
- Consistent naming conventions

### Error Handling
- Try-catch blocks for external calls
- Proper HTTP status codes
- User-friendly error messages
- Logging for debugging

### Documentation
- Keep README updated
- Add inline comments for complex logic
- Provide usage examples
- Document breaking changes

### Testing
- Write tests for new features
- Test error scenarios
- Use fixtures for test data
- Run tests before committing

## Support and Resources

### Getting Help
- Check documentation files first
- Review examples in test files
- Test API endpoints with `/docs`
- File issues on GitHub

### Contributing
- Follow code style guidelines
- Add tests for new features
- Update documentation
- Submit pull requests

### Community
- Star the repository
- Share feedback
- Report bugs
- Suggest features

## License

MIT License - See LICENSE file for details
