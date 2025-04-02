import mysql.connector as con
from datetime import datetime
import random
from flask import Flask, session, url_for, redirect, render_template

app=Flask(__name__)


def system_config():
	re={"waiter_id":"1","centers_id":"1","current_date": str(datetime.now().strftime("%Y-%M-%d")), "current_time": str(datetime.now().strftime("%H: %m: %S"))}

	return re


def connectDB():
	host="localhost"
	database="flask_pos"
	dbuser="root"
	dbpass=""
	datas={"host":host,"database":database,"user":dbuser,"password":dbpass,"raise_on_warnings":True}

	return datas


def create_grn(supplier_id,grn_no,comments,total_amount=0,total_items=0): #once pending approve is removed the items of grn are auto populated to the system with their repective status
	cd=connectDB()
	conn=con.connect(**cd)
	sc=system_config()
	date=sc['current_date']
	time=sc['current_time']
	centers_id=sc['centers_id']
	waiter_id=sc['waiter_id']
	q="insert into grn(supplier_id,grn_no,centers_id,waiter_id,date,trans_time,total_amount,total_items,comments) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	cur=conn.cursor()
	cur.execute(q,(supplier_id,grn_no,centers_id,waiter_id,date,time,total_amount,total_items,comments))
	conn.commit()
	grn_id=cur.lastrowid
	cur.close()
	conn.close()
	return grn_id

def get_grn_status(grn_id):
	q="select status from grn where grn_id=%s"
	cd=connectDB()
	conn=con.connect(**cd)
	cur=conn.cursor()
	cur.execute(q,(grn_id,))
	data=cur.fetchone()
	cur.close()
	conn.close()
	status="pending";
	if len(data) >0:
		status=data[0]
	return status

def get_grn_items_by_grn_id(grn_id,centers_id):
	q="select * from goods_received where centers_id=%s and grn_id=%s"
	cd=connectDB()
	conn=con.connect(**cd)
	sc=system_config()
	cur=conn.cursor(dictionary=True)
	cur.execute(q,(centers_id,grn_id))
	results=cur.fetchall()
	cur.close()
	conn.close()
	return results

def get_grn_items_by_grn_no(grn_no,centers_id):
	q="select * from goods_received where centers_id=%s grn_no=%s"
	cd=connectDB()
	conn=con.connect(**cd)
	sc=system_config()
	cur=conn.cursor(dictionary=True)
	cur.execute(q,(centers_id,grn_no))
	results=cur.fetchall()
	cur.close()
	conn.close()
	return results

def get_grn_total(grn_id):
	q="select SUM(total_cost) as grn_total from goods_received where grn_id=%s"
	cd=connectDB()
	conn=con.connect(**cd)
	cur=conn.cursor()
	cur.execute(q,(grn_id,))
	data=cur.fetchone()
	cur.close()
	conn.close()
	bt=0;
	if len(data) >0:
		bt=data[0]
	return bt

def set_grn_total(grn_id):
	q="update bill set total_cost=%s where grn_id=%s"
	total_amount=get_grn_total(grn_id)
	cd=connectDB()
	conn=con.connect(**cd)
	cur=conn.cursor()
	cur.execute(q,(total_amount,grn_id))
	conn.commit()
	cur.close()
	conn.close()
	return grn_id

def approve_grn_item(grn_id,goods_received_id):
	q="update goods_received set status=%s, grn_status=%s where grn_id=%s and goods_received_id=%s"
	grn_status=status="approved"
	total_amount=get_grn_total(grn_id)
	cd=connectDB()
	conn=con.connect(**cd)
	cur=conn.cursor()
	cur.execute(q,(status,grn_id,goods_received_id,grn_status))
	conn.commit()
	cur.close()
	conn.close()
	return "ok"

