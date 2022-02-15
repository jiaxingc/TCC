// odoo.define('agendamento_banco.myportal', function(require) {
//     'use strict';

//     var session = require('web.session');
//     var rpc = require('web.rpc');

//     $(document).ready(function() {
//         if (session.user_id) {
//             var p = $(this).find(".menu-myportal")
//             if (p.length == 1) {
//                 rpc.query({
//                         model: 'res.users',
//                         method: 'search_read',
//                         args: [
//                             [
//                                 ['id', '=', session.user_id]
//                             ]
//                         ],
//                         fields: [
//                             'partner_id'
//                         ],
//                         limit: 1
//                     })
//                     .then(function(data) {
//                         if (data.length == 1) {
//                             rpc.query({
//                                     model: 'res.partner',
//                                     method: 'search_read',
//                                     args: [
//                                         [
//                                             ['id', '=', data[0].partner_id[0]]
//                                         ]
//                                     ],
//                                     fields: [
//                                         'event_sponsor_id',
//                                         'is_event_sponsor_admin'
//                                     ],
//                                     limit: 1
//                                 })
//                                 .then(function(partner_id) {
//                                     var event_sponsor_id = partner_id[0].event_sponsor_id
//                                     var is_event_sponsor_admin = partner_id[0].is_event_sponsor_admin
//                                     if (event_sponsor_id) {
//                                         if (is_event_sponsor_admin) {
//                                             p.append("<a href='/myportal' role='menuitem' class='dropdown-item'>Portal</a>")
//                                         } else {
//                                             var str = "<a href='/expositores/representantes/sala/" + session.user_id + "' role='menuitem' class='dropdown-item'>Sala</a>"
//                                             str += "<div class='dropdown-divider'/>"
//                                             str += "<a href='/myportal' role='menuitem' class='dropdown-item'>Portal</a>"
//                                             p.append(str)
//                                         }
//                                     }
//                                 });
//                         }
//                     });
//             }
//         }
//     });
// });