#!/usr/bin/env python
"""
Error handling module for the E-commerce API application.
Provides standardized error responses and custom exception classes.
"""
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from typing import Any, Dict, List, Optional, Union


class BaseAPIError(Exception):
    """Base class for all API errors"""
    
    def __init__(
        self, 
        status_code: int, 
        message: str, 
        detail: Optional[Union[str, Dict[str, Any], List[Dict[str, Any]]]] = None,
        code: Optional[str] = None
    ):
        self.status_code = status_code
        self.message = message
        self.detail = detail
        self.code = code or f"ERR_{status_code}"
        super().__init__(self.message)


class NotFoundError(BaseAPIError):
    """Resource not found error"""
    
    def __init__(
        self, 
        message: str = "Resource not found", 
        detail: Optional[Union[str, Dict[str, Any], List[Dict[str, Any]]]] = None,
        code: Optional[str] = None
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=message,
            detail=detail,
            code=code or "ERR_NOT_FOUND"
        )


class ValidationError(BaseAPIError):
    """Input validation error"""
    
    def __init__(
        self, 
        message: str = "Validation error", 
        detail: Optional[Union[str, Dict[str, Any], List[Dict[str, Any]]]] = None,
        code: Optional[str] = None
    ):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message=message,
            detail=detail,
            code=code or "ERR_VALIDATION"
        )


class AuthorizationError(BaseAPIError):
    """Authorization error"""
    
    def __init__(
        self, 
        message: str = "Not authorized", 
        detail: Optional[Union[str, Dict[str, Any], List[Dict[str, Any]]]] = None,
        code: Optional[str] = None
    ):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message=message,
            detail=detail,
            code=code or "ERR_FORBIDDEN"
        )


class AuthenticationError(BaseAPIError):
    """Authentication error"""
    
    def __init__(
        self, 
        message: str = "Authentication required", 
        detail: Optional[Union[str, Dict[str, Any], List[Dict[str, Any]]]] = None,
        code: Optional[str] = None
    ):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message,
            detail=detail,
            code=code or "ERR_UNAUTHORIZED"
        )


class ConflictError(BaseAPIError):
    """Conflict error"""
    
    def __init__(
        self, 
        message: str = "Resource conflict", 
        detail: Optional[Union[str, Dict[str, Any], List[Dict[str, Any]]]] = None,
        code: Optional[str] = None
    ):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            message=message,
            detail=detail,
            code=code or "ERR_CONFLICT"
        )


class ServerError(BaseAPIError):
    """Internal server error"""
    
    def __init__(
        self, 
        message: str = "Internal server error", 
        detail: Optional[Union[str, Dict[str, Any], List[Dict[str, Any]]]] = None,
        code: Optional[str] = None
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            detail=detail,
            code=code or "ERR_INTERNAL"
        )


class ErrorResponseModel:
    """Standard error response model"""
    
    @staticmethod
    def create(
        status_code: int,
        message: str,
        detail: Optional[Union[str, Dict[str, Any], List[Dict[str, Any]]]] = None,
        code: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a standardized error response"""
        response = {
            "success": False,
            "error": {
                "code": code or f"ERR_{status_code}",
                "message": message,
            }
        }
        
        if detail:
            response["error"]["detail"] = detail
            
        return response


async def api_exception_handler(request: Request, exc: BaseAPIError) -> JSONResponse:
    """Handler for custom API exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponseModel.create(
            status_code=exc.status_code,
            message=exc.message,
            detail=exc.detail,
            code=exc.code
        )
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handler for HTTPException"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponseModel.create(
            status_code=exc.status_code,
            message=exc.detail,
            code=f"ERR_{exc.status_code}"
        )
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handler for validation errors"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponseModel.create(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message="Validation error",
            detail=[{"loc": err["loc"], "msg": err["msg"], "type": err["type"]} for err in exc.errors()],
            code="ERR_VALIDATION"
        )
    )


async def default_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Default handler for unhandled exceptions"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponseModel.create(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal server error",
            code="ERR_INTERNAL"
        )
    ) 