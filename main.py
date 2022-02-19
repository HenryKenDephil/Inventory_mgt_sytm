from datetime import datetime
from optparse import Values
import os
import secrets
from flask import Flask,request, render_template, url_for, redirect, flash, session
import psycopg2 


app = Flask(__name__)
app.config['SECRET_KEY']='ee199f92ba624dd53f9fd27bdff4d210'

conn = psycopg2.connect("dbname='d4ahe615593c39' user='tjvfmqqynrzirk' host='ec2-18-215-8-186.compute-1.amazonaws.com' password='187e35f9a412a9b353837991fd918442ffb097a74b2e28dd6a6020fde20512c3' port='3229'")



@app.route('/inventories')
def products():
 cur = conn.cursor()
 cur.execute('select * from products')
 products = cur.fetchall()
 conn.commit()
 print("products",products)
 return render_template('inventories.html', x=products) 


@app.route('/edit_products', methods=["GET","POST"])
def edit_products():
    cur = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        serial_no = request.form['serial_no']
        bp = request.form['bp']
        sp=request.form['sp']
        id=request.form['id']
        
        query = ("UPDATE products SET name=%s, serial_no=%s, bp=%s, sp=%s WHERE id=%s")
        row = (name, serial_no, bp, sp, id)
        cur.execute(query,row)
        conn.commit()
        flash('product edited successfully')
        return redirect(url_for('products'))
    else:
        flash('Sorry, unsuccessful process', 'Try Again')
    

@app.route('/add_products', methods=["GET","POST"])
def add_products():
    cur=conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        serial_no = request.form['serial_no']
        bp = request.form['bp']
        sp=request.form['sp']
        
        
        query="INSERT INTO products (name, serial_no, bp, sp) Values(%s,%s,%s,%s)"
        row= (name, serial_no,  bp, sp)
        cur.execute(query,row)
        conn.commit()
        flash('products Updated Successfully')
        return redirect(url_for('products'))
    else:
        flash('something went wrong', 'Try Again!')
  
@app.route('/')
def home():
  return render_template('home.html')  

@app.route('/sales') 
def sales():
    cur =conn.cursor()
    # cur.execute('SELECT * FROM sales')
    cur.execute('SELECT  p.name, sum(s.quantity) as q ,sum((p.sp-p.bp)*s.quantity) as totalprofit FROM public.products as p join sales as s on p.id=s.productid GROUP BY name;')
    sales = cur.fetchall()
    print(sales)
    return render_template('sales.html', y=sales)


@app.route('/sales/<int:id>')
def view_sales(id):
 cur = conn.cursor()
#  cur.execute('SELECT  p.name, sum(s.quantity) as q ,sum((p.sp-p.bp)*s.quantity) as totalprofit FROM public.products as p join sales as s on p.id=s.productid WHERE id=%s;')
 cur.execute('SELECT * FROM sales WHERE id=%s',[id])
 sales = cur.fetchall()
 print(sales)
 return render_template('sales.html', y=sales)


@app.route('/makesales', methods=["GET", "POST"])
def makesales():
    cur = conn.cursor()
    if request.method == 'POST':
        id= request.form['productid']
        quantity = request.form['quantity']
        created_at=datetime.now()
         
        query = "INSERT INTO sales (productid, quantity, created_at) VALUES (%s, %s, %s)"
        row = (id,quantity, created_at)
        cur.execute(query,row)
        conn.commit()
        flash('sales Added successfully')
        return redirect(url_for('products'))
    # else:
    #     flash('Sorry, unsuccessful process', 'Try Again')
    
@app.route('/stock') 
def stock():
    cur =conn.cursor()
    cur.execute('SELECT * FROM products')
    # cur.execute('SELECT  p.name, sum(s.quantity) as q ,sum((p.sp-p.bp)*s.quantity) as totalprofit FROM public.products as p join sales as s on p.id=s.productid GROUP BY name;')
    stock = cur.fetchall()
    print(stock)
    return render_template('stock.html', z=stock)


@app.route('/dashboard')
def dashboard():
  cur = conn.cursor()
  cur.execute ("SELECT extract(year from s.created_at) || '-' || extract(month from created_at) || '-' || EXTRACT (DAY FROM s.created_at) as siku,sum((p.sp-p.bp)*s.quantity) as totalprofit FROM public.products as p join sales as s on p.id=s.productid GROUP BY s.created_at;")
  dashboard = cur.fetchall()
  print(dashboard)
  labels=[]
  data=[]
  for i in dashboard:
      labels.append(i[0])
      data.append(int(i[1]))
  print(labels)
  print(data)
  return render_template('dashboard.html', labels=labels, data=data)
if __name__ == '__main__':
    app.run(debug=True)

