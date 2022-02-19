odoo.define('agendamento_banco.form', function(require) {
    'use strict';

    var FormEditorRegistry = require('website_form.form_editor_registry');

    FormEditorRegistry.add('create_curso', {
        formFields: [{
            type: 'char',
            required: true,
            name: 'title',
            string: 'Título',
            placeholder: 'Título'
        }, {
            type: 'char',
            required: true,
            name: 'description',
            string: 'Descrição',
            placeholder: 'Descrição'
        }, {
            type: 'char',
            required: true,
            name: 'url',
            string: 'URL',
            placeholder: 'URL'
        }]
    });

    FormEditorRegistry.add('create_video', {
        formFields: [{
            type: 'char',
            required: true,
            name: 'title',
            string: 'Título',
            placeholder: 'Título'
        }, {
            type: 'char',
            required: true,
            name: 'url',
            string: 'URL',
            placeholder: 'url'
        }]
    });

    FormEditorRegistry.add('create_catalogo', {
        formFields: [{
            type: 'char',
            required: true,
            name: 'title',
            string: 'Título',
            placeholder: 'Título'
        }, {
            type: 'char',
            required: true,
            name: 'description',
            string: 'Descrição',
            placeholder: 'Descrição'
        }, {
            type: 'binary',
            required: true,
            name: 'img',
            string: 'Imagem',
            placeholder: 'Imagem'
        }, {
            type: 'binary',
            required: true,
            name: 'catalogo',
            string: 'Catálogo',
            placeholder: 'Catálogo'
        }]
    });

    FormEditorRegistry.add('create_product', {
        formFields: [{
            type: 'char',
            required: true,
            name: 'name',
            string: 'Nome',
            placeholder: 'Nome'
        }, {
            type: 'float',
            required: true,
            name: 'list_price',
            string: 'Preço',
            placeholder: 'Preço'
        }, {
            type: 'char',
            required: true,
            name: 'url',
            string: 'URL',
            placeholder: 'URL'
        }, {
            type: 'char',
            required: false,
            name: 'description_sale',
            string: 'Descrição',
            placeholder: 'Descrição'
        }, {
            type: 'binary',
            required: false,
            name: 'image_1920',
            string: 'Imagem',
            placeholder: 'Imagem'
        }]
    });

    FormEditorRegistry.add('create_banner', {
        formFields: [{
            type: 'binary',
            required: true,
            name: 'img_desktop',
            string: 'Imagem Desktop',
            placeholder: 'Imagem Desktop'
        }, {
            type: 'binary',
            required: true,
            name: 'img_mobile',
            string: 'Imagem Mobile',
            placeholder: 'Imagem Mobile'
        }]
    });
});