from pathlib import Path


def ensure_dir(path: str | Path) -> Path:
    """
    Creates directory if it does not exist and returns a Path object.
    
    Args:
        path: Directory path to create (can be string or Path object)
        
    Returns:
        Path object of the created/existing directory
    """
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p
