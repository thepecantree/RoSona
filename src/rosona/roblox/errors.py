class RobloxError(Exception):
    pass


class RobloxNotFound(RobloxError):
    pass


class RobloxUnauthorized(RobloxError):
    pass


class RobloxRateLimited(RobloxError):
    pass


class RobloxServerError(RobloxError):
    pass