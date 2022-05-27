from dataclasses import dataclass

@dataclass
class Signal:
	market        : str
	side          : str
	position_side : str
	size          : float = None
	portion       : float = None
	sl            : float = None
	limit         : float = None
	tp            : float = None
