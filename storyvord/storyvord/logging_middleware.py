import logging
import json

class RequestResponseLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger = logging.getLogger('django.request')  # Use the request-specific logger

        # Log the incoming request details
        logger.debug("Incoming Request:")
        logger.debug(f"  Method: {request.method}")
        logger.debug(f"  URL: {request.get_full_path()}")
        
        if request.body:
            try:
                # Attempt to load and pretty-print the request body JSON
                request_data = json.loads(request.body.decode('utf-8'))
                formatted_request_body = json.dumps(request_data, indent=4)
            except (json.JSONDecodeError, UnicodeDecodeError):
                # If the body is not valid JSON, fall back to plain decoding
                formatted_request_body = request.body.decode('utf-8', errors='ignore')

            # Log the formatted request body
            logger.debug("  Request Body:")
            logger.debug(formatted_request_body)

        # Get the response
        response = self.get_response(request)

        # Log the outgoing response details
        logger.debug("Outgoing Response:")
        logger.debug(f"  Status: {response.status_code}")
        
        if hasattr(response, 'content'):
            try:
                # Attempt to load and pretty-print the response body JSON
                response_data = json.loads(response.content.decode('utf-8'))
                formatted_response_content = json.dumps(response_data, indent=4)
            except (json.JSONDecodeError, UnicodeDecodeError):
                # If the content is not valid JSON, fall back to plain decoding
                formatted_response_content = response.content.decode('utf-8', errors='ignore')

            # Log the formatted response content
            logger.debug("  Response Content:")
            logger.debug(formatted_response_content)

        return response


# Custom Filter to Exclude `autoreload` Logs
class ExcludeAutoreloadFilter(logging.Filter):
    def filter(self, record):
        # Exclude logs starting with the string "File"
        return not record.getMessage().startswith('File')