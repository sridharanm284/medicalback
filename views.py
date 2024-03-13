from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd

# Define doctor ID and patient ID
DOCTOR_ID = '1234'
PATIENT_ID = '2222'

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        # Hardcoded credentials for testing
        test_credentials = {
            'admin': {'username': 'admin', 'password': 'admin', 'user_type': 'doctor', 'user_id': DOCTOR_ID},
            'user': {'username': 'user', 'password': 'user', 'user_type': 'patient', 'user_id': PATIENT_ID}
        }
        
        username = request.data.get('username')
        password = request.data.get('password')
        user_type = request.data.get('user_type')
        user_id = request.data.get('user_id')

        if not username or not password or not user_type or not user_id:
            return Response({'error': 'Username, password, user type, and user ID are required'}, status=400)

        # Check if the provided credentials match the hardcoded test credentials
        if username in test_credentials and test_credentials[username]['password'] == password:
            user_data = test_credentials[username]
            if user_data['user_type'] == user_type and user_data['user_id'] == user_id:
                # Process Excel file if uploaded
                if request.FILES.get('excel_file'):
                    excel_file = request.FILES['excel_file']
                    df = pd.read_excel(excel_file)
                    # Perform data preprocessing, model training, etc.
                    # Return response based on model predictions
                    # For now, let's return a success message
                    return Response({'user_type': user_type, 'user_id': user_id, 'message': 'Excel file processed successfully'})
                else:
                    return Response({'user_type': user_type, 'user_id': user_id})
            else:
                return Response({'error': 'Invalid user type or user ID'}, status=400)
        else:
            # Authentication failed
            return Response({'error': 'Invalid credentials'}, status=400)
    else:
        # Handle other HTTP methods
        return Response({'error': 'Method not allowed'}, status=405)