def approve_grn(grn_id,centers_id):
	q="update grn set status=%s where grn_id=%s and centers_id=%s"
	status="approved"
	total_amount=get_grn_total(grn_id)
	cd=connectDB()
	conn=con.connect(**cd)
	cur=conn.cursor()
	cur.execute(q,(status,grn_id,centers_id))
	conn.commit()
	cur.close()
	conn.close()
	#populate the goods received into actual working stock:
	items=get_grn_items_by_grn_id(grn_id,centers_id)
	for item in items:
		item_exist=if_item_exists(item['name'],centers_id)
		if item_exist:
			#update stock info
			name=item["name"]
			goods_received_id=item["goods_received_id"]
			standard_quantity=item["actual_units_received"]
			actual_units_in_stock=item["actual_units_received"]
			cost_price_per_unit=item["cost_price_per_unit"]
			selling_price_per_unit=item["selling_price_per_unit"]
			discount_in_percentage=item["discount_in_percentage"]
			reorder_level=item["reorder_level"]
			date_updated=item["date_updated"]
			visibility="show"
			item_source_id=item["item_source_id"]
			photo=item["photo"]
			supplier_id=item["supplier_id"]
			status=item["status"]
			total_cost=item["total_cost"]
			update_item_in_stock(name,supplier_id,actual_units_in_stock,reorder_level,centers_id)
			#set status to approved
			approve_grn_item(grn_id,goods_received_id)
		else:
			#add as new item
			name=item["name"]
			goods_received_id=item["goods_received_id"]
			standard_quantity=item["actual_units_received"]
			actual_units_in_stock=item["actual_units_received"]
			cost_price_per_unit=item["cost_price_per_unit"]
			selling_price_per_unit=item["selling_price_per_unit"]
			discount_in_percentage=item["discount_in_percentage"]
			reorder_level=item["reorder_level"]
			date_updated=item["date_updated"]
			visibility="show"
			item_source_id=item["item_source_id"]
			photo=item["photo"]
			supplier_id=item["supplier_id"]
			status=item["status"]
			total_cost=item["total_cost"]
			create_item(name,standard_quantity,actual_units_in_stock,cost_price_per_unit,selling_price_per_unit,discount_in_percentage,reorder_level,date_updated,centers_id,visibility,item_source_id,photo,supplier_id,status)
			#set status to approved
			approve_grn_item(grn_id,goods_received_id)
	return "items moved to actual stock"

def approve_grn_items(grn_id,goods_received_id):
	q="update goods_received set status=%s where grn_id=%s and goods_received_id=%s"
	status="received"
	total_amount=get_grn_total(grn_id)
	cd=connectDB()
	conn=con.connect(**cd)
	cur=conn.cursor()
	cur.execute(q,(status,grn_id,goods_received_id))
	conn.commit()
	cur.close()
	conn.close()
	return grn_id

def delete_grn_item(goods_received_id,grn_id):
	q="delete from goods_received where goods_received_id=%s and grn_id=%s"
	cd=connectDB()
	conn=con.connect(**cd)
	cur=conn.cursor()
	cur.execute(q,(goods_received_id,grn_id))
	conn.commit()
	cur.close()
	conn.close()
	set_grn_total(grn_id)
	return "ok"

def create_grn_items(grn_id,name,standard_quantity,actual_units_received,cost_price_per_unit,selling_price_per_unit,discount_in_percentage,reorder_level,date_updated,centers_id,visibility,item_source_id,photo,supplier_id,status,total_cost): #once pending approve is removed the items of grn are auto populated to the system with their repective status
	cd=connectDB()
	conn=con.connect(**cd)
	sc=system_config()
	date=sc['current_date']
	time=sc['current_time']
	centers_id=sc['centers_id']
	waiter_id=sc['waiter_id']
	total_cost=actual_units_received*cost_price_per_unit
	grn_status=get_grn_status(grn_id)
	q="insert into goods_received(grn_status,grn_id,name,standard_quantity,actual_units_in_stock,cost_price_per_unit,selling_price_per_unit,discount_in_percentage,reorder_level,date_updated,centers_id,visibility,item_source_id,photo,supplier_id,status,total_cost) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	cur=conn.cursor()
	cur.execute(q,(grn_status,grn_id,name,standard_quantity,actual_units_in_stock,cost_price_per_unit,selling_price_per_unit,discount_in_percentage,reorder_level,date_updated,centers_id,visibility,item_source_id,photo,supplier_id,status,total_cost))
	conn.commit()
	goods_received_id=cur.lastrowid
	cur.close()
	conn.close()
	set_grn_total(grn_id)
	return goods_received_id

