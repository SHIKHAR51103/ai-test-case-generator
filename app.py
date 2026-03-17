import streamlit as st
import json
from datetime import datetime
import pandas as pd
from typing import List, Dict
import re

# Set page config
st.set_page_config(
    page_title="AI Test Case Generator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .test-case-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #1f77b4;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .success-msg {
        color: #28a745;
        font-weight: bold;
    }
    .warning-msg {
        color: #ffc107;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


class NLPTestCaseGenerator:
    """
    AI-powered test case generator using NLP techniques
    Falls back to rule-based NLP if OpenAI API is not available
    """

    def __init__(self, use_openai=False, api_key=None):
        self.use_openai = use_openai
        self.api_key = api_key
        self.test_case_templates = {
            'functional': ['positive', 'negative', 'boundary'],
            'ui': ['layout', 'responsiveness', 'navigation'],
            'performance': ['load_time', 'concurrent_users', 'data_volume'],
            'security': ['authentication', 'authorization', 'data_validation'],
            'integration': ['api', 'database', 'third_party']
        }

    def analyze_requirement(self, requirement_text: str) -> Dict:
        """Extract key information from requirement using NLP"""
        analysis = {
            'actions': [],
            'entities': [],
            'conditions': [],
            'test_types': [],
            'priority': 'Medium'
        }

        # Extract actions (verbs)
        action_keywords = ['create', 'update', 'delete', 'view', 'search', 'login',
                           'logout', 'submit', 'validate', 'process', 'generate',
                           'calculate', 'send', 'receive', 'display', 'filter',
                           'sort', 'export', 'import', 'upload', 'download']

        for keyword in action_keywords:
            if keyword.lower() in requirement_text.lower():
                analysis['actions'].append(keyword)

        # Extract entities (nouns)
        entity_keywords = ['user', 'admin', 'customer', 'product', 'order', 'payment',
                           'account', 'profile', 'report', 'data', 'file', 'email',
                           'notification', 'dashboard', 'form', 'button', 'field']

        for keyword in entity_keywords:
            if keyword.lower() in requirement_text.lower():
                analysis['entities'].append(keyword)

        # Extract conditions
        condition_keywords = ['if', 'when', 'must', 'should', 'required', 'optional',
                              'valid', 'invalid', 'error', 'success']

        for keyword in condition_keywords:
            if keyword.lower() in requirement_text.lower():
                analysis['conditions'].append(keyword)

        # Determine test types
        if any(word in requirement_text.lower() for word in ['login', 'password', 'authentication', 'security']):
            analysis['test_types'].append('security')
        if any(word in requirement_text.lower() for word in ['api', 'integration', 'third-party']):
            analysis['test_types'].append('integration')
        if any(word in requirement_text.lower() for word in ['ui', 'interface', 'display', 'button']):
            analysis['test_types'].append('ui')
        if any(word in requirement_text.lower() for word in ['performance', 'load', 'speed']):
            analysis['test_types'].append('performance')

        if not analysis['test_types']:
            analysis['test_types'].append('functional')

        # Determine priority
        if any(word in requirement_text.lower() for word in ['critical', 'must', 'required', 'essential']):
            analysis['priority'] = 'High'
        elif any(word in requirement_text.lower() for word in ['should', 'recommended']):
            analysis['priority'] = 'Medium'
        else:
            analysis['priority'] = 'Low'

        return analysis

    def generate_test_cases_nlp(self, requirement: Dict) -> List[Dict]:
        """Generate test cases using rule-based NLP"""
        test_cases = []
        req_id = requirement.get('id', 'REQ-001')
        req_title = requirement.get('title', 'Requirement')
        req_description = requirement.get('description', '')

        # Analyze the requirement
        analysis = self.analyze_requirement(req_description)

        # Generate test cases based on analysis
        test_case_id = 1

        for test_type in analysis['test_types']:
            # Positive test case
            positive_tc = {
                'id': f'TC-{req_id}-{test_case_id:03d}',
                'title': f'{test_type.capitalize()} - {req_title} - Positive Test',
                'type': test_type,
                'priority': analysis['priority'],
                'description': f'Verify {req_title} works correctly with valid inputs',
                'preconditions': self._generate_preconditions(analysis, positive=True),
                'steps': self._generate_test_steps(analysis, req_description, positive=True),
                'expected_result': f'System should process the request successfully and display appropriate success message',
                'test_data': self._generate_test_data(analysis, positive=True),
                'status': 'Not Executed'
            }
            test_cases.append(positive_tc)
            test_case_id += 1

            # Negative test case
            negative_tc = {
                'id': f'TC-{req_id}-{test_case_id:03d}',
                'title': f'{test_type.capitalize()} - {req_title} - Negative Test',
                'type': test_type,
                'priority': analysis['priority'],
                'description': f'Verify {req_title} handles invalid inputs correctly',
                'preconditions': self._generate_preconditions(analysis, positive=False),
                'steps': self._generate_test_steps(analysis, req_description, positive=False),
                'expected_result': f'System should reject invalid input and display appropriate error message',
                'test_data': self._generate_test_data(analysis, positive=False),
                'status': 'Not Executed'
            }
            test_cases.append(negative_tc)
            test_case_id += 1

            # Boundary test case
            if test_type == 'functional':
                boundary_tc = {
                    'id': f'TC-{req_id}-{test_case_id:03d}',
                    'title': f'{test_type.capitalize()} - {req_title} - Boundary Test',
                    'type': test_type,
                    'priority': analysis['priority'],
                    'description': f'Verify {req_title} handles boundary values correctly',
                    'preconditions': self._generate_preconditions(analysis, positive=True),
                    'steps': self._generate_test_steps(analysis, req_description, boundary=True),
                    'expected_result': f'System should handle boundary values as per specifications',
                    'test_data': self._generate_test_data(analysis, boundary=True),
                    'status': 'Not Executed'
                }
                test_cases.append(boundary_tc)
                test_case_id += 1

        return test_cases

    def generate_test_cases_openai(self, requirement: Dict) -> List[Dict]:
        """Generate test cases using OpenAI API"""
        try:
            import openai
            openai.api_key = self.api_key

            prompt = f"""
            Generate comprehensive test cases for the following software requirement:

            Requirement ID: {requirement.get('id', 'REQ-001')}
            Title: {requirement.get('title', '')}
            Description: {requirement.get('description', '')}

            Generate at least 5 test cases covering:
            1. Positive scenarios
            2. Negative scenarios
            3. Boundary conditions
            4. Edge cases
            5. Security considerations

            For each test case, provide:
            - Test Case ID
            - Title
            - Type (functional/ui/performance/security/integration)
            - Priority (High/Medium/Low)
            - Description
            - Preconditions
            - Test Steps (as a list)
            - Expected Result
            - Test Data

            Return the response as a JSON array of test case objects.
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "You are an expert software testing engineer specializing in test case generation."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )

            test_cases_text = response.choices[0].message.content

            # Extract JSON from response
            json_match = re.search(r'\[.*\]', test_cases_text, re.DOTALL)
            if json_match:
                test_cases = json.loads(json_match.group())
                return test_cases
            else:
                st.warning("Failed to parse OpenAI response. Falling back to NLP-based generation.")
                return self.generate_test_cases_nlp(requirement)

        except Exception as e:
            st.warning(f"OpenAI API error: {str(e)}. Falling back to NLP-based generation.")
            return self.generate_test_cases_nlp(requirement)

    def _generate_preconditions(self, analysis: Dict, positive: bool = True) -> List[str]:
        """Generate preconditions based on analysis"""
        preconditions = []

        if 'user' in analysis['entities'] or 'login' in analysis['actions']:
            preconditions.append('User is logged into the system')

        if 'admin' in analysis['entities']:
            preconditions.append('User has admin privileges')

        if positive:
            preconditions.append('System is in stable state')
            preconditions.append('All required services are running')
        else:
            preconditions.append('Test environment is configured for error scenarios')

        return preconditions if preconditions else ['System is accessible']

    def _generate_test_steps(self, analysis: Dict, description: str, positive: bool = True, boundary: bool = False) -> \
    List[str]:
        """Generate test steps based on analysis"""
        steps = []

        # Start with navigation
        if 'login' in analysis['actions']:
            steps.append('Navigate to login page')
        else:
            steps.append('Navigate to the application')

        # Add action-based steps
        for action in analysis['actions'][:3]:  # Limit to first 3 actions
            if positive:
                steps.append(f'{action.capitalize()} the required information with valid data')
            elif boundary:
                steps.append(f'{action.capitalize()} the required information with boundary values')
            else:
                steps.append(f'{action.capitalize()} the required information with invalid data')

        # Add verification step
        if positive:
            steps.append('Click Submit/Confirm button')
            steps.append('Verify the success message is displayed')
        else:
            steps.append('Attempt to Submit/Confirm')
            steps.append('Verify appropriate error message is displayed')

        return steps if steps else ['Execute the functionality', 'Verify the result']

    def _generate_test_data(self, analysis: Dict, positive: bool = True, boundary: bool = False) -> Dict:
        """Generate test data based on analysis"""
        test_data = {}

        if 'email' in analysis['entities'] or 'login' in analysis['actions']:
            if positive:
                test_data['email'] = 'test.user@example.com'
                test_data['password'] = 'ValidPass123!'
            elif boundary:
                test_data['email'] = 'a@b.c'  # Minimum valid email
                test_data['password'] = 'Pass1!'  # Minimum length
            else:
                test_data['email'] = 'invalid-email'
                test_data['password'] = '123'

        if 'user' in analysis['entities'] or 'profile' in analysis['entities']:
            if positive:
                test_data['username'] = 'testuser'
                test_data['name'] = 'Test User'
            else:
                test_data['username'] = ''
                test_data['name'] = 'A' * 300  # Too long

        if boundary:
            test_data['note'] = 'Testing boundary conditions with edge values'

        return test_data if test_data else {'input': 'Sample test data'}

    def generate_test_cases(self, requirements: List[Dict]) -> List[Dict]:
        """Main method to generate test cases"""
        all_test_cases = []

        for requirement in requirements:
            if self.use_openai and self.api_key:
                test_cases = self.generate_test_cases_openai(requirement)
            else:
                test_cases = self.generate_test_cases_nlp(requirement)

            all_test_cases.extend(test_cases)

        return all_test_cases


def export_test_cases_json(test_cases: List[Dict], filename: str = None):
    """Export test cases to JSON file"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_cases_{timestamp}.json"

    export_data = {
        'metadata': {
            'generated_date': datetime.now().isoformat(),
            'total_test_cases': len(test_cases),
            'generator': 'AI-Powered Test Case Generator'
        },
        'test_cases': test_cases
    }

    return json.dumps(export_data, indent=2)


def export_test_cases_excel(test_cases: List[Dict]):
    """Export test cases to Excel format"""
    # Flatten test cases for Excel
    flattened_data = []
    for tc in test_cases:
        flat_tc = {
            'Test Case ID': tc['id'],
            'Title': tc['title'],
            'Type': tc['type'],
            'Priority': tc['priority'],
            'Description': tc['description'],
            'Preconditions': '\n'.join(tc['preconditions']),
            'Test Steps': '\n'.join([f"{i + 1}. {step}" for i, step in enumerate(tc['steps'])]),
            'Expected Result': tc['expected_result'],
            'Test Data': json.dumps(tc['test_data'], indent=2),
            'Status': tc['status']
        }
        flattened_data.append(flat_tc)

    return pd.DataFrame(flattened_data)


def main():
    # Header
    st.markdown('<div class="main-header">🤖 AI-Powered Test Case Generator</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Transform Software Requirements into Comprehensive Test Cases using NLP & AI</div>',
        unsafe_allow_html=True)

    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")

        # API Selection
        use_openai = st.checkbox("Use OpenAI API (Optional)", value=False,
                                 help="Enable for GPT-powered test case generation. Falls back to NLP if unavailable.")

        api_key = None
        if use_openai:
            api_key = st.text_input("OpenAI API Key", type="password",
                                    help="Enter your OpenAI API key for enhanced test case generation")

        st.markdown("---")

        # Statistics (placeholder)
        st.subheader("📊 Session Statistics")
        if 'test_cases' in st.session_state:
            st.metric("Total Test Cases", len(st.session_state.test_cases))
            st.metric("Requirements Processed", len(st.session_state.requirements))
        else:
            st.metric("Total Test Cases", 0)
            st.metric("Requirements Processed", 0)

        st.markdown("---")

        # About
        st.subheader("ℹ️ About")
        st.info("""
        This tool uses NLP and AI to automatically generate comprehensive test cases from software requirements.

        **Features:**
        - Rule-based NLP analysis
        - OpenAI GPT integration (optional)
        - Multiple test types
        - JSON/Excel export
        - Comprehensive coverage
        """)

    # Initialize session state
    if 'requirements' not in st.session_state:
        st.session_state.requirements = []
    if 'test_cases' not in st.session_state:
        st.session_state.test_cases = []

    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Input Requirements", "🧪 Generated Test Cases", "📊 Analytics", "💾 Export"])

    with tab1:
        st.header("Input Software Requirements")

        # Option to input requirements
        input_method = st.radio("Choose input method:",
                                ["Manual Entry", "Upload JSON", "Sample Requirements"])

        if input_method == "Manual Entry":
            with st.form("requirement_form"):
                col1, col2 = st.columns(2)

                with col1:
                    req_id = st.text_input("Requirement ID", value="REQ-001",
                                           help="Unique identifier for the requirement")
                    req_title = st.text_input("Requirement Title",
                                              help="Short title describing the requirement")

                with col2:
                    req_priority = st.selectbox("Priority", ["High", "Medium", "Low"])
                    req_category = st.selectbox("Category",
                                                ["Functional", "UI/UX", "Performance",
                                                 "Security", "Integration"])

                req_description = st.text_area("Requirement Description",
                                               height=150,
                                               help="Detailed description of the requirement",
                                               placeholder="Example: The system shall allow users to login using email and password. The password must be at least 8 characters with one uppercase letter and one number.")

                submitted = st.form_submit_button("Add Requirement", type="primary")

                if submitted and req_description:
                    requirement = {
                        'id': req_id,
                        'title': req_title,
                        'description': req_description,
                        'priority': req_priority,
                        'category': req_category
                    }
                    st.session_state.requirements.append(requirement)
                    st.success(f"✅ Requirement {req_id} added successfully!")

        elif input_method == "Upload JSON":
            uploaded_file = st.file_uploader("Upload Requirements JSON", type=['json'])
            if uploaded_file:
                try:
                    requirements_data = json.load(uploaded_file)
                    if isinstance(requirements_data, list):
                        st.session_state.requirements = requirements_data
                    elif 'requirements' in requirements_data:
                        st.session_state.requirements = requirements_data['requirements']
                    st.success(f"✅ Loaded {len(st.session_state.requirements)} requirements!")
                except Exception as e:
                    st.error(f"Error loading JSON: {str(e)}")

        else:  # Sample Requirements
            if st.button("Load Sample Requirements", type="primary"):
                st.session_state.requirements = [
                    {
                        'id': 'REQ-001',
                        'title': 'User Login Functionality',
                        'description': 'The system shall allow users to login using their email address and password. The password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character. After 3 failed login attempts, the account should be locked for 15 minutes.',
                        'priority': 'High',
                        'category': 'Security'
                    },
                    {
                        'id': 'REQ-002',
                        'title': 'Product Search Feature',
                        'description': 'Users should be able to search for products using keywords. The search should be case-insensitive and support partial matching. Results should be displayed with product name, price, and image. The system should handle at least 1000 concurrent search requests.',
                        'priority': 'High',
                        'category': 'Functional'
                    },
                    {
                        'id': 'REQ-003',
                        'title': 'Shopping Cart Management',
                        'description': 'Users must be able to add, update, and remove items from their shopping cart. The cart should persist across sessions. The system should calculate the total price including taxes and display it to the user. Maximum 50 items can be added to the cart.',
                        'priority': 'Medium',
                        'category': 'Functional'
                    }
                ]
                st.success("✅ Sample requirements loaded!")

        # Display current requirements
        if st.session_state.requirements:
            st.subheader(f"Current Requirements ({len(st.session_state.requirements)})")
            for idx, req in enumerate(st.session_state.requirements):
                with st.expander(f"{req['id']}: {req['title']}"):
                    st.write(f"**Priority:** {req.get('priority', 'N/A')}")
                    st.write(f"**Category:** {req.get('category', 'N/A')}")
                    st.write(f"**Description:** {req['description']}")
                    if st.button(f"Remove", key=f"remove_{idx}"):
                        st.session_state.requirements.pop(idx)
                        st.rerun()

        # Generate test cases button
        st.markdown("---")
        if st.session_state.requirements:
            if st.button("🚀 Generate Test Cases", type="primary", use_container_width=True):
                with st.spinner("Generating test cases using AI..."):
                    generator = NLPTestCaseGenerator(use_openai=use_openai, api_key=api_key)
                    st.session_state.test_cases = generator.generate_test_cases(st.session_state.requirements)
                    st.success(f"✅ Successfully generated {len(st.session_state.test_cases)} test cases!")
                    st.balloons()

    with tab2:
        st.header("Generated Test Cases")

        if not st.session_state.test_cases:
            st.info("👆 Generate test cases from the 'Input Requirements' tab first.")
        else:
            # Filters
            col1, col2, col3 = st.columns(3)

            with col1:
                filter_type = st.multiselect("Filter by Type",
                                             options=['functional', 'ui', 'performance', 'security', 'integration'],
                                             default=[])
            with col2:
                filter_priority = st.multiselect("Filter by Priority",
                                                 options=['High', 'Medium', 'Low'],
                                                 default=[])
            with col3:
                search_term = st.text_input("Search Test Cases", placeholder="Enter keywords...")

            # Apply filters
            filtered_cases = st.session_state.test_cases

            if filter_type:
                filtered_cases = [tc for tc in filtered_cases if tc['type'] in filter_type]
            if filter_priority:
                filtered_cases = [tc for tc in filtered_cases if tc['priority'] in filter_priority]
            if search_term:
                filtered_cases = [tc for tc in filtered_cases
                                  if search_term.lower() in tc['title'].lower()
                                  or search_term.lower() in tc['description'].lower()]

            st.write(f"Showing {len(filtered_cases)} of {len(st.session_state.test_cases)} test cases")

            # Display test cases
            for tc in filtered_cases:
                with st.expander(f"**{tc['id']}** - {tc['title']} [{tc['type'].upper()}] - Priority: {tc['priority']}"):
                    col1, col2 = st.columns([2, 1])

                    with col1:
                        st.write(f"**Description:** {tc['description']}")

                        st.write("**Preconditions:**")
                        for precond in tc['preconditions']:
                            st.write(f"  • {precond}")

                        st.write("**Test Steps:**")
                        for idx, step in enumerate(tc['steps'], 1):
                            st.write(f"  {idx}. {step}")

                        st.write(f"**Expected Result:** {tc['expected_result']}")

                    with col2:
                        st.write("**Test Data:**")
                        st.json(tc['test_data'])

                        st.write(f"**Status:** {tc['status']}")

                        # Update status
                        new_status = st.selectbox("Update Status",
                                                  ["Not Executed", "Pass", "Fail", "Blocked"],
                                                  key=f"status_{tc['id']}")
                        if new_status != tc['status']:
                            tc['status'] = new_status

    with tab3:
        st.header("Test Coverage Analytics")

        if not st.session_state.test_cases:
            st.info("👆 Generate test cases to view analytics.")
        else:
            # Metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Test Cases", len(st.session_state.test_cases))
            with col2:
                high_priority = len([tc for tc in st.session_state.test_cases if tc['priority'] == 'High'])
                st.metric("High Priority", high_priority)
            with col3:
                types_count = len(set(tc['type'] for tc in st.session_state.test_cases))
                st.metric("Test Types", types_count)
            with col4:
                avg_steps = sum(len(tc['steps']) for tc in st.session_state.test_cases) / len(
                    st.session_state.test_cases)
                st.metric("Avg Steps/Test", f"{avg_steps:.1f}")

            # Charts
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Test Cases by Type")
                type_counts = pd.Series([tc['type'] for tc in st.session_state.test_cases]).value_counts()
                st.bar_chart(type_counts)

            with col2:
                st.subheader("Test Cases by Priority")
                priority_counts = pd.Series([tc['priority'] for tc in st.session_state.test_cases]).value_counts()
                st.bar_chart(priority_counts)

            # Test case distribution table
            st.subheader("Test Case Distribution")
            distribution_data = []
            for req in st.session_state.requirements:
                req_test_cases = [tc for tc in st.session_state.test_cases if req['id'] in tc['id']]
                distribution_data.append({
                    'Requirement ID': req['id'],
                    'Requirement Title': req['title'],
                    'Test Cases Generated': len(req_test_cases),
                    'High Priority': len([tc for tc in req_test_cases if tc['priority'] == 'High']),
                    'Medium Priority': len([tc for tc in req_test_cases if tc['priority'] == 'Medium']),
                    'Low Priority': len([tc for tc in req_test_cases if tc['priority'] == 'Low'])
                })

            if distribution_data:
                st.dataframe(pd.DataFrame(distribution_data), use_container_width=True)

    with tab4:
        st.header("Export Test Cases")

        if not st.session_state.test_cases:
            st.info("👆 Generate test cases to export them.")
        else:
            st.write(f"Ready to export {len(st.session_state.test_cases)} test cases")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📄 JSON Export")
                st.write("Export test cases in JSON format for integration with other tools.")

                json_data = export_test_cases_json(st.session_state.test_cases)

                st.download_button(
                    label="⬇️ Download JSON",
                    data=json_data,
                    file_name=f"test_cases_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )

                with st.expander("Preview JSON"):
                    st.code(json_data, language='json')

            with col2:
                st.subheader("📊 Excel Export")
                st.write("Export test cases in Excel format for easy sharing and review.")

                df = export_test_cases_excel(st.session_state.test_cases)

                # Convert to Excel bytes
                from io import BytesIO
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Test Cases')
                excel_data = output.getvalue()

                st.download_button(
                    label="⬇️ Download Excel",
                    data=excel_data,
                    file_name=f"test_cases_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

                with st.expander("Preview Excel Data"):
                    st.dataframe(df, use_container_width=True)

            # Summary report
            st.markdown("---")
            st.subheader("📋 Test Summary Report")

            summary_report = f"""
            # Test Case Generation Summary

            **Generated Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

            ## Overview
            - **Total Requirements:** {len(st.session_state.requirements)}
            - **Total Test Cases:** {len(st.session_state.test_cases)}
            - **Average Test Cases per Requirement:** {len(st.session_state.test_cases) / len(st.session_state.requirements):.1f}

            ## Test Case Breakdown
            """

            for test_type in ['functional', 'ui', 'performance', 'security', 'integration']:
                count = len([tc for tc in st.session_state.test_cases if tc['type'] == test_type])
                if count > 0:
                    summary_report += f"- **{test_type.capitalize()}:** {count}\n"

            summary_report += "\n## Priority Distribution\n"
            for priority in ['High', 'Medium', 'Low']:
                count = len([tc for tc in st.session_state.test_cases if tc['priority'] == priority])
                summary_report += f"- **{priority}:** {count}\n"

            st.markdown(summary_report)

            st.download_button(
                label="⬇️ Download Summary Report (Markdown)",
                data=summary_report,
                file_name=f"test_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True
            )


if __name__ == "__main__":
    main()
