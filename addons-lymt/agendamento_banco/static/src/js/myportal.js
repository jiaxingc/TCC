odoo.define('agendamento_banco.myportal', function(require) {
    'use strict';

    var session = require('web.session'); // id do usuario logado
    var rpc = require('web.rpc');

    $(document).ready(function() {
        if (session.user_id) {
            var p = $(this).find(".menu-myportal")
            if (p.length == 1) {
              //buscando no banco
                rpc.query({
                        model: 'res.users',
                        method: 'search_read',
                        args: [
                            [
                                ['id', '=', session.user_id]
                            ]
                        ],
                        fields: [
                            'partner_id'
                        ],
                        limit: 1
                    })
                    .then(function(data) {
                        if (data.length == 1) {
                            rpc.query({
                                    model: 'agendamento.servico',
                                    method: 'search_read',
                                    args: [
                                        [
                                            ['cliente', '=', data[0].partner_id[0]],
                                            ['state', '=', 'agendado']
                                        ]
                                    ],
                                    fields: [
                                        'dataAgendada',
                                        'hora'
                                    ],
                                    limit: 1
                                })
                                .then(function(partner_id) {
                                    // var dataAgendada = partner_id[0].event_sponsor_id
                                    // var hora = partner_id[0].is_event_sponsor_admin
                                    // if (event_sponsor_id) {
                                    //     if (is_event_sponsor_admin) {
                                    //         p.append("<a href='/myportal' role='menuitem' class='dropdown-item'>Portal</a>")
                                    //     } else {
                                    //         var str = "<a href='/expositores/representantes/sala/" + session.user_id + "' role='menuitem' class='dropdown-item'>Sala</a>"
                                    //         str += "<div class='dropdown-divider'/>"
                                    //         str += "<a href='/myportal' role='menuitem' class='dropdown-item'>Portal</a>"
                                    //         p.append(str)
                                    //     }
                                    // }
                                });
                        }
                    });
            }
        }
    });
});


// Import stylesheets
// import './style.css';

// odoo.define('agendamento_banco.forms_agendamento', function (require) {
//   'use strict';
//   function retornaDiaDaSemana(dia) {
//     var diaSemana = '';

//     switch (dia) {
//       case 0:
//         diaSemana = 'domingo';
//         break;
//       case 1:
//         diaSemana = 'segunda';
//         break;
//       case 2:
//         diaSemana = 'terca';
//         break;
//       case 3:
//         diaSemana = 'quarta';
//         break;
//       case 4:
//         diaSemana = 'quinta';
//         break;
//       case 5:
//         diaSemana = 'sexta';
//         break;
//       case 6:
//         diaSemana = 'sabado';
//         break;
//       default:
//         console.log('final de semana');
//     }

//     return diaSemana;
//   }

//   function retornaMes(mes) {
//     var mesReferente = '';

//     switch (mes) {
//       case 0:
//         mesReferente = 'janeiro';
//         break;
//       case 1:
//         mesReferente = 'fevereiro';
//         break;
//       case 2:
//         mesReferente = 'março';
//         break;
//       case 3:
//         mesReferente = 'abril';
//         break
//       case 4:
//         mesReferente = 'maio';
//         break
//       case 5:
//         mesReferente = 'junho';
//         break;
//       case 6:
//         mesReferente = 'julho';
//         break;
//       case 7:
//         mesReferente = 'agosto';
//         break;
//       case 8:
//         mesReferente = 'setembro';
//         break;
//       case 9:
//         mesReferente = 'outubro';
//         break;
//       case 10:
//         mesReferente = 'novembro';
//         break;
//       case 11:
//         mesReferente = 'dezembro';
//         break;
//       default:
//         console.log('nao achou o mes');
//     }

//     return mesReferente;
//   }

//   function pushDateIntoHtmlNodes(day, mesHtmlNode) {
//     let dateObject = new Date();
//     diasDeSemanaElementNodes.forEach(
//       (element) => {
//         let diaDaSemana = retornaDiaDaSemana(dateObject.getDay() + day);
//         let dia = dateObject.getDate() + day;
//         element.innerHTML = `
//         <span class="data-dia-semana">${diaDaSemana}</span>
//         <span class="data-dia-mes">${dia} ${mesHtmlNode}</span>
//         `;

//         day++;
//       });
//   }

//   var diasDeSemanaElementNodes = [];

//   function criaListaDeDiaDeSemana() {
//     let date = new Date();

//     let diaSemana = date.getDay()
//     let mes = date.getMonth()


