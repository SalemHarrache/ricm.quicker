$(function () {
  var startDate;
  var endDate;

  Date.prototype.getWeek = function () {
    return $.datepicker.iso8601Week(this);
  }

  var selectCurrentWeek = function () {
    window.setTimeout(function () {
      $('#ui-datepicker-div').find('.ui-datepicker-current-day a').addClass('ui-state-active')
    }, 1);
  }

  $('.week-picker').datepicker({
    showOtherMonths: true,
    selectOtherMonths: true,
    onSelect: function (dateText, inst) {
      var date = $(this).datepicker('getDate');
      startDate = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay()-1);
      endDate = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay() + 5);
      
      
      date = new Date();
      //handle end of weeks
      if (date.getDay() > 5){
        date.setDate(date.getDate()+2);
      }
      var today = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay());
      var weekno = today.getWeek();
      var offset = startDate.getWeek() - weekno;
      
      //handle year change
      var yeardiff =  today.getYear() - startDate.getYear();
      if (yeardiff != 0) {
        offset = offset - (52*yeardiff);
      }

      var newPathname = $("#dry_link").val();
      selectCurrentWeek();
       
      window.location = newPathname+offset;
    },
    beforeShowDay: function (date) {
      selectCurrentWeek();
      var cssClass = '';
      if (date >= startDate && date <= endDate) cssClass = 'ui-datepicker-current-day';
      return [true, cssClass];
    },
    onChangeMonthYear: function (year, month, inst) {
      selectCurrentWeek();
    },
    showOn: 'button',
    buttonText: 'Sélectionner une semaine',
    firstDay: 6
  });

  $('#ui-datepicker-div').live('focus', function () {
    selectCurrentWeek();
  });
  $('#ui-datepicker-div tr').live('mousemove', function () {
    $(this).find('td a').addClass('ui-state-hover');
  });
  $('#ui-datepicker-div tr').live('mouseleave', function () {
    $(this).find('td a').removeClass('ui-state-hover');
  });
  
  //set location
  $.datepicker.setDefaults( $.datepicker.regional[ "" ] );
  $.datepicker.regional['fr'] = 
  { 
    clearText: 'Effacer', clearStatus: '',
    closeText: 'Fermer', closeStatus: 'Fermer sans modifier',
    prevText: '<Préc', prevStatus: 'Voir le mois précédent',
    nextText: 'Suiv>', nextStatus: 'Voir le mois suivant',
    currentText: 'Courant', currentStatus: 'Voir le mois courant',
    monthNames: ['Janvier','Février','Mars','Avril','Mai','Juin',
    'Juillet','Août','Septembre','Octobre','Novembre','Décembre'],
    monthNamesShort: ['Jan','Fév','Mar','Avr','Mai','Jun',
    'Jul','Aoû','Sep','Oct','Nov','Déc'],
    monthStatus: 'Voir un autre mois', yearStatus: 'Voir un autre année',
    weekHeader: 'Sm', weekStatus: '',
    dayNames: ['Dimanche','Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi'],
    dayNamesShort: ['Dim','Lun','Mar','Mer','Jeu','Ven','Sam'],
    dayNamesMin: ['Di','Lu','Ma','Me','Je','Ve','Sa'],
    dayStatus: 'Utiliser DD comme premier jour de la semaine', dateStatus: 'Choisir le DD, MM d',
    dateFormat: 'dd/mm/yy', firstDay: 0, 
    initStatus: 'Choisir la date', isRTL: false
  };
  $.datepicker.setDefaults($.datepicker.regional['fr']);
  
  //offset to date 
  var pathArray = window.location.pathname.split( '/' );
  var date = new Date();
  if (! isNaN(pathArray[pathArray.length-1]) ){
    var offset = pathArray[pathArray.length-1];
    date.setDate(date.getDate() + (offset*7));
    //handle end of weeks
    if (date.getDay() > 5){
      date.setDate(date.getDate()+2);
    }
  }
  $('.week-picker').datepicker( "setDate", date );
  startDate = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay()-1);
  endDate = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay() + 5);
  
  selectCurrentWeek();
});

