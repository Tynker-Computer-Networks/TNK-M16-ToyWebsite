from flask import Blueprint
from controllers.controller import index, login, logout, profile, order, addAddress, addToCart, cart, placeOrder, generateReceipt

blueprint = Blueprint('blueprint', __name__)

blueprint.route('/', methods=['GET'])(index)
blueprint.route('/login', methods=['GET', 'POST'])(login)
blueprint.route('/logout', methods=['GET'])(logout)
blueprint.route("/order", methods=['GET', 'POST'])(order)
blueprint.route("/placeOrder", methods=['GET', 'POST'])(placeOrder)
blueprint.route("/addAddress", methods=["POST"])(addAddress)
blueprint.route("/addToCart", methods=["POST"])(addToCart)
blueprint.route("/profile", methods=['GET',"POST"])(profile)
blueprint.route("/cart", methods=['GET',"POST"])(cart)

blueprint.route("/generateReceipt", methods=["GET","POST"])(generateReceipt)