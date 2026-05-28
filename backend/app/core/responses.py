def success_response(data=None, message: str = "Success", status_code: int = 200):
    return {
        "success": True,
        "message": message,
        "data":    data,
    }, status_code


def list_response(data: list, message: str = "Success", status_code: int = 200):
    return {
        "success": True,
        "message": message,
        "data":    data,
        "total":   len(data),
    }, status_code


def message_response(message: str, status_code: int = 200):
    return {
        "success": True,
        "message": message,
        "data":    None,
    }, status_code


def created_response(data=None, message: str = "Created successfully"):
    return success_response(data, message, 201)