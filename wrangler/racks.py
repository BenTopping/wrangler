from .helper import parse_tube_rack_csv, send_request_to_sequencescape, wrangle_tubes
from http import HTTPStatus

from flask import Blueprint, current_app as app


bp = Blueprint("racks", __name__)


@bp.route("/tube_rack/<tube_rack_barcode>")
def get_tubes_from_rack_barcode(tube_rack_barcode: str):
    """A Flask route which expects a tube rack barcode and returns the tubes in the rack with
    their coordinates.

    Arguments:
        tube_rack_barcode {str} -- the barcode on the tube rack

    Returns:
        [type] -- [description]
    """
    try:
        return parse_tube_rack_csv(tube_rack_barcode)
    except ValueError as e:
        app.logger.warning(e)
        return {"error": str(e)}, HTTPStatus.NOT_FOUND
    except Exception as e:
        app.logger.error(e)
        return {"error": f"Server error: {e}"}, HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route("/wrangle/<tube_rack_barcode>")
def wrangle(tube_rack_barcode: str):
    """A Flask route which accepts a tube rack barcode, then verifies if it exists in a particular
    MLWH table and if so generates a request body to send to Sequencescape.

    Arguments:
        tube_rack_barcode {str} -- The barcode of the tube rack

    Returns:
        ... --
    """
    try:
        app.logger.debug(f"tube_rack_barcode: {tube_rack_barcode}")

        tube_request_body = wrangle_tubes(tube_rack_barcode)
        send_request_to_sequencescape(tube_request_body)

        return "POST request successfully sent to Sequencescape", HTTPStatus.OK
    except ValueError as e:
        app.logger.warning(e)
        return {"error": str(e.message)}, HTTPStatus.NOT_FOUND
    except Exception as e:
        return {"error": f"Server error: {e}"}, HTTPStatus.NOT_FOUND
