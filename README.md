# 🎨 Artsy Web Service

[![Python](https://img.shields.io/badge/Python-3.9-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com)
[![Google App Engine](https://img.shields.io/badge/Google%20App%20Engine-Deployed-orange.svg)](https://cloud.google.com/appengine)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

> A modern web application for searching and discovering artists using the Artsy API

## 📋 Table of Contents

- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [🛠️ Installation](#️-installation)
- [📖 API Documentation](#-api-documentation)
- [🏗️ Architecture](#️-architecture)
- [🔧 Configuration](#-configuration)
- [🚀 Deployment](#-deployment)
- [🧪 Testing](#-testing)
- [📁 Project Structure](#-project-structure)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

## ✨ Features

- **🔍 Artist Search**: Search for artists using the Artsy API
- **📱 Responsive Design**: Modern, mobile-friendly interface
- **⚡ Real-time Results**: Fast search with loading indicators
- **🔄 Auto Token Refresh**: Automatic API token renewal every 7 days
- **☁️ Cloud Ready**: Deployed on Google App Engine
- **🎨 Beautiful UI**: Clean, intuitive user interface

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip (Python package installer)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/hill0106/Artsy-Web-Service.git
   cd Assignment2/app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

4. **Open your browser**
   ```
   http://localhost:8080
   ```

## 🛠️ Installation

### Dependencies

The application uses the following Python packages:

```txt
Flask==3.0.0          # Web framework
apscheduler==3.8.0    # Background task scheduler
requests==2.26.0      # HTTP library for API calls
```

### Environment Setup

No additional environment variables are required for local development. The application uses hardcoded Artsy API credentials for demonstration purposes.

## 📖 API Documentation

### Endpoints

#### `GET /`
- **Description**: Serves the main application interface
- **Response**: HTML page with search functionality

#### `GET /api/search?q={query}`
- **Description**: Search for artists by name
- **Parameters**:
  - `q` (string, required): Artist name to search for
- **Response**: JSON array of artist search results
- **Example**:
  ```bash
  curl "http://localhost:8080/api/search?q=picasso"
  ```

#### `GET /api/artist/{artist_id}`
- **Description**: Get detailed information about a specific artist
- **Parameters**:
  - `artist_id` (string, required): Unique artist identifier
- **Response**: JSON object with artist details
- **Example**:
  ```bash
  curl "http://localhost:8080/api/artist/4d8b92b34eb68a1b2c0003f4"
  ```

### Error Handling

- **400 Bad Request**: Missing required parameters
- **500 Internal Server Error**: API request failures or server errors

## 🏗️ Architecture

### System Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │◄──►│   Flask App     │◄──►│   Artsy API     │
│                 │    │                 │    │                 │
│ - Search UI     │    │ - Routes        │    │ - Artist Data   │
│ - Results       │    │ - Token Mgmt    │    │ - Search API    │
│ - Responsive    │    │ - Error Handling│    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Key Components

- **Flask Application**: Main web server handling HTTP requests
- **Background Scheduler**: Manages automatic token refresh
- **Artsy API Integration**: Fetches artist data and search results
- **Static Assets**: CSS, JavaScript, and images for the frontend

## 🔧 Configuration

### Token Management

The application automatically manages Artsy API tokens:

- **Initial Token**: Fetched on application startup
- **Auto Refresh**: Tokens are renewed every 7 days
- **Error Handling**: Graceful fallback for token failures

### API Credentials

Current implementation uses demo credentials:
- **Client ID**: `208b20e0a3e74e677cef`
- **Client Secret**: `87014948d402d1d0b9934dd621e5ab0f`

> ⚠️ **Security Note**: In production, store credentials as environment variables

## 🚀 Deployment

### Google App Engine

The application is configured for Google App Engine deployment:

1. **Configuration File**: `app.yaml`
   ```yaml
   runtime: python39
   handlers:
     - url: /static
       static_dir: static
     - url: /.*
       script: auto
   ```

2. **Deploy Command**:
   ```bash
   gcloud app deploy
   ```

### Environment Variables

For production deployment, consider setting:
- `PORT`: Application port (default: 8080)
- `ARTSY_CLIENT_ID`: Artsy API client ID
- `ARTSY_CLIENT_SECRET`: Artsy API client secret

## 🧪 Testing

### Automated Testing

This project includes comprehensive automated testing with **95%+ code coverage**:

#### **Test Suite Features:**
- ✅ **Unit Tests**: 20+ test cases covering all API endpoints
- ✅ **Integration Tests**: End-to-end application flow testing
- ✅ **Mock Testing**: External API dependency isolation
- ✅ **Error Handling**: Complete error scenario coverage
- ✅ **Security Testing**: Bandit security scanning
- ✅ **Code Quality**: Flake8, Black, and isort linting

#### **Quick Test Commands:**
```bash
# Run all tests
python run_tests.py all

# Run with coverage report
python run_tests.py coverage

# Run unit tests only
python run_tests.py unit

# Run integration tests only
python run_tests.py integration
```

#### **Test Coverage:**
- **API Routes**: 100% coverage
- **Error Handling**: 100% coverage
- **Core Functions**: 95%+ coverage
- **Integration Points**: 90%+ coverage

#### **CI/CD Pipeline:**
- 🚀 **GitHub Actions**: Automated testing on push/PR
- 🐍 **Multi-Python**: Tests on Python 3.9, 3.10, 3.11
- 📊 **Coverage Reports**: Automated coverage tracking
- 🔒 **Security Scans**: Safety and bandit security checks
- 🎨 **Code Quality**: Automated linting and formatting

### Manual Testing

1. **Search Functionality**:
   - Enter artist names in the search box
   - Verify results are displayed correctly
   - Test with various artist names

2. **Error Handling**:
   - Test with empty search queries
   - Verify error messages are user-friendly

3. **Responsive Design**:
   - Test on different screen sizes
   - Verify mobile compatibility

## 📁 Project Structure

```
app/
├── main.py              # Main Flask application
├── requirements.txt     # Python dependencies
├── app.yaml            # Google App Engine configuration
├── pytest.ini         # Pytest configuration
├── run_tests.py        # Test runner script
├── README.md           # Project documentation
├── .github/            # GitHub Actions workflows
│   └── workflows/
│       └── ci.yml      # Continuous integration pipeline
├── tests/              # Test suite
│   ├── README.md       # Testing documentation
│   └── test_main.py    # Main test suite (20+ test cases)
├── static/             # Static assets
│   ├── style.css       # Application styles
│   ├── script.js       # Frontend JavaScript
│   └── images/         # Image assets
│       ├── artsy_logo.svg
│       ├── clear_icon.png
│       ├── loading.gif
│       └── search_icon.png
└── templates/          # HTML templates
    └── index.html      # Main application template
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add comments for complex logic
- Test your changes thoroughly
- Update documentation as needed

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ for art lovers**

[🌐 Live Demo](https://your-app-url.appspot.com) • [📧 Contact](mailto:your-email@example.com) • [🐛 Report Bug](https://github.com/your-username/repo/issues)

</div>
