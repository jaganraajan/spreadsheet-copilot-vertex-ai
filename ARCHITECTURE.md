# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          User Browser                            │
│                    (Web UI - Port 5000)                          │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Flask Application                           │
│                      (preview_ui.py)                             │
│                                                                   │
│  Routes:                                                          │
│  • GET  /              → Home page with upload form              │
│  • GET  /files         → List uploaded files                     │
│  • GET  /samples       → List sample files                       │
│  • POST /load-sample   → Load sample to uploads                  │
│  • GET  /preview/:file → Preview CSV data                        │
│  • GET  /analyze/:file → Analysis form                           │
│  • POST /analyze/:file → Run AI analysis                         │
│  • GET  /diff/:file    → Diff view (placeholder)                 │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP Requests
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Application                           │
│                     (app/main.py)                                │
│                      Port 8000                                   │
│                                                                   │
│  Endpoints:                                                       │
│  • POST /upload            → Upload CSV file                     │
│  • POST /analyze           → Analyze with Gemini AI              │
│  • POST /execute-tool      → Execute tool stub                   │
│  • GET  /files            → List uploaded files                  │
│  • GET  /samples          → List sample files                    │
│  • POST /load-sample      → Copy sample to uploads               │
│  • GET  /download/:file   → Download file                        │
│  • GET  /tools            → List available tools                 │
└───┬──────────────────┬─────────────────┬─────────────────────────┘
    │                  │                 │
    ▼                  ▼                 ▼
┌────────┐      ┌─────────────┐   ┌──────────────┐
│ Pandas │      │   Gemini    │   │   Tool       │
│  CSV   │      │  Service    │   │   Stubs      │
│ Handler│      │  (AI Model) │   │              │
└────────┘      └──────┬──────┘   └──────────────┘
                       │
                       │ API Call
                       ▼
              ┌────────────────────┐
              │  Google Gemini AI  │
              │   (gemini-pro)     │
              └────────────────────┘
```

## Data Flow

### 1. File Upload Flow

```
User → Upload Form → Flask UI → FastAPI /upload → Save to uploads/ → Return success
```

### 2. AI Analysis Flow

```
User → Analysis Request → Flask UI → FastAPI /analyze
                                      ↓
                                   Load CSV (Pandas)
                                      ↓
                                   Generate Summary
                                      ↓
                                   Build Prompt
                                      ↓
                                   Call Gemini API
                                      ↓
                                   Parse Response
                                      ↓
                                   Return ActionPlan
                                      ↓
Flask UI ← Display Results ← JSON Response
```

### 3. Sample Loading Flow

```
User → Click "Load" → Flask UI → FastAPI /load-sample → Copy sample to uploads → Return success
```

## Component Details

### FastAPI Application (`app/main.py`)

**Responsibilities:**
- Handle HTTP requests
- Validate input data
- Manage file operations
- Coordinate with services
- Return structured responses

**Key Features:**
- Automatic API documentation (Swagger/ReDoc)
- Request validation via Pydantic
- CORS middleware for browser access
- Type hints for better IDE support

### Gemini Service (`app/gemini_service.py`)

**Responsibilities:**
- Initialize Gemini AI client
- Create data summaries from CSV
- Build analysis prompts
- Parse AI responses
- Convert to ActionPlan schema

**Process:**
1. Load CSV with Pandas
2. Generate statistical summary
3. Build structured prompt
4. Call Gemini API
5. Parse JSON response
6. Validate against ActionPlan schema

### Pydantic Schemas (`app/schemas.py`)

**Purpose:** Type-safe data validation

**Schemas:**
- `ToolCall`: Represents a tool action
  - tool_name: string
  - parameters: dict
  - reasoning: string
  
- `ActionPlan`: AI analysis response
  - analysis: string
  - recommended_actions: List[ToolCall]
  - summary: string
  - priority: string (high/medium/low)

### Tool Stubs (`app/tools.py`)

**Current State:** Stub implementations

**Tools:**
1. `apply_formula`: Apply formulas to columns
2. `create_pivot`: Create pivot tables
3. `conditional_format`: Apply conditional formatting

**Tool Registry:**
- Dictionary mapping tool names to functions
- Easy to extend with new tools
- Consistent return structure

### Flask UI (`preview_ui.py`)

**Responsibilities:**
- Render HTML templates
- Display data visualizations
- Handle user interactions
- Proxy requests to FastAPI
- Format results for display

**Templates:**
- `base.html`: Common layout
- `index.html`: Home/upload page
- `preview.html`: Data preview
- `analyze.html`: Analysis form
- `results.html`: Analysis results
- `diff.html`: Diff view (placeholder)

## Technology Choices

### Why FastAPI?
- Automatic API documentation
- Built-in validation with Pydantic
- Async support for better performance
- Modern Python features (type hints)
- Fast development

### Why Flask for UI?
- Lightweight and simple
- Good for rendering templates
- Easy to separate concerns
- Can be replaced with React/Vue if needed

### Why Pandas?
- Industry standard for data manipulation
- Rich CSV handling
- Statistical functions
- Easy integration with AI models

### Why Pydantic?
- Runtime type validation
- Automatic JSON serialization
- Clear error messages
- Integration with FastAPI

## Scalability Considerations

### Current Limitations
- Single server instances
- File storage on local disk
- Synchronous AI calls
- No caching

### Future Improvements
1. **Storage:**
   - Move to S3/GCS for file storage
   - Database for metadata

2. **Performance:**
   - Add Redis for caching
   - Async AI calls
   - Background job queue (Celery)

3. **Deployment:**
   - Kubernetes for orchestration
   - Load balancer for scaling
   - CDN for static assets

4. **Security:**
   - Authentication (JWT, OAuth)
   - Rate limiting
   - File validation
   - API key management

## Development Workflow

```
Developer writes code
       ↓
