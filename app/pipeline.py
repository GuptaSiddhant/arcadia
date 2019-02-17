def get_avatar(backend, strategy, details, response,
               user=None, *args, **kwargs):
    url = None
    if backend.name == 'github':
        url = response.get('avatar_url')
    if backend.name == 'twitter':
        url = response.get('profile_image_url', '').replace('_normal', '').replace('http', 'https')
    if backend.name == 'google-oauth2':
        url = response['picture']
        ext = url.split('.')[-1]
    if url:
        user.image = url
        user.save()
