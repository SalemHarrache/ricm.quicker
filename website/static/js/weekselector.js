$(function () {
  var startDate;
  var endDate;

  Date.prototype.getWeek = function () {
    var onejan = new Date(this.getFullYear(), 0, 1);
    return Math.ceil((((this - onejan) / 86400000) + onejan.getDay() + 1) / 7);
  }

  var selectCurrentWeek = function () {
    window.setTimeout(function () {
      $('.week-picker').find('.ui-datepicker-current-day a').addClass('ui-state-active')
    }, 1);
  }

  $('.week-picker').datepicker({
    showOtherMonths: true,
    selectOtherMonths: true,
    onSelect: function (dateText, inst) {
      var date = $(this).datepicker('getDate');
      startDate = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay());
      endDate = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay() + 6);
      
      var today = new Date();
      var weekno = today.getWeek();
      var offset = startDate.getWeek() - weekno;
      //handle year change
      var yeardiff =  today.getYear() - startDate.getYear();
      if (yeardiff != 0) {
        offset = offset - (52*yeardiff);
      }

			//create new path
      var pathArray = window.location.pathname.split( '/' );
      var newPathname = "";
      for ( i = 0; i<pathArray.length-1; i++ ) {
	      newPathname += pathArray[i];
	      newPathname += "/";
      }
      if ( isNaN(pathArray[pathArray.length-1]) ){
	      newPathname += pathArray[pathArray.length-1];
	      newPathname += "/";
      }
      selectCurrentWeek();
      
      window.location = newPathname+offset;
    },
    beforeShowDay: function (date) {
      var cssClass = '';
      if (date >= startDate && date <= endDate) cssClass = 'ui-datepicker-current-day';
      return [true, cssClass];
    },
    onChangeMonthYear: function (year, month, inst) {
      selectCurrentWeek();
    }
  });

  $('.week-picker .ui-datepicker-calendar tr').live('mousemove', function () {
    $(this).find('td a').addClass('ui-state-hover');
  });
  $('.week-picker .ui-datepicker-calendar tr').live('mouseleave', function () {
    $(this).find('td a').removeClass('ui-state-hover');
  });
  
  //offset to date 
  var pathArray = window.location.pathname.split( '/' );
  var date = new Date();
  if (! isNaN(pathArray[pathArray.length-1]) ){
    var offset = pathArray[pathArray.length-1];
    date.setDate(date.getDate() + (offset*7));
  }
  
  startDate = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay());
  endDate = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay() + 6);
  $('.week-picker').datepicker( "setDate", date );
  selectCurrentWeek();
});