//     switch (diaSemana) {
//       case 0:
//         pushDateIntoHtmlNodes(1, retornaMes(mes))
//         break;
//       case 1:
//         pushDateIntoHtmlNodes(1, retornaMes(mes))
//         break;
//       case 2:
//         pushDateIntoHtmlNodes(-1, retornaMes(mes))
//         break;
//       case 3:
//         pushDateIntoHtmlNodes(-2, retornaMes(mes))
//         break;
//       case 4:
//         pushDateIntoHtmlNodes(-3, retornaMes(mes))
//         break;
//       case 5:
//         pushDateIntoHtmlNodes(-4, retornaMes(mes))
//         break;
//       case 6:
//         pushDateIntoHtmlNodes(-5, retornaMes(mes))
//         break;

//       default:
//         break;
//     }
//   }

//   function tratarClickEmSegunda() {
//     console.log('click em segunda');

//     //verificar se o elemento ja possui a classe
//     let isSelected = elSegunda.classList.contains('selecionado');

//     if (isSelected) {
//       // caso ele ja tenha remove a classe
//       elSegunda.classList.remove('selecionado');
//     } else {
//       //caso ele nao tenha adiciona classe quando clicado no elemento
//       elSegunda.classList.add('selecionado');
//       let meusElementosFilhos = elSegunda.getElementsByTagName('span');
//       diaDaSemanaSelecionado = meusElementosFilhos[0].innerText;
//       let diaEMes = meusElementosFilhos[1].innerText.split(' ')
//       diaDoMesSelecionado = diaEMes[0];
//       mesSelecionado = diaEMes[1];

//       console.log("diaDaSemana:", diaDaSemanaSelecionado)
//       console.log("diaDoMes:", diaDoMesSelecionado)
//       console.log("mes:", mesSelecionado)
//     }
//   }

//   function tratarClickEmTerca() {
//     console.log('click em terca');

//     //verificar se o elemento ja possui a classe
//     let isSelected = elTerca.classList.contains('selecionado');

//     if (isSelected) {
//       // caso ele ja tenha remove a classe
//       elTerca.classList.remove('selecionado');
//     } else {
//       //caso ele nao tenha adiciona classe quando clicado no elemento
//       elTerca.classList.add('selecionado');
//       let meusElementosFilhos = elTerca.getElementsByTagName('span');
//       diaDaSemanaSelecionado = meusElementosFilhos[0].innerText;
//       let diaEMes = meusElementosFilhos[1].innerText.split(' ')
//       diaDoMesSelecionado = diaEMes[0];
//       mesSelecionado = diaEMes[1];

//       console.log("diaDaSemana:", diaDaSemanaSelecionado)
//       console.log("diaDoMes:", diaDoMesSelecionado)
//       console.log("mes:", mesSelecionado)
//     }
//   }

//   function tratarClickEmQuarta() {
//     console.log('click em quarta');

//     //verificar se o elemento ja possui a classe
//     let isSelected = elQuarta.classList.contains('selecionado');

//     if (isSelected) {
//       // caso ele ja tenha remove a classe
//       elQuarta.classList.remove('selecionado');
//     } else {
//       //caso ele nao tenha adiciona classe quando clicado no elemento
//       elQuarta.classList.add('selecionado');
//       let meusElementosFilhos = elQuarta.getElementsByTagName('span');
//       diaDaSemanaSelecionado = meusElementosFilhos[0].innerText;
//       let diaEMes = meusElementosFilhos[1].innerText.split(' ')
//       diaDoMesSelecionado = diaEMes[0];
//       mesSelecionado = diaEMes[1];

//       console.log("diaDaSemana:", diaDaSemanaSelecionado)
//       console.log("diaDoMes:", diaDoMesSelecionado)
//       console.log("mes:", mesSelecionado)
//     }
//   }

//   function tratarClickEmQuinta() {
//     console.log('click em quinta');

//     //verificar se o elemento ja possui a classe
//     let isSelected = elQuinta.classList.contains('selecionado');

//     if (isSelected) {
//       // caso ele ja tenha remove a classe
//       elQuinta.classList.remove('selecionado');
//     } else {
//       //caso ele nao tenha adiciona classe quando clicado no elemento
//       elQuinta.classList.add('selecionado');
//       let meusElementosFilhos = elQuinta.getElementsByTagName('span');
//       diaDaSemanaSelecionado = meusElementosFilhos[0].innerText;
//       let diaEMes = meusElementosFilhos[1].innerText.split(' ')
//       diaDoMesSelecionado = diaEMes[0];
//       mesSelecionado = diaEMes[1];

//       console.log("diaDaSemana:", diaDaSemanaSelecionado)
//       console.log("diaDoMes:", diaDoMesSelecionado)
//       console.log("mes:", mesSelecionado)
//     }
//   }

//   function tratarClickEmSexta() {
//     console.log('click em sexta');

//     //verificar se o elemento ja possui a classe
//     let isSelected = elSexta.classList.contains('selecionado');

