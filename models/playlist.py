class Playlist:
    def __init__(self, name: str = "My Playlist", description: str = ""):
        self.name: str = name
        self.description: str = description

    def __repr__(self) -> str:
        return f"Playlist(name='{self.name}')"

    def __str__(self) -> str:
        return self.name
