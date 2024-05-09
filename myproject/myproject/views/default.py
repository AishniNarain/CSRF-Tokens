from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy.exc import SQLAlchemyError
from pyramid.csrf import check_csrf_token
from pyramid.csrf import get_csrf_token
from pyramid.renderers import render_to_response

from .. import models

@view_config(route_name='home', renderer='myproject:templates/mytemplate.jinja2')
def my_view(request):
    try:
        query = request.dbsession.query(models.MyModel)
        one = query.filter(models.MyModel.name == 'one').one()
    except SQLAlchemyError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'one': one, 'project': 'myproject'}

# @view_config(route_name='login', renderer='templates/login.jinja2')
# def login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         # Check username and password (add your authentication logic here)
#         if username == 'admin' and password == 'admin':
#             headers = remember(request, username)
#             return HTTPFound(location='/', headers=headers)
#         else:
#             return {'error': 'Invalid credentials'}
#     return {}

# @view_config(route_name='logout')
# def logout(request):
#     headers = forget(request)
#     return HTTPFound(location='/', headers=headers)

@view_config(route_name='form', renderer='templates/login.jinja2', request_method='GET')
def login_get(request):
    if request.method == 'GET':
        # Get CSRF token for GET request
        csrf_token = get_csrf_token(request)
        # Render the login form template with CSRF token
        return render_to_response('templates/login.jinja2', {'csrf_token': csrf_token}, request=request)

@view_config(route_name='login',request_method = 'POST')
def login_post(request):
    if request.method == 'POST':
        # Validate CSRF token from custom header
        csrf_token = request.headers.get('X-CSRF-Token')
        
        if not csrf_token or not check_csrf_token(request, token=csrf_token):
            return Response('Bad CSRF token', status=400)

        # Get username and password from the form
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Validate credentials
        if username and password:
        # Perform login/authentication logic here
            if validate_credentials(username, password):
                return Response('Login successful!')
            else:
                return Response('Invalid username or password', status=400)
    else:
        return Response('Username and password are required', status=400)
    
def validate_credentials(username, password):
    if username == 'admin' and password == 'admin':
        return True
    else:
        return False
    

db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for descriptions and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
