# -*- coding: utf-8 -*-
import requests
import re
import logging
import werkzeug
from odoo import http, _
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.exceptions import UserError
from odoo.http import request
from odoo.addons.auth_signup.controllers.main import AuthSignupHome

_logger = logging.getLogger(__name__)

class AuthSignupHomeInherit(AuthSignupHome):
    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        values = {key: qcontext.get(key) for key in ('login', 'name', 'cpf_cnpj', 'password', 'phone', 'zip', 'rg', 'street', 'street2', 'city', 'state_id', 'country_id')}
        values.update({'zip': qcontext.get('zip', None)})
        if values['zip'] and re.findall(r'^\d{8}$', values['zip']):
            zip = values['zip']
            print(zip)
            url = f"https://viacep.com.br/ws/{zip}/json/"
            try:
                resp = requests.get(url)
                print(resp)
                if resp.status_code == 200 and not resp.json().get('erro', False):
                    _json = resp.json()
                    print(_json)
                    street = _json.get('logradouro', None)
                    street2 = _json.get('complemento', None)
                    city = _json.get('localidade', None)
                    country_id = request.env['res.country'].search([('code', '=', 'BR')], limit=1)
                    state_id = request.env['res.country.state'].search([('code', '=', _json.get('uf', None)),('country_id', '=', country_id.id)], limit=1)
                    print(f"Pais id: {country_id} / Estado id: {state_id}")
                    values.update({'street': street,
                    'street2': street2,
                    'city': city,
                    'state_id': int(state_id),
                    'country_id': int(country_id),
                    })
            except:
                _logger.error("erro ao pesquisar o CEP.")
        if not values:
            raise UserError(_("The form was not properly filled in."))
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))

        self._signup_with_values(qcontext.get('token'), values)
        print(f'Values do_signup: {values}')
        request.env.cr.commit()

    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)
                # Send an account creation confirmation email
                if qcontext.get('token'):
                    User = request.env['res.users']
                    print(f'User: {User}')
                    user_sudo = User.sudo().search(
                        User._get_login_domain(qcontext.get('login')), order=User._get_login_order(), limit=1
                    )
                    template = request.env.ref('auth_signup.mail_template_user_signup_account_created', raise_if_not_found=False)

                    if user_sudo and template:
                        template.sudo().send_mail(user_sudo.id, force_send=True)
                return self.web_login(*args, **kw)
            except UserError as e:
                qcontext['error'] = e.args[0]
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    _logger.error("%s", e)
                    qcontext['error'] = _("Could not create a new account.")

        response = request.render('auth_signup.signup', qcontext)
        response.headers['X-Frame-Options'] = 'DENY'
        return response