def get_bill_total(bill_id):
	q="select SUM(total_amount) as bill_total from sale where bill_id=%s"
	cd=connectDB()
	conn=con.connect(**cd)
	cur=conn.cursor()
	cur.execute(q,(bill_id,))
	data=cur.fetchone()
	cur.close()
	conn.close()
	bt=0;
	if len(data) >0:
		bt=data[0]
	return bt

def set_bill_total(bill_id):
	q="update bill set total_amount=%s where bill_id=%s"
	total_amount=get_bill_total(bill_id)
	cd=connectDB()
	conn=con.connect(**cd)
	cur=conn.cursor()
	cur.execute(q,(total_amount,bill_id))
	conn.commit()
	cur.close()
	conn.close()
	return bill_id

def set_bill_sale_status(bill_id,sale_id,status="sold"):
	q="update sale set status=%s where bill_id=%s and sale_id=%s"
	cd=connectDB()
	conn=con.connect(**cd)
	cur=conn.cursor()
	cur.execute(q,(status,bill_id,sale_id))
	conn.commit()
	cur.close()
	conn.close()
	return bill_id

def post_bill(bill_id):
	q="update bill set status=%s where bill_id=%s"
	status="posted"
	total_amount=get_bill_total(bill_id)
	cd=connectDB()
	conn=con.connect(**cd)
	cur=conn.cursor()
	cur.execute(q,(status,bill_id))
	conn.commit()
	cur.close()
	conn.close()
	sc=system_config()
	date=sc['current_date']
	trans_time=sc['current_time']
	centers_id=sc['centers_id']
	waiter_id=sc['waiter_id']
	bitems=single_bill_items(centers_id,bill_id)
	for item in bitems:
		#nus the stock
		current_requested_quantity=get_current_sale_quantity(item['sale_id'])
		reduce_item_in_stock(item['item_id'],current_requested_quantity,centers_id)
		#update the sale to sold status
		set_bill_sale_status(bill_id,item['sale_id'])
	return "ok"



def create_new_bill(bill_type="New"):
	cd=connectDB()
	conn=con.connect(**cd)
	bill_number=str(datetime.now().strftime("%y%M%d%H%m%S"))+"_"+str(random.randint(0,99));
	sc=system_config()
	date=sc['current_date']
	trans_time=sc['current_time']
	centers_id=sc['centers_id']
	waiter_id=sc['waiter_id']
	
	total_amount=0;
	created_date=str(datetime.now().strftime("%Y-%M-%d"))
	q="insert into bill(created_date,bill_number,total_amount,date,trans_time,centers_id,waiter_id,bill_type) values(%s,%s,%s,%s,%s,%s,%s,%s)"
	cur=conn.cursor()
	cur.execute(q,(created_date,bill_number,total_amount,date,trans_time,centers_id,waiter_id,bill_type))
	conn.commit()
	bill_id=cur.lastrowid
	cur.close()
	conn.close()
	return bill_id

def single_bill_items(centers_id,bill_id):
	q="select * from sale where centers_id=%s and bill_id=%s"
	cd=connectDB()
	conn=con.connect(**cd)
	sc=system_config()
	cur=conn.cursor(dictionary=True)
	cur.execute(q,(centers_id,bill_id))
	results=cur.fetchall()
	cur.close()
	conn.close()
	return results

def show_items(centers_id,item_source_id,status="for sale",visibility="show"):
	q="select * from item where centers_id=%s and item_source_id=%s and visibility=%s and status=%s"
	cd=connectDB()
	conn=con.connect(**cd)
	sc=system_config()
	cur=conn.cursor(dictionary=True)
	cur.execute(q,(centers_id,item_source_id,visibility,status))
	results=cur.fetchall()
	cur.close()
	conn.close()
	return results

def if_item_exists(name,centers_id,visibility="show"):
	q="select * from item where name=%s and centers_id=%s and visibility=%s"
	cd=connectDB()
	conn=con.connect(**cd)
	sc=system_config()
	cur=conn.cursor(dictionary=True)
	cur.execute(q,(name,centers_id,visibility))
	data=cur.fetchall()
	cur.close()
	conn.close()
	if len(data) >0:
		return True
	else:
		return False