//     if (isSelected) {
//       // caso ele ja tenha remove a classe
//       elSexta.classList.remove('selecionado');
//     } else {
//       //caso ele nao tenha adiciona classe quando clicado no elemento
//       elSexta.classList.add('selecionado');
//       let meusElementosFilhos = elSexta.getElementsByTagName('span');
//       diaDaSemanaSelecionado = meusElementosFilhos[0].innerText;
//       let diaEMes = meusElementosFilhos[1].innerText.split(' ')
//       diaDoMesSelecionado = diaEMes[0];
//       mesSelecionado = diaEMes[1];

//       console.log("diaDaSemana:", diaDaSemanaSelecionado)
//       console.log("diaDoMes:", diaDoMesSelecionado)
//       console.log("mes:", mesSelecionado)
//     }
//   }

//   function tratarClickEmPrimeiroHorario() {
//     let meusElementosFilhos = elPrimeiroHorario.getElementsByTagName('label');
//     horarioSelecionado = meusElementosFilhos[0].innerText
//     console.log("selecionei horario:", horarioSelecionado)
//   }
//   function tratarClickEmSegundoHorario() {
//     let meusElementosFilhos = elSegundoHorario.getElementsByTagName('label');
//     horarioSelecionado = meusElementosFilhos[0].innerText
//     console.log("selecionei horario:", horarioSelecionado)
//   }
//   function tratarClickEmTerceiroHorario() {
//     let meusElementosFilhos = elTerceiroHorario.getElementsByTagName('label');
//     horarioSelecionado = meusElementosFilhos[0].innerText
//     console.log("selecionei horario:", horarioSelecionado)
//   }
//   function tratarClickEmQuartoHorario() {
//     let meusElementosFilhos = elQuartoHorario.getElementsByTagName('label');
//     horarioSelecionado = meusElementosFilhos[0].innerText
//     console.log("selecionei horario:", horarioSelecionado)
//   }
//   function tratarClickEmQuintoHorario() {
//     let meusElementosFilhos = elQuintoHorario.getElementsByTagName('label');
//     horarioSelecionado = meusElementosFilhos[0].innerText
//     console.log("selecionei horario:", horarioSelecionado)
//   }

//   //variaveis selecionadas 
//   var diaDaSemanaSelecionado;
//   var diaDoMesSelecionado;
//   var mesSelecionado;
//   var horarioSelecionado;

//   //cria os eventos para escutar o click no container do html
//   const elSegunda = document.getElementById('segunda');
//   elSegunda.addEventListener('click', tratarClickEmSegunda);
//   diasDeSemanaElementNodes.push(elSegunda);

//   const elTerca = document.getElementById('terca');
//   elTerca.addEventListener('click', tratarClickEmTerca);
//   diasDeSemanaElementNodes.push(elTerca);

//   const elQuarta = document.getElementById('quarta');
//   elQuarta.addEventListener('click', tratarClickEmQuarta);
//   diasDeSemanaElementNodes.push(elQuarta);

//   const elQuinta = document.getElementById('quinta');
//   elQuinta.addEventListener('click', tratarClickEmQuinta);
//   diasDeSemanaElementNodes.push(elQuinta);

//   const elSexta = document.getElementById('sexta');
//   elSexta.addEventListener('click', tratarClickEmSexta);
//   diasDeSemanaElementNodes.push(elSexta);

//   const elPrimeiroHorario = document.getElementById('primeiro-horario');
//   elPrimeiroHorario.addEventListener('click', tratarClickEmPrimeiroHorario);

//   const elSegundoHorario = document.getElementById('segundo-horario');
//   elSegundoHorario.addEventListener('click', tratarClickEmSegundoHorario);

//   const elTerceiroHorario = document.getElementById('terceiro-horario');
//   elTerceiroHorario.addEventListener('click', tratarClickEmTerceiroHorario);

//   const elQuartoHorario = document.getElementById('quarto-horario');
//   elQuartoHorario.addEventListener('click', tratarClickEmQuartoHorario);

//   const elQuintoHorario = document.getElementById('quinto-horario');
//   elQuintoHorario.addEventListener('click', tratarClickEmQuintoHorario);

//   criaListaDeDiaDeSemana();

//   // botão enviar 

//   const submit_button = document.getElementById('enviar');

//   function btn_send() {
//     console.log(mesSelecionado)
//     return mesSelecionado
//   }

//   submit_button.addEventListener('click', btn_send);
//   var ajax = require('web.ajax');
//   ajax.jsonRpc("/url", 'call', {
//     'input_data': $('#input').val(),
//   })
//   //   .then(function (data) {
    
//   //   var output_data = data['output_data']
//   //   $("#output").html(output_data);
//   // });
// })