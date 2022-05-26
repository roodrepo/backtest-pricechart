from dataclasses import dataclass

@dataclass
class Signal:
	market        : str
	side          : str
	position_side : str
	size          : float
	portion       : float
	sl            : float
	limit         : float
	tp            : float
