from .Error import ResponseDict, ErrorCode


def output_response(name: str):
    def new_func(func):
        def parse_output_response(*args, **kwargs):
            try:
                res = func(*args, **kwargs)
                return ResponseDict(ErrorCode.success, **{name: res})
            except PermissionError:
                return ResponseDict(ErrorCode.permisson_forbidden)
            except Exception:
                return ResponseDict(ErrorCode.internal_errors)

        return parse_output_response

    return new_func


def common_response(success_response=None):
    if success_response is None:
        success_response = ResponseDict(ErrorCode.success)

    def new_func(func):
        def parse_common_response(*args, **kwargs):
            try:
                func(*args, **kwargs)
                return success_response
            except PermissionError:
                return ResponseDict(ErrorCode.permisson_forbidden)
            except Exception:
                return ResponseDict(ErrorCode.internal_errors)

        return parse_common_response

    return new_func
