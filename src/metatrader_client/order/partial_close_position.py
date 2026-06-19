from typing import Union

from ..types import TradeRequestActions
from .send_order import send_order
from .get_positions_by_id import get_positions_by_id


def partial_close_position(connection, id: Union[str, int], volume: float):

    try:
        position_id = int(id)
    except (TypeError, ValueError):
        return {"success": False, "error": "Invalid position id"}

    positions = get_positions_by_id(connection, position_id)

    if positions is None or len(positions) == 0:
        return {"success": False, "error": "Position not found"}

    position = positions[0]

    if volume <= 0:
        return {"success": False, "error": "Volume must be greater than zero"}

    if volume > float(position["volume"]):
        return {
            "success": False,
            "error": f"Requested volume {volume} exceeds position volume {position['volume']}"
        }

    return send_order(
        connection=connection,
        action=TradeRequestActions.DEAL,
        position=position_id,
        order_type="SELL" if position["type"] == "BUY" else "BUY",
        symbol=position["symbol"],
        volume=volume
    )
