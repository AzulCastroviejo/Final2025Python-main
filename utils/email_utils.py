"""
Utility for sending emails, such as order confirmations.

This module uses Python's built-in smtplib and email libraries to send
emails via an SMTP server. It retrieves SMTP credentials from environment
variables for security.
"""
import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict

from utils.logging_utils import get_sanitized_logger

logger = get_sanitized_logger(__name__)

# --- SMTP Configuration from Environment Variables ---
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() in ("true", "1", "t")


def create_order_confirmation_html(order_id: int, client_name: str, total: float, order_details: List[Dict]) -> str:
    """Creates a simple HTML body for the order confirmation email."""
    
    products_html = ""
    for detail in order_details:
        product = detail.get("product", {})
        products_html += f"""
        <tr>
            <td style="padding: 10px; border-bottom: 1px solid #ddd;">{product.get("name", "N/A")}</td>
            <td style="padding: 10px; border-bottom: 1px solid #ddd; text-align: center;">{detail.get("quantity", 0)}</td>
            <td style="padding: 10px; border-bottom: 1px solid #ddd; text-align: right;">${detail.get("price", 0):.2f}</td>
        </tr>
        """

    html_content = f"""
    <html>
        <head></head>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <h2>¡Gracias por tu compra, {client_name}!</h2>
            <p>Hemos recibido tu pedido y lo estamos procesando. Aquí tienes un resumen:</p>
            <p><b>Número de Pedido:</b> {order_id}</p>
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr>
                        <th style="padding: 10px; border-bottom: 2px solid #333; text-align: left;">Producto</th>
                        <th style="padding: 10px; border-bottom: 2px solid #333; text-align: center;">Cantidad</th>
                        <th style="padding: 10px; border-bottom: 2px solid #333; text-align: right;">Precio</th>
                    </tr>
                </thead>
                <tbody>
                    {products_html}
                </tbody>
            </table>
            <h3 style="text-align: right; margin-top: 20px;">Total del Pedido: ${total:.2f}</h3>
            <p>Recibirás otra notificación cuando tu pedido haya sido enviado.</p>
            <p>¡Gracias por confiar en nosotros!</p>
        </body>
    </html>
    """
    return html_content

def send_order_confirmation_email(client_email: str, client_name: str, order_id: int, total: float, order_details: List[Dict]):
    """
    Sends an order confirmation email to the client.

    Args:
        client_email: The recipient's email address.
        client_name: The name of the client.
        order_id: The ID of the order.
        total: The total amount of the order.
        order_details: A list of dictionaries, each representing a product in the order.
    """
    if not all([EMAIL_HOST_USER, EMAIL_HOST_PASSWORD]):
        logger.warning(
            "Email credentials (EMAIL_HOST_USER, EMAIL_HOST_PASSWORD) are not set. " 
            "Skipping email notification."
        )
        return

    logger.info(f"Attempting to send order confirmation email for order {order_id} to {client_email}")

    message = MIMEMultipart("alternative")
    message["Subject"] = f"Confirmación de tu Pedido #{order_id}"
    message["From"] = EMAIL_HOST_USER
    message["To"] = client_email

    # Create the HTML part of the email
    html_body = create_order_confirmation_html(order_id, client_name, total, order_details)
    message.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            if EMAIL_USE_TLS:
                server.starttls()
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            server.sendmail(EMAIL_HOST_USER, client_email, message.as_string())
            logger.info(f"Successfully sent email for order {order_id} to {client_email}")
    except smtplib.SMTPAuthenticationError as e:
        logger.error(
            f"SMTP Authentication failed for user {EMAIL_HOST_USER}. " 
            f"Check EMAIL_HOST_USER and EMAIL_HOST_PASSWORD. Error: {e}"
        )
    except Exception as e:
        logger.error(f"Failed to send email for order {order_id}. Error: {e}", exc_info=True)
