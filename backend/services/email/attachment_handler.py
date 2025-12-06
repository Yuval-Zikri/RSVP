"""Email attachment handler for background images."""
import os


def attach_background_image(msg, attachment_cid):
    """Attach background image to email message
    
    Args:
        msg: Flask-Mail Message object
        attachment_cid: CID/filename of the background image
        
    Returns:
        bool: True if attached successfully, False otherwise
    """
    if not attachment_cid:
        return False
        
    try:
        file_path = os.path.join('/app/backgrounds', attachment_cid)
        with open(file_path, 'rb') as f:
            file_data = f.read()
            # Guess content type based on extension
            content_type = 'image/jpeg'
            if attachment_cid.lower().endswith('.png'):
                content_type = 'image/png'
                
            msg.attach(
                filename=attachment_cid,
                content_type=content_type,
                data=file_data,
                disposition='inline',
                headers=[['Content-ID', f'<{attachment_cid}>']]
            )
            print(f"DEBUG: Attached {attachment_cid} to email")
            return True
    except Exception as e:
        print(f"ERROR: Failed to attach file {attachment_cid}: {e}")
        return False