def create_item(name,standard_quantity,actual_units_in_stock,cost_price_per_unit,selling_price_per_unit,discount_in_percentage,reorder_level,date_updated,centers_id,visibility,item_source_id,photo,supplier_id,status="for sale"):
	q='insert into item(name,standard_quantity,actual_units_in_stock,cost_price_per_unit,selling_price_per_unit,discount_in_percentage,reorder_level,date_updated,centers_id,visibility,item_source_id,photo,supplier_id,status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
	cd=connectDB()
	conn=con.connect(**cd)
	sc=system_config()
	date=sc['current_date']
	time=sc['current_time']
	centers_id=sc['centers_id']
	waiter_id=sc['waiter_id']
	cur=conn.cursor()
	cur.execute(q,(name,standard_quantity,actual_units_in_stock,cost_price_per_unit,selling_price_per_unit,discount_in_percentage,reorder_level,date_updated,centers_id,visibility,item_source_id,photo,supplier_id,status))
	conn.commit()
	bill_id=cur.lastrowid
	cur.close()
	conn.close()
	return bill_id

def get_item_stock_count(name,centers_id):
	actual_units_in_stock="0"
	q="select actual_units_in_stock from item where name=%s and centers_id=%s"
	cd=connectDB()
	conn=con.connect(**cd)
	sc=system_config()
	cur=conn.cursor()
	cur.execute(q,(name,centers_id))
	data=cur.fetchone()
	cur.close()
	conn.close()
	if len(data) >0:
		actual_units_in_stock=data[0]
	return actual_units_in_stock

def get_item_stock_count_by_item_id(item_id,centers_id):
	actual_units_in_stock="0"
	q="select actual_units_in_stock from item where item_id=%s and centers_id=%s"
	cd=connectDB()
	conn=con.connect(**cd)
	sc=system_config()
	cur=conn.cursor(dictionary=True)
	cur.execute(q,(item_id,centers_id))
	data=cur.fetchall()
	cur.close()
	conn.close()
	if len(data) >0:
		actual_units_in_stock=data[0]['actual_units_in_stock']
	return actual_units_in_stock


def reduce_item_in_stock(item_id,no_of_items_to_reduce,centers_id):
	q="update item set actual_units_in_stock=%s where item_id=%s and centers_id=%s"
	cd=connectDB()
	conn=con.connect(**cd)
	cur=conn.cursor()
	old_stock_count=get_item_stock_count_by_item_id(item_id,centers_id)
	new_stock_count=int(old_stock_count)-int(no_of_items_to_reduce)
	if new_stock_count <1:
		new_stock_count=0;
	cur.execute(q,(new_stock_count,item_id,centers_id))
	conn.commit()
	cur.close()
	conn.close()
	return "ok"

def update_item_in_stock(name,supplier_id,actual_units_in_stock,reorder_level,centers_id):
	q="update item set actual_units_in_stock=%s, supplier_id=%s, reorder_level=%s  where name=%s and centers_id=%s"
	cd=connectDB()
	conn=con.connect(**cd)
	cur=conn.cursor()
	old_stock_count=get_item_stock_count(name,centers_id)
	new_stock_count=old_stock_count+actual_units_in_stock
	cur.execute(q,(new_stock_count,supplier_id,reorder_level,name,centers_id))
	conn.commit()
	cur.close()
	conn.close()

def get_item_name(item_id):
	item_name="n/a"
	q="select name from item where item_id=%s"
	cd=connectDB()
	conn=con.connect(**cd)
	sc=system_config()
	date=sc['current_date']
	time=sc['current_time']
	centers_id=sc['centers_id']
	waiter_id=sc['waiter_id']
	cur=conn.cursor()
	cur.execute(q,(item_id,))
	data=cur.fetchone()
	cur.close()
	conn.close()
	if len(data) >0:
		item_name=data[0]
	return item_name

def get_item_amount(item_id):
	amount="1"
	q="select selling_price_per_unit from item where item_id=%s"
	cd=connectDB()
	conn=con.connect(**cd)
	sc=system_config()
	date=sc['current_date']
	time=sc['current_time']
	centers_id=sc['centers_id']
	waiter_id=sc['waiter_id']
	cur=conn.cursor()
	cur.execute(q,(item_id,))
	data=cur.fetchone()
	cur.close()
	conn.close()
	if len(data) >0:
		amount=data[0]
	return amount

