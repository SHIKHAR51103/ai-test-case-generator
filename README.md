# 🤖 AI-Powered Test Case Generator

> Transform Software Requirements into Comprehensive Test Cases using NLP & AI

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🌟 Overview

An intelligent test case generation tool that uses Natural Language Processing (NLP) and AI to automatically create comprehensive test cases from Software Requirement Documents (SRDs). This tool combines the power of rule-based NLP with optional OpenAI GPT integration to generate high-quality test cases covering functional, UI, performance, security, and integration testing scenarios.

## ✨ Key Features

### 🎯 Core Functionality
- **Smart NLP Analysis**: Automatically extracts actions, entities, and conditions from requirements
- **Multiple Test Types**: Generates functional, UI, performance, security, and integration tests
- **Dual AI Modes**: 
  - Rule-based NLP engine (works offline, no API needed)
  - OpenAI GPT integration (optional, for enhanced generation)
- **Comprehensive Coverage**: Positive, negative, and boundary test scenarios
- **Priority Detection**: Automatically assigns test priority based on requirement criticality

### 📊 Advanced Features
- **Interactive Dashboard**: Beautiful Streamlit UI with real-time analytics
- **Multiple Input Methods**: Manual entry, JSON upload, or sample requirements
- **Smart Filtering**: Filter by type, priority, or search keywords
- **Export Options**: JSON and Excel formats with one-click download
- **Test Analytics**: Visual charts and distribution metrics
- **Session Persistence**: Maintains state across interactions

### 🔧 Technical Highlights
- No database required - runs entirely in-memory
- Works without OpenAI API (falls back to NLP)
- Generates structured test data automatically
- Professional test case format (ID, steps, expected results, preconditions)
- Scalable architecture for batch processing

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download this repository**
```bash
cd ai-test-generator
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

4. **Open your browser**
The app will automatically open at `http://localhost:8501`

## 📖 Usage Guide

### Method 1: Using Sample Requirements (Fastest)
1. Go to "Input Requirements" tab
2. Select "Sample Requirements"
3. Click "Load Sample Requirements"
4. Click "🚀 Generate Test Cases"
5. View results in "Generated Test Cases" tab

### Method 2: Manual Entry
1. Go to "Input Requirements" tab
2. Select "Manual Entry"
3. Fill in:
   - Requirement ID (e.g., REQ-001)
   - Title (e.g., "User Login")
   - Description (detailed requirement text)
   - Priority and Category
4. Click "Add Requirement"
5. Repeat for more requirements
6. Click "🚀 Generate Test Cases"

### Method 3: JSON Upload
1. Prepare a JSON file with requirements:
```json
[
  {
    "id": "REQ-001",
    "title": "User Login",
    "description": "The system shall allow users to login with email and password...",
    "priority": "High",
    "category": "Security"
  }
]
```
2. Upload the JSON file
3. Click "🚀 Generate Test Cases"

### Viewing Test Cases
- Navigate to "Generated Test Cases" tab
- Filter by type, priority, or search
- Expand any test case to see:
  - Description
  - Preconditions
  - Test steps
  - Expected results
  - Test data
  - Status

### Exporting Results
1. Go to "Export" tab
2. Choose format:
   - **JSON**: For API integration or version control
   - **Excel**: For team sharing and manual testing
   - **Markdown**: Summary report
3. Click download button

## 🎓  Talking Points

### Why This Project Stands Out
1. **AI + Testing Combination**: Rare skill set that combines ML/AI with QA
2. **Production Ready**: Full-featured app with UI, not just a script
3. **Dual Intelligence**: Works with and without OpenAI API
4. **Real-World Application**: Solves actual testing team pain points
5. **Modern Tech Stack**: Streamlit, Pandas, NLP, OpenAI API

### Technical Deep Dive

#### NLP Analysis Pipeline
```
Requirement Text → Tokenization → Entity Extraction → Action Detection
                                                    → Condition Analysis
                                                    → Test Type Classification
                                                    → Priority Inference
                                                    ↓
                                            Test Case Generation
```

#### Architecture Highlights
- **Modular Design**: `NLPTestCaseGenerator` class with clear separation
- **Strategy Pattern**: Switches between NLP and OpenAI modes seamlessly
- **Template Method**: Consistent test case structure across all types
- **Factory Pattern**: Dynamic test data and step generation

#### Key Algorithms
1. **Keyword Extraction**: Uses predefined dictionaries for action/entity detection
2. **Context Analysis**: Identifies test types based on requirement context
3. **Priority Inference**: Uses linguistic markers (must/should/critical)
4. **Step Generation**: Creates logical test sequences from extracted actions

### Demo Flow 
1. **Show Problem**: Manual test case writing is time-consuming
2. **Demo Solution**: Load sample requirements → Generate → Show results
3. **Highlight Features**: Filters, analytics, multiple export formats
4. **Explain AI**: How NLP extracts entities and actions
5. **Show Code**: Walk through `analyze_requirement()` method
6. **Future Enhancements**: Discuss scalability and improvements

## 🛠️ Advanced Configuration

### Using OpenAI API (Optional)
1. Get API key from https://platform.openai.com/
2. In sidebar, check "Use OpenAI API"
3. Enter your API key
4. Generate test cases (will use GPT-3.5-turbo)

**Note**: The app works perfectly without OpenAI API using the built-in NLP engine.

### Customizing Test Types
Edit the `test_case_templates` dictionary in `NLPTestCaseGenerator.__init__()`:
```python
self.test_case_templates = {
    'functional': ['positive', 'negative', 'boundary'],
    'ui': ['layout', 'responsiveness', 'navigation'],
    'performance': ['load_time', 'concurrent_users', 'data_volume'],
    'security': ['authentication', 'authorization', 'data_validation'],
    'integration': ['api', 'database', 'third_party'],
    'custom_type': ['scenario1', 'scenario2']  # Add your own
}
```

