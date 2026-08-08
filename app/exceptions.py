class ClinicError(Exception):
    pass

class SlotNotFoundError(ClinicError):
    pass

class SlotAlreadyBookedError(ClinicError):
    pass

class UserAlreadyExistsError(ClinicError):
    pass

class InvalidCredentialsError(ClinicError):
    pass