def create_sales(bill_id,item_id,no_of_items="1"):
	item_name=get_item_name(item_id)
	total_amount=get_item_amount(item_id)
	cd=connectDB()
	conn=con.connect(**cd)
	sc=system_config()
	date=sc['current_date']
	time=sc['current_time']
	centers_id=sc['centers_id']
	waiter_id=sc['waiter_id']
	q="insert into sale(bill_id,item_id,item_name,no_of_items,centers_id,waiter_id,date,time,total_amount) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	cur=conn.cursor()
	cur.execute(q,(bill_id,item_id,item_name,no_of_items,centers_id,waiter_id,date,time,total_amount))
	conn.commit()
	cur.close()
	conn.close()
	set_bill_total(bill_id)
	return "OK"

def get_current_sale_quantity(sale_id):
	no_of_items="0"
	q="select no_of_items from sale where sale_id=%s"
	cd=connectDB()
	conn=con.connect(**cd)
	sc=system_config()
	date=sc['current_date']
	time=sc['current_time']
	centers_id=sc['centers_id']
	waiter_id=sc['waiter_id']
	cur=conn.cursor()
	cur.execute(q,(sale_id,))
	data=cur.fetchone()
	cur.close()
	conn.close()
	if len(data) >0:
		no_of_items=data[0]
	return no_of_items

def delete_sale_item(sale_id,bill_id):
	cd=connectDB()
	conn=con.connect(**cd)
	sc=system_config()
	date=sc['current_date']
	trans_time=sc['current_time']
	centers_id=sc['centers_id']
	waiter_id=sc['waiter_id']
	q="delete from sale where sale_id=%s and bill_id=%s and centers_id=%s and waiter_id"
	cur=conn.cursor()
	cur.execute(q,(sale_id,bill_id,centers_id,waiter_id))
	conn.commit()
	cur.close()
	conn.close()
	set_bill_total(bill_id)
	return "ok"

def increase_single_sale_quantity(bill_id,sale_id,item_id,item_count=1):
	item_name=get_item_name(item_id)
	total_amount=get_item_amount(item_id)
	cd=connectDB()
	conn=con.connect(**cd)
	sc=system_config()
	date=sc['current_date']
	time=sc['current_time']
	centers_id=sc['centers_id']
	waiter_id=sc['waiter_id']
	current_item_count=get_current_sale_quantity(sale_id)
	no_of_items=int(current_item_count)+int(item_count)
	new_price=no_of_items*total_amount
	q="update sale set no_of_items=%s, total_amount=%s where sale_id=%s and bill_id=%s and centers_id=%s"
	cur=conn.cursor()
	cur.execute(q,(no_of_items,new_price,sale_id,bill_id,centers_id))
	conn.commit()
	cur.close()
	conn.close()
	set_bill_total(bill_id)
	return "OK"

def decrease_single_sale_quantity(bill_id,sale_id,item_id,item_count=1):
	item_name=get_item_name(item_id)
	total_amount=get_item_amount(item_id)
	cd=connectDB()
	conn=con.connect(**cd)
	sc=system_config()
	date=sc['current_date']
	time=sc['current_time']
	centers_id=sc['centers_id']
	waiter_id=sc['waiter_id']
	current_item_count=get_current_sale_quantity(sale_id)
	no_of_items=int(current_item_count)-int(item_count)
	if no_of_items < 1:
		no_of_items=0
	new_price=no_of_items*total_amount
	q="update sale set no_of_items=%s, total_amount=%s where sale_id=%s and bill_id=%s and centers_id=%s"
	cur=conn.cursor()
	cur.execute(q,(no_of_items,new_price,sale_id,bill_id,centers_id))
	conn.commit()
	cur.close()
	conn.close()
	set_bill_total(bill_id)
	return "OK"

def update_single_sale_quantity(bill_id,sale_id,item_id,item_count=1):
	item_name=get_item_name(item_id)
	total_amount=get_item_amount(item_id)
	cd=connectDB()
	conn=con.connect(**cd)
	sc=system_config()
	date=sc['current_date']
	time=sc['current_time']
	centers_id=sc['centers_id']
	waiter_id=sc['waiter_id']
	current_item_count=get_current_sale_quantity(sale_id)
	no_of_items=int(item_count)
	new_price=no_of_items*total_amount
	q="update sale set no_of_items=%s, total_amount=%s where sale_id=%s and bill_id=%s and centers_id=%s"
	cur=conn.cursor()
	cur.execute(q,(no_of_items,new_price,sale_id,bill_id,centers_id))
	conn.commit()
	cur.close()
	conn.close()
	set_bill_total(bill_id)
	return "OK"

