"""Email template generator for event invitations."""
import os


def generate_email_html(event, guest_name, rsvp_link):
    """Generate HTML email body for invitations and reminders
    
    Args:
        event: Event object with details
        guest_name: Name of the guest
        rsvp_link: URL for RSVP page
        
    Returns:
        tuple: (html_body, attachment_cid) - HTML string and CID for attachment if needed
    """
    # Ensure we have a valid URL for the email background
    bg_url = event.email_background_url
    print(f"DEBUG: Raw email_background_url: {bg_url}")
    
    attachment_cid = None
    
    if bg_url and not bg_url.startswith('http'):
         # It's a local filename, try to attach it
         file_path = os.path.join('/app/backgrounds', bg_url)
         if os.path.exists(file_path):
             attachment_cid = bg_url # Use filename as CID
             bg_url = f"cid:{attachment_cid}"
             print(f"DEBUG: Attaching local file: {file_path} as CID: {attachment_cid}")
         else:
             print(f"DEBUG: Local file not found: {file_path}")
             # Fallback to a default Unsplash image if file not found
             bg_url = 'https://images.unsplash.com/photo-1519751138087-5bf79df62d58?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
    elif not bg_url:
        # Fallback to a default Unsplash image if no valid URL is present
        bg_url = 'https://images.unsplash.com/photo-1519751138087-5bf79df62d58?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
    
    print(f"DEBUG: Final bg_url: {bg_url}")

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ margin: 0; padding: 0; width: 100% !important; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; background-color: transparent; }}
            img {{ border: 0; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; }}
            .btn-primary {{ 
                background-color: #007bff; 
                color: #ffffff; 
                padding: 14px 28px; 
                text-decoration: none; 
                border-radius: 50px; 
                font-weight: bold; 
                display: inline-block;
                mso-padding-alt: 0;
                text-underline-color: #007bff;
            }}
            .btn-nav {{
                background-color: #ffffff;
                color: #007bff;
                border: 1px solid #007bff;
                padding: 8px 16px;
                text-decoration: none;
                border-radius: 50px;
                font-size: 14px;
                display: inline-block;
                margin: 0 5px;
            }}
        </style>
    </head>
    <body style="margin: 0; padding: 0; background-color: transparent;">
        <!-- Main Table Container (Full Width Gray Background) -->
        <table border="0" cellpadding="0" cellspacing="0" width="100%" height="100%" style="min-height: 100vh; background-color: transparent;">
            <tr>
                <td align="center" valign="top" style="padding: 40px 0;">
                    
                    <!-- Phone Container (Centered, Fixed Width) -->
                    <!-- Using max-width 500px to match mobile preview -->
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 500px; width: 100%; margin: 0 auto; border-radius: 20px; overflow: hidden; box-shadow: 0 20px 40px rgba(0,0,0,0.2);">
                        <tr>
                            <td align="center" valign="middle" background="{bg_url}" style="padding: 0; background-image: url('{bg_url}'); background-size: cover; background-position: center; background-repeat: no-repeat; background-color: #e6f7ff; height: 640px;">
                                <!--[if gte mso 9]>
                                <v:rect xmlns:v="urn:schemas-microsoft-com:vml" fill="true" stroke="false" style="width:500px;height:640px;">
                                <v:fill type="frame" src="{bg_url}" color="#e6f7ff" />
                                <v:textbox inset="0,0,0,0">
                                <![endif]-->
                                
                                <!-- Content Wrapper (to center the card vertically if needed, or just padding) -->
                                <div style="padding: 20px;">
                                    <!-- Card Container -->
                                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: rgba(255, 255, 255, 0.95); border-radius: 16px; box-shadow: 0 8px 32px rgba(0,0,0,0.1); backdrop-filter: blur(10px);">
                                        <tr>
                                            <td align="center" style="padding: 30px 20px;">
                                                
                                                <!-- Event Type -->
                                                <div style="text-transform: uppercase; letter-spacing: 2px; font-size: 12px; color: #666; margin-bottom: 10px; font-weight: bold; font-family: Helvetica, Arial, sans-serif;">
                                                    {event.type.upper()}
                                                </div>

                                                <!-- Event Title -->
                                                <h1 style="margin: 10px 0; font-size: 28px; font-weight: 700; color: #1a1a1a; line-height: 1.2; font-family: Helvetica, Arial, sans-serif;">
                                                    {event.title}
                                                </h1>

                                                <!-- Subtitle -->
                                                {f'<div style="font-size: 18px; color: #4a4a4a; margin-bottom: 20px; font-family: Georgia, serif; font-style: italic;">{event.subtitle}</div>' if event.subtitle else ''}

                                                <!-- Details -->
                                                <table border="0" cellpadding="0" cellspacing="0" style="margin: 20px auto; text-align: left;">
                                                    <tr>
                                                        <td style="padding: 5px 0; font-size: 14px; color: #333; font-family: Helvetica, Arial, sans-serif;">
                                                            <span style="margin-right: 8px; font-size: 16px;">📅</span>
                                                            {event.date.strftime('%A, %B %d, %Y')} at {event.date.strftime('%I:%M %p')}
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td style="padding: 5px 0; font-size: 14px; color: #333; font-family: Helvetica, Arial, sans-serif;">
                                                            <span style="margin-right: 8px; font-size: 16px;">📍</span>
                                                            {event.location}
                                                        </td>
                                                    </tr>
                                                </table>

                                                <!-- RSVP Button -->
                                                <div style="margin-top: 20px; margin-bottom: 20px;">
                                                    <!--[if mso]>
                                                    <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="{rsvp_link}" style="height:40px;v-text-anchor:middle;width:160px;" arcsize="50%" stroke="f" fillcolor="#007bff">
                                                    <w:anchorlock/>
                                                    <center>
                                                    <![endif]-->
                                                        <a href="{rsvp_link}" class="btn-primary" style="color: #ffffff; font-family: Helvetica, Arial, sans-serif; padding: 10px 24px; font-size: 14px;">RSVP Now</a>
                                                    <!--[if mso]>
                                                    </center>
                                                    </v:roundrect>
                                                    <![endif]-->
                                                </div>

                                                <!-- Navigation Buttons -->
                                                {f'''
                                                <table border="0" cellpadding="0" cellspacing="0" style="margin: 15px auto 0 auto;">
                                                    <tr>
                                                        <td style="padding: 0 5px;">
                                                            <!--[if mso]>
                                                            <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="https://waze.com/ul?ll={event.latitude},{event.longitude}&navigate=yes" style="height:32px;v-text-anchor:middle;width:100px;" arcsize="50%" strokecolor="#007bff" fillcolor="#ffffff">
                                                            <w:anchorlock/>
                                                            <center style="color:#007bff;font-family:Helvetica, Arial,sans-serif;font-size:12px;font-weight:bold;">Waze</center>
                                                            </v:roundrect>
                                                            <![endif]-->
                                                            <a href="https://waze.com/ul?ll={event.latitude},{event.longitude}&navigate=yes" style="background-color: #ffffff; color: #007bff; border: 1px solid #007bff; padding: 8px 20px; text-decoration: none; border-radius: 50px; font-size: 12px; font-weight: bold; display: inline-block; font-family: Helvetica, Arial, sans-serif; mso-hide:all;">🚗 Waze</a>
                                                        </td>
                                                        <td style="padding: 0 5px;">
                                                            <!--[if mso]>
                                                            <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="https://www.google.com/maps/search/?api=1&query={event.latitude},{event.longitude}" style="height:32px;v-text-anchor:middle;width:100px;" arcsize="50%" strokecolor="#007bff" fillcolor="#ffffff">
                                                            <w:anchorlock/>
                                                            <center style="color:#007bff;font-family:Helvetica, Arial,sans-serif;font-size:12px;font-weight:bold;">Maps</center>
                                                            </v:roundrect>
                                                            <![endif]-->
                                                            <a href="https://www.google.com/maps/search/?api=1&query={event.latitude},{event.longitude}" style="background-color: #ffffff; color: #007bff; border: 1px solid #007bff; padding: 8px 20px; text-decoration: none; border-radius: 50px; font-size: 12px; font-weight: bold; display: inline-block; font-family: Helvetica, Arial, sans-serif; mso-hide:all;">🗺️ Maps</a>
                                                        </td>
                                                    </tr>
                                                </table>
                                                ''' if event.latitude and event.longitude else ''}

                                                <!-- Footer -->
                                                <div style="margin-top: 20px; font-size: 10px; color: #888; border-top: 1px solid #eee; padding-top: 15px; font-family: Helvetica, Arial, sans-serif;">
                                                    <p style="margin: 3px 0;">Hello {guest_name}, we can't wait to see you!</p>
                                                    <p style="margin: 3px 0;">If the button doesn't work: <br><a href="{rsvp_link}" style="color: #007bff; text-decoration: none;">Link</a></p>
                                                </div>

                                            </td>
                                        </tr>
                                    </table>
                                </div>

                                <!--[if gte mso 9]>
                                </v:textbox>
                                </v:rect>
                                <![endif]-->
                            </td>
                        </tr>
                    </table>

                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    return html_body, attachment_cid
