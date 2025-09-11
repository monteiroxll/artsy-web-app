# 🧪 Testing Documentation

This directory contains comprehensive test suites for the Artsy Web Service application.

## 📋 Test Structure

```
tests/
├── README.md           # This file
├── test_main.py        # Main test suite
└── conftest.py         # Pytest configuration and fixtures
```

## 🚀 Quick Start

### Install Test Dependencies

```bash
pip install -r requirements.txt
```

### Run All Tests

```bash
python run_tests.py all
```

### Run Specific Test Types

```bash
# Unit tests only
python run_tests.py unit

# Integration tests only
python run_tests.py integration

# With coverage report
python run_tests.py coverage
```

## 🧪 Test Categories

### Unit Tests (`TestArtsyWebService`)

Tests individual components and functions:

- ✅ **API Endpoints**: All routes (`/`, `/api/search`, `/api/artist/{id}`)
- ✅ **Error Handling**: 400, 500 error responses
- ✅ **Authentication**: Token management and API headers
- ✅ **Data Validation**: Input validation and response formatting
- ✅ **Static Files**: CSS, JS, and image serving
- ✅ **Template Rendering**: HTML template correctness

### Integration Tests (`TestIntegration`)

Tests complete application flows:

- ✅ **End-to-End Flow**: Frontend to API integration
- ✅ **Static Asset Serving**: Complete asset pipeline
- ✅ **API Accessibility**: All endpoints reachable

## 📊 Coverage Metrics

Current test coverage targets:

- **API Routes**: 100% coverage
- **Error Handling**: 100% coverage  
- **Core Functions**: 95%+ coverage
- **Integration Points**: 90%+ coverage

## 🔧 Test Configuration

### Pytest Configuration (`pytest.ini`)

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
    --cov=main
    --cov-report=term-missing
    --cov-report=html:htmlcov
    --cov-report=xml
```

### Test Markers

- `@pytest.mark.unit`: Unit tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.slow`: Slow running tests

## 🎯 Test Examples

### API Endpoint Testing

```python
def test_search_artist_success(self, client, mock_artsy_response):
    """Test successful artist search."""
    with patch('main.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = mock_artsy_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        response = client.get('/api/search?q=picasso')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert '_embedded' in data
        assert 'artists' in data['_embedded']
```

### Error Handling Testing

```python
def test_search_artist_no_query(self, client):
    """Test search endpoint with no query parameter."""
    response = client.get('/api/search')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'No query provided'
```

## 🔄 Continuous Integration

### GitHub Actions Workflow

The CI pipeline includes:

1. **Multi-Python Testing**: Python 3.9, 3.10, 3.11
2. **Unit & Integration Tests**: Complete test suite
3. **Coverage Reporting**: Code coverage metrics
4. **Code Quality**: Linting with flake8, black, isort
5. **Security Scanning**: Safety and bandit checks
6. **Build Verification**: Application startup testing

### Workflow Triggers

- Push to `main`, `develop`, or `feature/*` branches
- Pull requests to `main` or `develop`
- Manual workflow dispatch

## 📈 Coverage Reports

### HTML Coverage Report

After running tests with coverage:

```bash
python run_tests.py coverage
```

Open `htmlcov/index.html` in your browser for detailed coverage information.

### Coverage Metrics

- **Lines**: Percentage of lines executed
- **Branches**: Percentage of branches taken
- **Functions**: Percentage of functions called
- **Missing**: Specific lines not covered

## 🐛 Debugging Tests

### Verbose Output

```bash
python -m pytest tests/ -v -s
```

### Run Single Test

```bash
python -m pytest tests/test_main.py::TestArtsyWebService::test_search_artist_success -v
```

### Debug Mode

```bash
python -m pytest tests/ --pdb
```

## 📝 Adding New Tests

### Test File Structure

```python
class TestNewFeature:
    """Test suite for new feature."""
    
    @pytest.fixture
    def client(self):
        """Test client fixture."""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_new_feature(self, client):
        """Test new feature functionality."""
        # Test implementation
        pass
```

### Test Naming Convention

- **Files**: `test_*.py`
- **Classes**: `Test*`
- **Methods**: `test_*`
- **Descriptive names**: `test_search_artist_with_valid_query`

## 🎯 Best Practices

### Test Organization

1. **One test per assertion**: Keep tests focused
2. **Descriptive names**: Clear test purpose
3. **Setup/Teardown**: Use fixtures for setup
4. **Mock external dependencies**: Isolate units under test
5. **Test edge cases**: Error conditions and boundaries

### Mocking Guidelines

```python
# Mock external API calls
with patch('main.requests.get') as mock_get:
    mock_response = Mock()
    mock_response.json.return_value = test_data
    mock_get.return_value = mock_response
    
    # Test code here
```

## 📊 Performance Testing

### Load Testing

For performance validation:

```bash
# Install locust for load testing
pip install locust

# Run load tests
locust -f tests/load_test.py --host=http://localhost:8080
```

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure `sys.path.append()` includes project root
2. **Mock Failures**: Verify mock patches target correct modules
3. **Fixture Issues**: Check fixture scope and dependencies
4. **Coverage Gaps**: Review untested code paths

### Debug Commands

```bash
# Check test discovery
python -m pytest --collect-only

# Run with detailed output
python -m pytest tests/ -vvv

# Profile test execution
python -m pytest tests/ --profile
```

---

**📚 For more information, see the main project README.md**
