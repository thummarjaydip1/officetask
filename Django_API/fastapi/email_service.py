from fastapi_mail import FastMail, MessageSchema, MessageType
from config import conf

# register email
async def register_send_email(
    email : str,
    username : str,
    address : str,
):
    email_message = MessageSchema(
        subject = "User register successfully",
        recipients = [email],
        body = f"""
            <html>
                <body>

                    <h2>New user register</h2>
                    <hr>
                    <p> <b>User : </b> {username}</p>
                    <p> <b>Email : </b> {email}</p> <br />
                    <p> <b>Address : </b> {address}</p> <br />
                    <b>Thank You</b>
                
                </body> 
            </html>
        """,
        subtype = MessageType.html
    )

    fm = FastMail(conf)

    await fm.send_message(email_message)
    

# login email
async def login_send_email(
    username : str,
    email : str
):
    email_message = MessageSchema(
        subject = "User login successfully",
        recipients = [email],
        body= f"""
            <html>
                <body>
                
                    <h2>Login Successfully</h2>
                    <hr>
                    <p><b>User : </b> {username}</p> <br />
                    <p><b>Email : </b> {email}</p> <br />
                
                </body>
            </html>
        """,
        subtype = MessageType.html
    )

    fm = FastMail(conf)

    await fm.send_message(email_message)


# logout email
async def logout_send_email(
    username : str,
    email : str
):
    email_message = MessageSchema(
        subject = "User Logout Successfully",
        recipients = [email],
        body = f"""
            <html>
                <body>
                
                    <h2>Logout Successfully</h2>
                    <hr>
                    <p><b>Username : </b> {username} </p> <br />
                    <p><b>Email : </b> {email} </p> <br />       
                    
                </body>
            </html>
        """,
        subtype = MessageType.html
    )

    fm = FastMail(conf)

    await fm.send_message(email_message)


# order email
async def order_send_email(
    username : str,
    email : str,
    product_name : str,
    price : int,
    quantity : int,
    total_price : int,
    delivery_address : str    
):
    email_message = MessageSchema(
        subject = "Order Place Successfully",
        recipients = [email],
        body = f"""
            <html>
                <body>

                    <h2>Order Place Successfully</h2>
                    <p><b>Username : </b> {username} </p> <br />
                    <p><b>Email :</b> {email}</p> <br />
                    <p><b>Product Name : </b> {product_name} </p> <br />
                    <p><b>Price : </b> {price} </p> <br /> 
                    <p><b>Quantity : </b>{quantity} </p> <br />
                    <p><b>Total Price</b> {total_price} </p> <br />
                    <p><b>Delivery Address : </b> {delivery_address} </p> <br />

                </body>
            </html>
        """,
        subtype = MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(email_message)

