import requests
import json
from datetime import datetime

def fetch_and_save_rank_data(user_id=130662, ApiKey = 'UOloNrq6hpoJfU2FmtsbXdz0TDh71wMYgQs2c773R8zyc'
                             , aiteam = 'aiteam' , output_file="backoff.json"):

    url = "https://aiapi.iyovia.com/rank"
    params = {
    "ApiUser": aiteam,
    "ApiKey": ApiKey,
    "UserId": user_id}

    headers = {
        "User-Agent": "PostmanRuntime/7.32.3",
        "Accept": "/"}
    
    try:
        response = requests.post(url, params=params, headers=headers)

        if response.status_code != 200:
            return {
                "success": False,
                "message": f"API request failed with status code: {response.status_code}",
                "status_code": response.status_code,
                "response_text": response.text[:500] if response.text else "No response text"
            }

        data = response.json()

        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        return {
            "success": True,
            "message": f"Data successfully saved to {output_file}",
            "file_path": output_file,
            "data_preview": str(data)[:100] + "..." if len(str(data)) > 100 else str(data)
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": f"Request failed: {str(e)}"
        }
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "message": f"Failed to decode JSON response: {str(e)}",
            "response_text": response.text[:500] if 'response' in locals() else "No response"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }

result = fetch_and_save_rank_data(user_id=130662, ApiKey = 'UOloNrq6hpoJfU2FmtsbXdz0TDh71wMYgQs2c773R8zyc' 
                             , aiteam = 'aiteam' , output_file="backoff.json")



