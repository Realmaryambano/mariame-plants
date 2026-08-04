# 🌿 Mariamé Plants Ecosystem



An international-grade, full-stack e-commerce web application and botanical ecosystem management platform built with Flask. Designed for connoisseurs across Pakistan, it features curated tropical flora, proprietary bio-active organic soils, artisanal planters, dynamic cart management, and professional plant care consultations led by founder Maryam Bano.

## 🌐 Live Demo

Experience the project live: [View Live Demo]( https://mariaméplants.vercel.app)


---

## 📸 Screenshots

| Home Page / Hero Slider | Shop Catalog & Filters |
| :----------------: | :----------------: |
| ![Home Screenshot](/static/images/home-page.png) | ![Shop Screenshot](/static//images/shop.png) |

| Cart & Checkout Flow | PDF Invoice Generation |
| :----------------: | :----------------: |
| ![Checkout Screenshot](/static/images/cart.png) | ![Invoice Screenshot](/static/images/invoice.png) |

---

## 🚀 Features & Capabilities

* **Curated Botanical Catalog:** Features exclusive nursery stock including Monstera Deliciosa, Fiddle Leaf Fig, Snake Plant Laurentii, and ZZ Plant with ratings and instant cart actions.
* **Smart Categories & Filtering:** Seamless navigation for indoor plants, artisanal pottery, and nutrient-dense organic soils.
* **E-Commerce Shopping Cart:** Full session-based cart management with real-time calculations.
* **Automated Order Processing & Database:** Secure checkout saving customer orders and items directly into a SQLite database using SQLAlchemy.
* **Instant Email Notifications:** Integrated with the **Resend API** to instantly alert store management upon new customer orders or contact form submissions.
* **Automated PDF Invoices:** Built-in PDF generator utilizing **ReportLab** for professional customer billing.
* **Responsive UI/UX:** Dark-themed, elegant design reflecting upscale botanical standards across Karachi, Lahore, Islamabad, and beyond.

---

## 🛠️ Tech Stack & Dependencies

### **Backend Framework**
* **Python 3.x**
* **Flask** - Lightweight WSGI web application framework
* **Flask-SQLAlchemy** - ORM for database management and SQLite interface

### **APIs & Integrations**
* **Resend API (`resend`)** - Transactional email dispatch service for notifications

### **PDF Generation**
* **ReportLab (`reportlab`)** - Dynamic document generation for official store invoices

### **Frontend & Styling**
* **HTML5 / CSS3** - Custom styling with responsive layouts and hero sliders
* **Jinja2 Templates** - Server-side HTML rendering engine
* **FontAwesome** - Modern vector iconography

---

## ⚙️ Local Installation & Setup

Follow these steps to set up and run the project locally on your machine:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Realmaryambano/mariame-plants.git
   cd mariame-plants
   ```

2. **Create and Activate a Virtual Environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:** Create a `.env` file in the root directory and add your Resend API key:
   ```
   RESEND_API_KEY=your_resend_api_key_here
   ```

5. **Run the Application:**
   ```bash
   python app.py
   ```

   Open your browser and navigate to `http://127.0.0.1:5000`.

---

## 📦 Deployment

This application is structured for seamless deployment on cloud platforms like Vercel or Render:

* Configure `RESEND_API_KEY` in your hosting provider's environment variables dashboard.
* Ensure `.env` and local `.db` files are kept out of version control using `.gitignore`.

---

## 👩‍💻 Author & Contact

* **Founder & Lead Botanist:** Maryam Bano
* **Email:** maryambano.official@gmail.com
* **Phone / WhatsApp:** +92 333 2119480
* **LinkedIn:** [Realmaryambano](https://www.linkedin.com/in/realmaryambano)
* **GitHub Repository:** [Realmaryambano/mariame-plants](https://github.com/Realmaryambano/mariame-plants)

