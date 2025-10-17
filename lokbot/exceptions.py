class ApiException(Exception):
    def __str__(self):
        return f"API Exception: {super().__str__() or 'Unknown API error'}"


class RetryableApiException(ApiException):
    def __str__(self):
        return f"Retryable API Exception: {super().__str__() or 'Request can be retried'}"


class FatalApiException(ApiException):
    def __str__(self):
        return f"Fatal API Exception: {super().__str__() or 'Critical error occurred'}"


class NoAuthException(FatalApiException):
    def __str__(self):
        return "Authentication failed: Invalid or expired token"


class NeedCaptchaException(FatalApiException):
    def __str__(self):
        return "Captcha required: Bot detection triggered"


class NotOnlineException(FatalApiException):
    def __str__(self):
        return "Not online: Account is not currently online or accessible"


class OtherException(FatalApiException):
    def __init__(self, error_code=None):
        super().__init__()
        self.error_code = error_code
    
    def __str__(self):
        if self.error_code:
            return f"API Error: {self.error_code}"
        return "Unknown API error occurred"


class DuplicatedException(RetryableApiException):
    def __str__(self):
        return "Request duplicated: Server-side rate limiter triggered"


class ExceedLimitPacketException(RetryableApiException):
    def __str__(self):
        return "Rate limit exceeded: Too many requests, waiting 1 hour"
