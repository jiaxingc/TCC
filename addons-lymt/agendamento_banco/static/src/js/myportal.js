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


// Import stylesheets
// import './style.css';

function retornaDiaDaSemana(dia) {
    var diaSemana = '';
  
    switch (dia) {
      case 0:
        diaSemana = 'domingo';
        break;
      case 1:
        diaSemana = 'segunda';
        break;
      case 2:
        diaSemana = 'terca';
        break;
      case 3:
        diaSemana = 'quarta';
        break;
      case 4:
        diaSemana = 'quinta';
        break;
      case 5:
        diaSemana = 'sexta';
        break;
      default:
        console.log('final de semana');
    }
  
    return diaSemana;
  }
  
  function retornaMes(mes) {
    var mesReferente = '';
  
    switch (mes) {
      case 0:
        mesReferente = 'janeiro';
        break;
      case 1:
        mesReferente = 'fevereiro';
        break;
      case 2:
        mesReferente = 'março';
        break;
      case 3:
        mesReferente = 'abril';
      case 4:
        mesReferente = 'maio';
      case 5:
        mesReferente = 'junho';
        break;
      case 6:
        mesReferente = 'julho';
        break;
      case 7:
        mesReferente = 'agosto';
        break;
      case 8:
        mesReferente = 'setembro';
        break;
      case 9:
        mesReferente = 'outubro';
        break;
      case 10:
        mesReferente = 'novembro';
        break;
      case 11:
        mesReferente = 'dezembro';
        break;
      default:
        console.log('nao achou o mes');
    }
  
    return mesReferente;
  }
  
  // var date = new Date();
  
  // full date
  // console.log(date);
  
  // dia do mes
  // var diaDoMes = date.getDate();
  // console.log('Dia do mes: ', diaDoMes);
  
  // mes
  // var mes = retornaMes(date.getMonth());
  // console.log('mes: ', mes);
  
  // dia da semana
  // var diaDaSemana = retornaDiaDaSemana(date.getDay());
  // console.log('dia da semana: ', diaDaSemana);
  
  // ano
  // var ano = date.getFullYear();
  // console.log('ano: ', ano);
  
  // var dataCompleta = `${diaDaSemana}, ${diaDoMes} de ${mes} de ${ano}`;
  // console.log(dataCompleta);
  
  var diasDeSemanaElementNodes = [];
  
  function criaListaDeDiaDeSemana() {
    let date = new Date();
  
    let isDomingo = date.getDay() == 0;
  
    let counter = 0;
  
    if (isDomingo) {
      counter = 1;
    }
  
    diasDeSemanaElementNodes.forEach((element) => {
      let diaDaSemana = retornaDiaDaSemana(date.getDay() + counter);
      console.log('dia da semana: ', retornaDiaDaSemana(date.getDay() + counter));
      console.log(date.getDay() + counter);
      let dia = date.getDate() + counter;
      let mes = retornaMes(date.getMonth() + counter);
  
      element.innerHTML = `
        <span class="data-dia-semana">${diaDaSemana}</span>
        <span class="data-dia-mes">${dia} ${mes}</span>
        `;
  
      counter++;
    });
  }
  
  //cria os eventos para escutar o click no container do html
  const elSegunda = document.getElementById('segunda');
  elSegunda.addEventListener('click', tratarClickEmSegunda);
  diasDeSemanaElementNodes.push(elSegunda);
  
  const elTerca = document.getElementById('terca');
  elTerca.addEventListener('click', tratarClickEmTerca);
  diasDeSemanaElementNodes.push(elTerca);
  
  const elQuarta = document.getElementById('quarta');
  elQuarta.addEventListener('click', tratarClickEmQuarta);
  diasDeSemanaElementNodes.push(elQuarta);
  
  const elQuinta = document.getElementById('quinta');
  elQuinta.addEventListener('click', tratarClickEmQuinta);
  diasDeSemanaElementNodes.push(elQuinta);
  
  const elSexta = document.getElementById('sexta');
  elSexta.addEventListener('click', tratarClickEmSexta);
  diasDeSemanaElementNodes.push(elSexta);
  
  criaListaDeDiaDeSemana();
  
  function tratarClickEmSegunda() {
    console.log('click em segunda');
  
    //verificar se o elemento ja possui a classe
    let isSelected = elSegunda.classList.contains('selecionado');
  
    if (isSelected) {
      // caso ele ja tenha remove a classe
      elSegunda.classList.remove('selecionado');
    } else {
      //caso ele nao tenha adiciona classe quando clicado no elemento
      elSegunda.classList.add('selecionado');
    }
  }
  
  function tratarClickEmTerca() {
    console.log('click em terca');
  }
  
  function tratarClickEmQuarta() {
    console.log('click em quarta');
  }
  
  function tratarClickEmQuinta() {
    console.log('click em quinta');
  }
  
  function tratarClickEmSexta() {
    console.log('click em sexta');
  }
  
  
  
  
  
  
  