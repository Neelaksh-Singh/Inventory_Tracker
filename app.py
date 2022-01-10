from flask import Flask,render_template,url_for,redirect,flash,request
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import csv,os
from forms import addproduct,editproduct
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
app.secret_key = "redhat"
app.permanent_session_lifetime = timedelta(minutes=5)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
global ct
ct=0

class Product(db.Model):
    prod_id = db.Column(db.Integer, primary_key= True)
    prod_name = db.Column(db.String(20), nullable = False)
    prod_name = db.Column(db.String(20),unique = True ,nullable = False)
    prod_qty = db.Column(db.Integer, nullable = False)
    prod_price = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f"Product('{self.prod_id}','{self.prod_name}','{self.prod_qty}','{self.prod_price}')"



@app.route("/", methods = ['GET','POST'])
def product():
    form = addproduct()
    eform = editproduct()
    details = Product.query.all()
    exists = bool(Product.query.all())
    if exists== False and request.method == 'GET' :
            flash(f'Add products to view','info')
    elif eform.validate_on_submit() and request.method == 'POST':

        p_id = request.form.get("productid","")
        pname = request.form.get("productname","")
        details = Product.query.all()
        prod = Product.query.filter_by(prod_id = p_id).first()
        prod.prod_name = eform.editname.data
        prod.prod_qty= eform.editqty.data
        prod.prod_price = eform.editprice.data
        # Balance.query.filter_by(product=pname).update(dict(product=eform.editname.data))
        
        try:
            db.session.commit()
            flash(f'Your product  has been updated!', 'success')
            return redirect('/')
        except IntegrityError :
            db.session.rollback()
            flash(f'This product already exists','danger')
            return redirect('/')
        return render_template('prod.html',title = 'Products',details=details,eform=eform)

    elif form.validate_on_submit() :
        product = Product(prod_name=form.prodname.data,prod_qty=form.prodqty.data,prod_price=form.prodprice.data)
        db.session.add(product)
        try:
            db.session.commit()
            flash(f'Your product {form.prodname.data} has been added!', 'success')
            return redirect(url_for('product'))
        except IntegrityError :
            db.session.rollback()
            flash(f'This product already exists','danger')
            return redirect('/')
    return render_template('prod.html',title = 'Products',eform=eform,form = form,details=details)

@app.route("/delete")
def delete():
    type = request.args.get('type')
    if type == 'product':
        pid = request.args.get('p_id')
        product = Product.query.filter_by(prod_id=pid).delete()
        db.session.commit()
        flash(f'Your product  has been deleted!', 'success')
        return redirect(url_for('product'))
        return render_template('prod.html',title = 'Products')
    

ct=0
@app.route('/download')
def to_csv ():
    if bool(Product.query.all()) == False:
        flash(f'No product is present','danger')
        return redirect('/')
    else:

        global ct
        path = os.getcwd()+"\Generated_CSV"
        filepath = ("Updated-Inventory"+str(ct)+".csv") if ct !=0 else ("Updated-Inventory.csv")
        path = os.path.join(path,filepath)
        with open(path, 'w') as csvfile:
            details = db.session.query(Product.prod_id,Product.prod_name,Product.prod_qty,Product.prod_price)
            # writer = csv.DictWriter(csvfile, fieldnames=['id', 'Prod_Name', 'Prod_Quantity', 'Prod_Price'])
            # writer.writeheader()
            for row in details:
                csv_out = csv.writer(csvfile)
                csv_out.writerow(row)
        # return send_file(path, as_attachment=True)
        ct+=1
        flash(f'Your Product has now been exported to {path}!', 'success')
        return redirect('/')

db.create_all()
db.session.commit()

if __name__ == "__main__":
    app.run(port=80,debug=True)