def add_payment_mode(name,date,trans_time,centers_id,waiter_id):
	q="insert into payment_mode(name,date,trans_time,centers_id,waiter_id) values(%s,%s,%s,%s,%s)"
	cd=connectDB()
	conn=con.connect(**cd)
	sc=system_config()
	date=sc['current_date']
	trans_time=sc['current_time']
	centers_id=sc['centers_id']
	waiter_id=sc['waiter_id']
	cur=conn.cursor()
	cur.execute(q,(name,date,trans_time,centers_id,waiter_id))
	conn.commit()
	cur.close()
	conn.close()

def edit_payment_mode(payment_mode_id,name,date,trans_time,centers_id,waiter_id):
	q="update payment_mode set name=%s, date=%s, trans_time=%s, centers_id=%s ,waiter_id=%s where payment_mode_id=%s"
	cd=connectDB()
	conn=con.connect(**cd)
	sc=system_config()
	date=sc['current_date']
	trans_time=sc['current_time']
	centers_id=sc['centers_id']
	waiter_id=sc['waiter_id']
	cur=conn.cursor()
	cur.execute(q,(name,date,trans_time,centers_id,waiter_id,payment_mode_id))
	conn.commit()
	cur.close()
	conn.close()

def toggle_delete_payment_mode(payment_mode_id,visibility="hidden"):
	q="update payment_mode set visibility=%s where payment_mode_id=%s"
	cd=connectDB()
	conn=con.connect(**cd)
	sc=system_config()
	date=sc['current_date']
	trans_time=sc['current_time']
	centers_id=sc['centers_id']
	waiter_id=sc['waiter_id']
	cur=conn.cursor()
	cur.execute(q,(visibility,payment_mode_id))
	conn.commit()
	cur.close()
	conn.close()

def show_payment_modes(centers_id,visibility="show"):
	q="select * from payment_mode where centers_id=%s and visibility=%s"
	cd=connectDB()
	conn=con.connect(**cd)
	sc=system_config()
	cur=conn.cursor(dictionary=True)
	cur.execute(q,(centers_id,visibility))
	results=cur.fetchall()
	cur.close()
	conn.close()
	return results

def single_payment_mode(centers_id,payment_mode_id):
	q="select * from payment_mode where centers_id=%s and payment_mode_id=%s"
	cd=connectDB()
	conn=con.connect(**cd)
	sc=system_config()
	cur=conn.cursor(dictionary=True)
	cur.execute(q,(centers_id,payment_mode_id))
	results=cur.fetchall()
	cur.close()
	conn.close()
	return results

def make_payment(transaction_type,payment_mode_id,amount,bill_id,transaction_code,description,cash_in_hand,change_amount):
	trans_status="Completed"
	q="insert into transaction(transaction_type,payment_mode_id,amount,bill_id,date,trans_time,transaction_code,waiter_id,centers_id,description,trans_status,cash_in_hand,change_amount) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	cd=connectDB()
	conn=con.connect(**cd)
	sc=system_config()
	date=sc['current_date']
	trans_time=sc['current_time']
	centers_id=sc['centers_id']
	waiter_id=sc['waiter_id']
	cur=conn.cursor()
	cur.execute(q,(transaction_type,payment_mode_id,amount,bill_id,date,trans_time,transaction_code,waiter_id,centers_id,description,trans_status,cash_in_hand,change_amount))
	conn.commit()
	idd=cur.lastrowid
	cur.close()
	conn.close()
	return idd



#c=create_sales("3","1")
#print(c)

#print(single_bill_items("1","3"))

#print(approve_grn("1","1"))

#print(get_grn_status("1"))

#print(show_payment_modes("1"))

#print(make_payment("credit","1","200","1","QRWERG784673Y","","0","0"))

#print(post_bill("3"))





@app.route("/")
def indexpage():
	return "under construction"


@app.route("/receive-items")
def receive_goods():
	return render_template("receive-goods.html")


if __name__ == '__main__':
	app.run(port="2009", debug=True)

