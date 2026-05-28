from fastapi.responses import JSONResponse

def custom_error(message):

    return JSONResponse(
        status_code=500,
        content={
            "error": message
        }
    )