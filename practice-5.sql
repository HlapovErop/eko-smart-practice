CREATE TABLE customers (
    customer_id int primary key,
    first_name text,
    last_name text,
    email text
);

create table products (
    product_id int primary key,
    product_name text,
    price int
);

create table orders (
  order_id int primary key,
  customer_id int,
  order_date date,
  total_amount int,
  constraint fk_customer foreign key (customer_id) references customers(customer_id)
);

create table orderItems (
    order_item_id int primary key,
    order_id int references orders(order_id),
    product_id int references products(product_id),
    quantity int,
    subtotal int
);


insert into products (product_id, product_name, price) VALUES (1, 'Ноутбук', 80000);
insert into customers (customer_id, first_name, last_name, email) VALUES (1, 'Иван', 'Иванов', ' ivan@mail.ru');

-- Сценарий 1
begin;
insert into orders (order_id, customer_id, order_date, total_amount)
VALUES (1, 1, current_timestamp, 80000);

insert into orderItems (order_item_id, order_id, product_id, quantity, subtotal) VALUES (1, 1, 1, 1, 80000);
update orders set total_amount = (select sum(subtotal) from orderItems where orderItems.order_id = 1) where order_id=1;
commit;

-- Сценарий 2
begin;
update customers set email='ivan777@gmail.ru' where customer_id=1;
commit;

-- Сценарий 3
begin;
insert into products (product_id, product_name, price) VALUES (2, 'Телефон', 10000);
commit;
abort;