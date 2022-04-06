from os import environ


def get_doctors() -> list[str]:
    doctors_: list[str] = [d.strip() for d in environ.get("DOCTORS", "").split(',')]
    return doctors_


def get_clinics() -> list[str]:
    clinics_: list[str] = [d.strip() for d in environ.get("CLINICS", "").split(',')]
    return clinics_


is_online = bool(environ.get("IS_ONLINE", 0))
dms = bool(environ.get("DMS", 0))
doctors = get_doctors()
clinics = get_clinics()
