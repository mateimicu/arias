"""Version info."""
import pbr.version


def get_version():
    """Obtain the project version."""
    version = pbr.version.VersionInfo('arias')
    return version.release_string()
