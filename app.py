from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import os

app = Flask(__name__)
app.secret_key = 'mariame_plants_international_secret_key'

# Configure SQLite Database File Locally
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'mariame_plants.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model for Orders
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    soil_weight = db.Column(db.String(50), nullable=True)
    address = db.Column(db.Text, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    delivery_fee = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

# 28 International-Grade Plant, Soil, and Decor Products
PRODUCTS = [
    {
        "id": 1, "name": "Monstera Deliciosa", "category": "indoor", 
        "badge": "Bestseller", "price": 4500, "rating": 4.9, 
        "desc": "Famous Swiss Cheese plant known for natural leaf splits and tropical presence.",
        "image": "Monstera_Deliciosa.png"
    },
    {
        "id": 2, "name": "Fiddle Leaf Fig (Ficus lyrata)", "category": "indoor", 
        "badge": "Trending", "price": 6800, "rating": 4.8, 
        "desc": "Architectural statement plant with broad, violin-shaped glossy dark green leaves.",
        "image": "fiddle.png"
    },
    {
        "id": 3, "name": "Snake Plant Laurentii", "category": "indoor", 
        "badge": "Hardy", "price": 2800, "rating": 4.7, 
        "desc": "Nearly indestructible air-purifying plant featuring striking yellow-bordered stiff leaves.",
        "image": "snake.png"
    },
    {
        "id": 4, "name": "ZZ Plant (Zamioculcas zamiifolia)", "category": "indoor", 
        "badge": "Low Light", "price": 3200, "rating": 4.9, 
        "desc": "Glossy, emerald-green stems that thrive gracefully in dimly lit office or room spaces.",
        "image": "zz_plant.png"
    },
    {
        "id": 5, "name": "Peace Lily (Spathiphyllum)", "category": "indoor", 
        "badge": "Air Purifier", "price": 2500, "rating": 4.6, 
        "desc": "Elegant dark foliage paired with striking white spathe blooms that clean indoor air.",
        "image": "peace-lily.png"   
    },
    {
        "id": 6, "name": "Areca Palm (Dypsis lutescens)", "category": "outdoor", 
        "badge": "Tropical", "price": 5200, "rating": 4.8, 
        "desc": "Feathery, graceful fronds that introduce an instant resort-like ambiance to patios.",
        "image": "areca-palm.png"
    },
    {
        "id": 7, "name": "Bougainvillea Bonsai Specimen", "category": "outdoor", 
        "badge": "Vibrant", "price": 4100, "rating": 4.7, 
        "desc": "Sun-loving outdoor flowering shrub featuring vibrant magenta bracts and strong woody trunk.",
        "image": "bougainvillea.png"
    },
    {
        "id": 8, "name": "Sago Palm (Cycas revoluta)", "category": "outdoor", 
        "badge": "Classic", "price": 7500, "rating": 4.9, 
        "desc": "Stately architectural cycad with stiff, dark green glossy fronds resistant to heat.",
        "image": "sago-palm.png"
    },
    {
        "id": 9, "name": "Jasmine (Jasminum sambac)", "category": "outdoor", 
        "badge": "Fragrant", "price": 1800, "rating": 4.8, 
        "desc": "Beloved traditional climber producing intensely sweet nocturnal aromatic white blossoms.",
        "image": "jasmine.png"
    },
    {
        "id": 10, "name": "Hibiscus Rosa-Sinensis", "category": "outdoor", 
        "badge": "Exotic", "price": 2200, "rating": 4.5, 
        "desc": "Dazzling tropical blooms with deep red ruffled petals that thrive under full sunlight.",
        "image": "Hibiscus Rosa-Sinensis.png"
    },
    {
        "id": 11, "name": "Golden Barrel Cactus", "category": "cactus", 
        "badge": "Popular", "price": 3000, "rating": 4.7, 
        "desc": "Symmetrical globe-shaped succulent cactus adorned with striking golden-yellow spines.",
        "image": "Golden Barrel Cactus.png"
    },
    {
        "id": 12, "name": "Echeveria Elegans Rosette", "category": "cactus", 
        "badge": "Cute", "price": 1200, "rating": 4.8, 
        "desc": "Tightly formed succulent rosettes displaying pale blue-green fleshy leaves.",
        "image": "Echeveria Elegans Rosette.png"
    },
    {
        "id": 13, "name": "Aloe Vera Medicinal", "category": "cactus", 
        "badge": "Useful", "price": 1500, "rating": 4.9, 
        "desc": "Functional succulent with thick gel-filled leaves famous for soothing skin care properties.",
        "image": "Aloe Vera Medicinal.png"
    },
    {
        "id": 14, "name": "Haworthia Zebra Succulent", "category": "cactus", 
        "badge": "Mini", "price": 1100, "rating": 4.6, 
        "desc": "Compact dark green succulent featuring distinct horizontal white bumpy zebra stripes.",
        "image": "Haworthia Zebra Succulent.png"
    },
    {
        "id": 15, "name": "Pachycereus Candelabra Cactus", "category": "cactus", 
        "badge": "Statement", "price": 5500, "rating": 4.9, 
        "desc": "Tall branching architectural desert column specimen for high-end interior styling.",
        "image": "Pachycereus Candelabra Cactus.png"
    },
    {
        "id": 16, "name": "Ficus Retusa Bonsai", "category": "bonsai", 
        "badge": "Masterpiece", "price": 9500, "rating": 5.0, 
        "desc": "Aged trunk structure with aerial roots and deep green canopy, expertly trained."
    },
    {
        "id": 17, "name": "Chinese Elm Bonsai", "category": "bonsai", 
        "badge": "Artisanal", "price": 8800, "rating": 4.8, 
        "desc": "Classic indoor-tolerant bonsai featuring fine twig branching and small textured leaves."
    },
    {
        "id": 18, "name": "Carmona Microphylla (Fujian Tea)", "category": "bonsai", 
        "badge": "Exquisite", "price": 10500, "rating": 4.9, 
        "desc": "Stunning oriental bonsai bearing glossy dark leaves and tiny white star flowers."
    },
    {
        "id": 19, "name": "Juniper Procumbens Nana", "category": "bonsai", 
        "badge": "Classic", "price": 7200, "rating": 4.7, 
        "desc": "Evergreen needle-form conifer styled in traditional cascade and slanting aesthetics."
    },
    {
        "id": 20, "name": "Mariamé Premium Aroid Soil Mix (5kg)", "category": "soil", 
        "badge": "Best Grade", "price": 1600, "rating": 5.0, 
        "desc": "Custom coarse blend of chunky orchid bark, perlite, horticultural charcoal, and organic peat."
    },
    {
        "id": 21, "name": "Cactus & Succulent Grit Blend (3kg)", "category": "soil", 
        "badge": "Fast Draining", "price": 1200, "rating": 4.8, 
        "desc": "Mineral-heavy fast draining substrate formula engineered to completely prevent root rot."
    },
    {
        "id": 22, "name": "Nutrient-Dense Organic Worm Castings", "category": "soil", 
        "badge": "Bio-Active", "price": 950, "rating": 4.9, 
        "desc": "Pure organic earthworm compost loaded with beneficial microbes and natural plant growth hormones."
    },
    {
        "id": 23, "name": "Expanded Perlite & Pumice Aeration Pack", "category": "soil", 
        "badge": "Essential", "price": 850, "rating": 4.7, 
        "desc": "Lightweight volcanic rock additives designed to maximize oxygen flow inside heavy soils."
    },
    {
        "id": 24, "name": "Handmade Terracotta Cylinder Pot", "category": "pots", 
        "badge": "Handmade", "price": 1800, "rating": 4.8, 
        "desc": "Breathable classic terracotta clay vessel featuring a matching bottom drainage saucer."
    },
    {
        "id": 25, "name": "Minimalist Matte Ceramic Planter", "category": "pots", 
        "badge": "Modern", "price": 2400, "rating": 4.9, 
        "desc": "Sleek contemporary ceramic pot finished with a luxury soft-touch matte protective coating."
    },
    {
        "id": 26, "name": "Woven Natural Seagrass Basket Pot", "category": "pots", 
        "badge": "Boho Style", "price": 2100, "rating": 4.7, 
        "desc": "Hand-woven organic seagrass basket equipped with a protective inner plastic moisture liner."
    },
    {
        "id": 27, "name": "Nordic Concrete Textured Cachepot", "category": "pots", 
        "badge": "Industrial", "price": 2900, "rating": 4.8, 
        "desc": "Heavy-duty urban architectural grey concrete planter tailored for statement corners."
    },
    {
        "id": 28, "name": "Glazed Japanese Bonsai Training Tray", "category": "pots", 
        "badge": "Specialty", "price": 3500, "rating": 4.9, 
        "desc": "Overtly shallow oval ceramic dish finished in deep emerald celadon glaze with drainage mesh."
    }
]

DELIVERY_FEE = 350

@app.context_processor
def inject_cart_count():
    cart = session.get('cart', {})
    total_count = sum(cart.values()) if isinstance(cart, dict) else 0
    return dict(cart_count=total_count)

@app.route('/')
def home():
    featured = PRODUCTS[:4]
    return render_template('index.html', products=featured)

@app.route('/shop')
def shop():
    category = request.args.get('category', 'all')
    sort_by = request.args.get('sort', 'default')
    search_query = request.args.get('q', '').strip().lower()
    
    if category == 'all':
        filtered_products = PRODUCTS
    else:
        filtered_products = [p for p in PRODUCTS if p['category'] == category]
        
    if search_query:
        filtered_products = [
            p for p in filtered_products 
            if search_query in p['name'].lower() or search_query in p['desc'].lower()
        ]
        
    if sort_by == 'price_low':
        filtered_products = sorted(filtered_products, key=lambda x: x['price'])
    elif sort_by == 'price_high':
        filtered_products = sorted(filtered_products, key=lambda x: x['price'], reverse=True)
    elif sort_by == 'name':
        filtered_products = sorted(filtered_products, key=lambda x: x['name'])
        
    return render_template('shop.html', products=filtered_products, current_cat=category, current_sort=sort_by)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/cart')
def cart():
    cart_items = session.get('cart', {})
    detailed_cart = []
    subtotal_price = 0
    
    for product_id_str, quantity in cart_items.items():
        try:
            product_id = int(product_id_str)
            product = next((p for p in PRODUCTS if p['id'] == product_id), None)
            if product:
                subtotal = product['price'] * quantity
                subtotal_price += subtotal
                detailed_cart.append({
                    'product': product,
                    'quantity': quantity,
                    'subtotal': subtotal
                })
        except ValueError:
            continue
            
    delivery_fee = DELIVERY_FEE if detailed_cart else 0
    total_price = subtotal_price + delivery_fee
    return render_template('cart.html', cart=detailed_cart, subtotal=subtotal_price, delivery_fee=delivery_fee, total=total_price)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    str_id = str(product_id)
    
    if str_id in cart:
        cart[str_id] += 1
    else:
        cart[str_id] = 1
        
    session['cart'] = cart
    session.modified = True
    
    flash('Item successfully added to your living ecosystem cart!', 'success')
    return redirect(request.referrer or url_for('shop'))

@app.route('/update-cart/<int:product_id>/<action>', methods=['POST'])
def update_cart(product_id, action):
    cart = session.get('cart', {})
    str_id = str(product_id)
    
    if str_id in cart:
        if action == 'increase':
            cart[str_id] += 1
        elif action == 'decrease':
            cart[str_id] -= 1
            if cart[str_id] <= 0:
                del cart[str_id]
                
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    flash('Cart has been cleared.', 'info')
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_items = session.get('cart', {})
    
    if not cart_items:
        flash('Your cart is empty. Add items before checking out.', 'warning')
        return redirect(url_for('shop'))
        
    detailed_cart = []
    subtotal_price = 0
    
    for product_id_str, quantity in cart_items.items():
        try:
            product_id = int(product_id_str)
            product = next((p for p in PRODUCTS if p['id'] == product_id), None)
            if product:
                subtotal = product['price'] * quantity
                subtotal_price += subtotal
                detailed_cart.append({
                    'product': product,
                    'quantity': quantity,
                    'subtotal': subtotal
                })
        except ValueError:
            continue
            
    delivery_fee = DELIVERY_FEE
    total_price = subtotal_price + delivery_fee
            
    if request.method == 'POST':
        new_order = Order(
            name=request.form.get('name'),
            phone=request.form.get('phone'),
            city=request.form.get('city'),
            soil_weight=request.form.get('soil_weight'),
            address=request.form.get('address'),
            subtotal=subtotal_price,
            delivery_fee=delivery_fee,
            total=total_price
        )
        db.session.add(new_order)
        db.session.commit()

        for item in detailed_cart:
            order_item = OrderItem(
                order_id=new_order.id,
                product_name=item['product']['name'],
                quantity=item['quantity'],
                price=item['product']['price'],
                subtotal=item['subtotal']
            )
            db.session.add(order_item)
        db.session.commit()

        session['last_order_id'] = new_order.id
        session.pop('cart', None)
        return redirect(url_for('order_success'))
        
    return render_template('checkout.html', cart_items=detailed_cart, subtotal=subtotal_price, delivery_fee=delivery_fee, total_price=total_price)

@app.route('/order-success')
def order_success():
    order_id = session.get('last_order_id')
    if not order_id:
        return redirect(url_for('home'))
    order = Order.query.get(order_id)
    if not order:
        return redirect(url_for('home'))
    return render_template('order_success.html', order=order)

@app.route('/download-invoice-pdf')
def download_invoice_pdf():
    order_id = session.get('last_order_id')
    if not order_id:
        return redirect(url_for('home'))
    order = Order.query.get(order_id)
    if not order:
        return redirect(url_for('home'))
        
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'InvoiceTitle', parent=styles['Heading1'], fontSize=20, textColor=colors.HexColor('#2c3e50'), spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        'InvoiceSubtitle', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#7f8c8d'), spaceAfter=15
    )
    normal_style = ParagraphStyle(
        'NormalText', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#333333')
    )

    elements = []
    elements.append(Paragraph(f"Mariamé Plants - Official Invoice #{order.id}", title_style))
    elements.append(Paragraph("Botanical Ecosystem Specimen Delivery Order", subtitle_style))
    
    customer_info = [
        [Paragraph(f"<b>Customer Name:</b> {order.name}", normal_style), Paragraph(f"<b>City:</b> {order.city}", normal_style)],
        [Paragraph(f"<b>Phone:</b> {order.phone}", normal_style), Paragraph(f"<b>Package:</b> {order.soil_weight}", normal_style)],
        [Paragraph(f"<b>Delivery Address:</b> {order.address}", normal_style), ""]
    ]
    t_cust = Table(customer_info, colWidths=[270, 270])
    t_cust.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 6)]))
    elements.append(t_cust)
    elements.append(Spacer(1, 15))
    
    table_data = [["Product / Specimen", "Qty", "Price", "Subtotal"]]
    for item in order.items:
        table_data.append([
            Paragraph(item.product_name, normal_style),
            str(item.quantity),
            f"PKR {item.price}",
            f"PKR {item.subtotal}"
        ])
        
    table_data.append(["", "", "Subtotal:", f"PKR {order.subtotal}"])
    table_data.append(["", "", "Delivery Fee:", f"PKR {order.delivery_fee}"])
    table_data.append(["", "", "Total Amount:", f"PKR {order.total}"])
    
    t_items = Table(table_data, colWidths=[260, 60, 110, 110])
    t_items.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2d5a27')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -4), 0.5, colors.HexColor('#dcdde1')),
        ('BACKGROUND', (2, -3), (-1, -1), colors.HexColor('#f5f6fa')),
        ('FONTNAME', (2, -1), (-1, -1), 'Helvetica-Bold'),
        ('TOPPADDING', (0, -3), (-1, -1), 6),
        ('BOTTOMPADDING', (0, -3), (-1, -1), 6),
    ]))
    
    elements.append(t_items)
    doc.build(elements)
    
    buffer.seek(0)
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f"attachment; filename=Mariame_Invoice_{order.name.replace(' ', '_')}.pdf"
    return response

import resend

# Set up your Resend API key
resend.api_key = "abc"

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        try:
            # Send the email via Resend API
            params = {
                "from": "Mariamé Plants <onboarding@resend.dev>",
                "to": ["maryambano.official@gmail.com"],
                "subject": f"New Contact Message from {name}",
                "html": f"""
                    <h3>New Customer Message</h3>
                    <p><b>Name:</b> {name}</p>
                    <p><b>Email:</b> {email}</p>
                    <p><b>Message:</b></p>
                    <p>{message}</p>
                """
            }
            resend.Emails.send(params)
            flash('Thank you for reaching out! Your message has been sent successfully.', 'success')
        except Exception as e:
            flash('An error occurred while sending your message. Please try again later.', 'danger')
            
        return redirect(url_for('contact'))
        
    return render_template('contact.html')

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)