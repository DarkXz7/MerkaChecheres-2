# -------------------------------------------------
# Función para comprimir archivos
import zipfile

def compress_file_to_zip(filepath, zip_filepath, compression=zipfile.ZIP_DEFLATED, compresslevel=9):
    """Compresses a file to a zip archive.

    Args:
        filepath: Path to the file to compress.
        zip_filepath: Path to the output zip file.
        compression: Compression method (e.g., zipfile.ZIP_DEFLATED).
        compresslevel: Compression level (0-9, only for DEFLATED).
    """
    with zipfile.ZipFile(zip_filepath, 'w', compression=compression, compresslevel=compresslevel) as zipf:
        zipf.write(filepath)

# -------------------------------------------------
# Función para Enviar Correos con Archivos Adjuntos

from django.core.mail import EmailMessage
from . import email_settings  # Importa la configuración de correo

def send_email_with_attachment(subject, body, to_emails, attachments=None, from_email=None):
    """
    Envía un correo electrónico con archivos adjuntos.

    Args:
        subject (str): El asunto del correo electrónico.
        body (str): El cuerpo del correo electrónico.
        to_emails (list): Una lista de direcciones de correo electrónico de destino.
        attachments (list, optional): Una lista de tuplas (filename, content, mimetype).
                                      Defaults to None.
        from_email (str, optional): La dirección de correo electrónico del remitente.
                                     Si es None, se usará DEFAULT_FROM_EMAIL de la configuración.
    """
    if from_email is None:
        from_email = email_settings.DEFAULT_FROM_EMAIL

    email = EmailMessage(
        subject,
        body,
        from_email,
        to_emails
    )

    if attachments:
        for filename, content, mimetype in attachments:
            email.attach(filename, content, mimetype)

    try:
        email.send()
        return True
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return False
