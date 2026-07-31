class ClinicError(Exception):
    pass

class SlotNotFoundError(ClinicError):
    pass

class SlotAlreadyBookedError(ClinicError):
    pass