Local testing
       ↓
Unit tests (pytest)
       ↓
Git commit
       ↓
GitHub PR
       ↓
CI/CD pipeline
       ↓
Docker build
       ↓
Deploy to staging
       ↓
Manual testing
       ↓
Deploy to production
```

## File Organization

```
.
├── app/                    # FastAPI application
│   ├── __init__.py        # Package marker
│   ├── main.py            # API endpoints
│   ├── schemas.py         # Pydantic models
│   ├── gemini_service.py  # AI integration
│   └── tools.py           # Tool implementations
│
├── templates/             # Flask templates
│   └── *.html            # UI templates
│
├── samples/              # Sample data
│   └── *.csv            # CSV samples
│
├── uploads/              # User uploads
│   └── .gitkeep         # Keep directory
│
├── preview_ui.py         # Flask app
├── requirements.txt      # Dependencies
├── test_api.py          # Tests
├── Dockerfile           # Container config
├── docker-compose.yml   # Multi-container setup
└── *.md                 # Documentation
```

## Extension Points

### Adding New Tools
1. Define function in `app/tools.py`
2. Add to TOOLS registry
3. Update API documentation
4. Add UI handler

### Adding New AI Models
1. Create new service class (like GeminiService)
2. Implement same interface
3. Make service configurable
4. Support multiple models

### Adding Authentication
1. Add auth middleware to FastAPI
2. Implement user model
3. Add login/register endpoints
4. Protect routes
5. Update UI with auth flow

### Supporting Other File Formats
1. Add file type detection
2. Implement format-specific readers
3. Normalize to common format
4. Update validation logic

## Security Considerations

### Current Implementation
- Basic file validation
- CORS enabled (development)
- No authentication
- Local file storage

### Production Requirements
- User authentication
- File upload limits
- Virus scanning
- Input sanitization
- HTTPS only
- Rate limiting
- API key rotation
- Audit logging

## Monitoring & Logging

### Current State
- Basic console logging
- No metrics collection
- No error tracking

### Recommended Setup
- Structured logging (JSON)
- Application metrics (Prometheus)
- Error tracking (Sentry)
- Performance monitoring (New Relic/DataDog)
- User analytics

## Testing Strategy

### Unit Tests
- Test individual functions
- Mock external dependencies
- Fast execution

### Integration Tests
- Test API endpoints
- Test with real database
- Test file operations

### End-to-End Tests
- Test complete workflows
- Use Playwright/Selenium
- Test UI interactions

### Performance Tests
- Load testing (Locust)
- Stress testing
- Profile bottlenecks
