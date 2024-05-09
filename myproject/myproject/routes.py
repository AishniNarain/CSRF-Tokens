from pyramid.view import notfound_view_config, forbidden_view_config

def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('form','/form')
    config.add_route('login', '/login')
    config.add_route('success', '/success')
    
    
