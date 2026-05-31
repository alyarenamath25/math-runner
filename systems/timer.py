class GameTimer:
    """
    Timer countdown yang TIDAK PERNAH berhenti (sesuai GDD).
    add_time() digunakan untuk bonus waktu saat jawaban benar.
    """
    # Setup timer
    def __init__(self, initial_seconds: float):
        self.reset(initial_seconds)

    # Hitung mundur
    def update(self, dt: float) -> bool:
        """Kurangi waktu. Return True jika waktu habis (times up)."""
        if not self._active: 
            return False
            
        self.remaining -= dt
        if self.remaining <= 0:
            self.remaining = 0
            self._active = False
            return True
        return False

    def add_time(self, seconds: float):
        """Tambah waktu bonus (jawaban benar = +3 detik)."""
        self.remaining += seconds
        if not self._active and self.remaining > 0:
            self._active = True

    # Format jam digital
    def get_display(self) -> str:
        """Return string format MM:SS untuk HUD."""
        total_secs = max(0, int(self.remaining))
        mins = total_secs // 60
        secs = total_secs % 60
        return f"{mins:02d}:{secs:02d}"

    def reset(self, initial_seconds: float):
        """Reset timer ke nilai awal (Play Again)."""
        self.remaining = float(initial_seconds)
        self._active = True