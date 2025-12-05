
BACKGROUND_MAPPING = {
    # Wedding
    'wadding.jpg': 'https://images.unsplash.com/photo-1519751138087-5bf79df62d58?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
    'wadding2.jpg': 'https://images.unsplash.com/photo-1519751138087-5bf79df62d58?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
}

def get_bg_url(bg_url):
    print(f"Input: {bg_url}")
    if bg_url and not bg_url.startswith('http'):
            # It's a local filename, check the mapping
            if bg_url in BACKGROUND_MAPPING:
                bg_url = BACKGROUND_MAPPING[bg_url]
            else:
                # Fallback to a default Unsplash image if no valid URL is present
                bg_url = 'https://images.unsplash.com/photo-1519751138087-5bf79df62d58?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
    elif not bg_url:
        # Fallback to a default Unsplash image if no valid URL is present
        bg_url = 'https://images.unsplash.com/photo-1519751138087-5bf79df62d58?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
    
    print(f"Output: {bg_url}")
    return bg_url

# Test cases
get_bg_url('wadding.jpg')
get_bg_url('wadding2.jpg')
get_bg_url('unknown.jpg')
get_bg_url(None)
get_bg_url('')