### Adding Custom Keywords
Extend the keyword lists in `analyze_requirement()`:
```python
action_keywords = ['create', 'update', 'delete', 'view', 'search', 'your_action']
entity_keywords = ['user', 'admin', 'customer', 'product', 'your_entity']
```

## 📊 Sample Output

### Generated Test Case Example
```
ID: TC-REQ-001-001
Title: Security - User Login - Positive Test
Type: security
Priority: High
Description: Verify User Login works correctly with valid inputs

Preconditions:
  • System is in stable state
  • All required services are running

Test Steps:
  1. Navigate to login page
  2. Enter valid email address
  3. Enter valid password
  4. Click Submit/Confirm button
  5. Verify the success message is displayed

Expected Result: System should process the request successfully and display appropriate success message

Test Data:
{
  "email": "test.user@example.com",
  "password": "ValidPass123!"
}

Status: Not Executed
```

## 🎯 Use Cases

1. **Agile Teams**: Quickly generate test cases during sprint planning
2. **Test Automation**: Export JSON to feed into automation frameworks
3. **Documentation**: Create test case documentation for audits
4. **Training**: Help new QA engineers learn test case structure
5. **Coverage Analysis**: Identify gaps in test coverage

## 🔄 Workflow Integration

### CI/CD Pipeline
```bash
# Generate test cases from requirements.json
python -c "
import json
from app import NLPTestCaseGenerator

with open('requirements.json') as f:
    reqs = json.load(f)
    
generator = NLPTestCaseGenerator()
test_cases = generator.generate_test_cases(reqs)

with open('test_cases.json', 'w') as f:
    json.dump(test_cases, f, indent=2)
"
```

### Selenium Integration
```python
import json

# Load generated test cases
with open('test_cases.json') as f:
    data = json.load(f)
    test_cases = data['test_cases']

# Convert to automated tests
for tc in test_cases:
    if tc['type'] == 'functional':
        # Generate Selenium test
        test_data = tc['test_data']
        steps = tc['steps']
        # ... implement test automation
```

## 📈 Analytics Features

The tool provides comprehensive analytics:
- **Test Distribution**: By type, priority, and requirement
- **Coverage Metrics**: Test cases per requirement
- **Priority Analysis**: High/Medium/Low distribution
- **Visual Charts**: Bar charts for quick insights
## Screenshots
<img width="1917" height="1051" alt="image" src="https://github.com/user-attachments/assets/ae937a1a-f65c-486a-923c-782153f39ba1" />
<img width="1919" height="1047" alt="image" src="https://github.com/user-attachments/assets/53547e09-abbf-4ae0-8d1d-2c1daa010076" />
<img width="1919" height="968" alt="image" src="https://github.com/user-attachments/assets/cdb33940-495d-4543-8fb0-27f2b9bf7c5b" />
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/c7549b69-95aa-4506-89a0-5969607ef8b6" />
<img width="1919" height="1023" alt="image" src="https://github.com/user-attachments/assets/429f7412-218a-41d7-b5f3-57e190fec1b7" />
<img width="1897" height="1051" alt="image" src="https://github.com/user-attachments/assets/3db219cb-45ae-4efa-8a93-7a572de3e914" />
<img width="1497" height="798" alt="image" src="https://github.com/user-attachments/assets/3eff902f-783f-43bc-a174-72b491c44d53" />
<img width="1908" height="1074" alt="image" src="https://github.com/user-attachments/assets/6c3decc0-4f24-4db9-96fa-48d06122ce7e" />
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/ae56b4f4-158d-4be9-a51f-0e321efb50dc" />
<img width="1914" height="1052" alt="image" src="https://github.com/user-attachments/assets/eb3abe77-bb38-43e2-9de2-1d9a6b1b5906" />
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/2eaf15b5-8333-4338-bb64-854f61f34c0d" />


## Live demo



## 🚧 Future Enhancements

- [ ] BDD/Gherkin format export
- [ ] JIRA/Azure DevOps integration
- [ ] Test case versioning
- [ ] AI-powered test data generation
- [ ] Defect prediction model
- [ ] Multi-language support
- [ ] Test case optimization (remove duplicates)
- [ ] Risk-based test prioritization

## 🤝 Contributing

This is a portfolio project, but suggestions are welcome! Feel free to:
1. Fork the repository
2. Create feature branches
3. Submit pull requests

## 📝 License

MIT License - feel free to use this for your projects, portfolios, or interviews.

## 👨‍💻 Author

Created for demonstrating AI + Testing expertise in technical interviews.

## 🙏 Acknowledgments

- Streamlit for the amazing framework
- OpenAI for GPT models
- The software testing community for best practices

## 📞 Support

For questions or issues:
1. Check the FAQ section below
2. Review the code comments
3. Test with sample requirements first

## ❓ FAQ

**Q: Do I need an OpenAI API key?**
A: No! The tool works perfectly with the built-in NLP engine. OpenAI is optional for enhanced generation.

**Q: Can this handle large requirement documents?**
A: Yes! It processes requirements in batches and can handle hundreds of requirements.

**Q: What's the test case format?**
A: Standard format with ID, title, steps, expected results, preconditions, and test data.

**Q: Can I customize the test types?**
A: Yes! Edit the `test_case_templates` dictionary in the code.

**Q: How accurate is the NLP engine?**
A: It extracts ~80-90% of relevant information from well-written requirements. GPT mode is more comprehensive.

**Q: Can I integrate this with my testing tools?**
A: Yes! Export to JSON and use it with any tool that accepts JSON input.

