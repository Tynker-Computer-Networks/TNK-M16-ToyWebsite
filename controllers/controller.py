import json
from flask import render_template, request, redirect, session, jsonify, make_response
from reportlab.pdfgen import canvas
from flask_session import Session
import io, time

products = [{'id': 1,
             'name': 'Robo Dog',
             'image': 'toy1.png',
             'rating': 4, 
             'selling_price': 900,
             'marked_price': 1000,
             'status': 'For Sale'
             },{'id': 2,
             'name': 'Alza',
             'image': 'toy2.png',
             'rating': 5, 
             'selling_price': 1900,
             'marked_price': 2000,
             'status': 'For Sale'
             },{'id': 3,
             'name': 'Electric Toy Car',
             'image': 'toy3.png',
             'rating': 5, 
             'selling_price': 2900,
             'marked_price': 3000,
             'status': 'For Sale'
             },{'id': 4,
             'name': 'Lego house',
             'image': 'toy4.png',
             'rating': 4, 
             'selling_price': 500,
             'marked_price': 1000,
             'status': 'For Sale'
             },{'id': 5,
             'name': 'Toy car',
             'image': 'toy5.png',
             'rating': 4, 
             'selling_price': 900,
             'marked_price': 1000,
             'status': 'For Sale'
             },{'id': 6,
             'name': 'Plane',
             'image': 'toy6.png',
             'rating': 5, 
             'selling_price': 1900,
             'marked_price': 2000,
             'status': 'For Sale'
             },{'id': 7,
             'name': 'Crane',
             'image': 'toy7.png',
             'rating': 5, 
             'selling_price': 2900,
             'marked_price': 3000,
             'status': 'Not For Sale'
             },{'id': 8,
             'name': 'Truck',
             'image': 'toy8.png',
             'rating': 4, 
             'selling_price': 500,
             'marked_price': 1000,
             'status': 'Not For Sale'
             },
                
]

def index():
    print("incoming request")
    # Wait for 5 seconds
    time.sleep(5)
    if not session.get("user_id"):
        return redirect("/login")
        
    return render_template('dashboard/dashboard.html', products= products, user_id=session.get('user_id'))
    
def login():
    if request.method == "POST":
        session["user_id"] = request.form.get("email")
        print("Session name", request.form.get("email"))
        return redirect("/")
    return render_template("login/login.html")

def logout():
    session["user_id"] = None
    session["orders"] = None
    session["cart"] = None
    return redirect("/")

def order():
    productId = request.args.get('id')
    selectedProduct = None 
    for product in products:
        if product['id'] == int(productId):
            selectedProduct = product

    
    return render_template("order/order.html", product=selectedProduct)

def addAddress():
   return redirect("/")

def addToCart():
    data = request.json

    cart = session.get('cart', [])

    if( not cart):
        cart = []
        
    cart.append(data)

    session['cart'] = cart

    data = { 
            "message" : "Data Structures and Algorithms", 
        } 
    return jsonify(data) 

def cart():
    cart = session.get('cart', [])
    totalPrice = 0
    if (cart):
        totalPrice = sum(item['total'] for item in cart)

    
    return render_template("cart/cart.html", cart = cart, totalPrice = totalPrice)

def placeOrder():
    cart = session.get('cart', [])
    session['cart'] = []

    orders = session.get('orders', [])
    if(not orders):
        orders = []
    orders.append(cart)

    session['orders'] = orders
    
    print("placed order for ", cart)

    return redirect("/")

def profile():
    orders = session.get('orders', [])
    print("orders", orders)
    return render_template("profile/profile.html", orders = orders, user_id=session.get('user_id'))

def generateReceipt():
    print("########################Generating receipt#######################")
   
    data = request.json
    order_index = data['index']
    order_data = session.get('orders', [])

    if order_index < 0 or order_index >= len(order_data):
        raise ValueError("Invalid order index")

    selected_order = order_data[order_index]
    pdf_data = generatePdf(selected_order)
    response = make_response(pdf_data)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=receipt.pdf'

    return response


def generatePdf(order_data):
    pdf_buffer = io.BytesIO()
    pdf_canvas = canvas.Canvas(pdf_buffer)

    pdf_canvas.drawString(100, 800, f"Order Receipt")
    pdf_canvas.drawString(100, 780, f"------------------------")

    total_amount = 0  

    for index, order_item in enumerate(order_data, start=1):
        item_name = order_item.get('name', '')
        quantity = order_item.get('quantity', 0)
        price = order_item.get('price', 0)
        total = order_item.get('total', 0)

        pdf_canvas.drawString(
            100,
            780 - index * 20,
            f"Item {index}: {item_name}, Quantity: {quantity}, Price: {price}, Total: {total}"
        )

        total_amount += total

    
    pdf_canvas.drawString(100, 780, f"------------------------")
    pdf_canvas.drawString(100, 780 - (index + 1) * 20, f"Overall Total: {total_amount}")
    pdf_canvas.save()

    pdf_data = pdf_buffer.getvalue()
    pdf_buffer.close()

    return pdf_data
