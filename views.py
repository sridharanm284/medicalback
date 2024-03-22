from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
from django.http import JsonResponse
import joblib , pickle
import os



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



# # Assuming the trained model file is named trained_model.pkl and is inside the csv folder
# trained_model_path = os.path.join(os.path.dirname(__file__), 'csv', 'trained_model.pkl')

# def predict_view(request):
#     # Load the trained model
#     model = joblib.load(trained_model_path)

#     # Get input data from the request
#     input_data = request.POST.get('input_data')

#     # Perform prediction using the loaded model
#     prediction = model.predict([input_data])

#     # Return the prediction as a JSON response
#     return JsonResponse({'prediction': prediction})
    


import os
import pickle
import json
import numpy as np
from django.http import JsonResponse

def check_data_view(request):
    try:
        # Define the path to the trained model pickle file
        trained_model_path = os.path.join(os.path.dirname(__file__), 'csv', 'trained_model1.pkl')
        
        # Check if the pickle file exists
        if os.path.exists(trained_model_path):
            # Load the trained model
            with open(trained_model_path, 'rb') as f:
                loaded_data = pickle.load(f)
            
            # Serialize the loaded data
            serialized_data = json.dumps(loaded_data, default=lambda x: x.tolist() if isinstance(x, np.ndarray) else x)
            
            # Return a success response with the serialized data
            return JsonResponse({'status': 'success', 'message': 'Data loaded successfully', 'loaded_data': serialized_data})
        else:
            # Return an error response if the file does not exist
            return JsonResponse({'status': 'error', 'message': f'Trained model file not found at {trained_model_path}'}, status=404)
    except Exception as e:
        # Return an error response if an exception occurs
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


from django.views.generic import View
from django.http import JsonResponse
from django.middleware.csrf import get_token

class GetCSRFTokenView(View):
    def get(self, request, *args, **kwargs):
        csrf_token = get_token(request)
        return JsonResponse({'csrfToken': csrf_token})
    


