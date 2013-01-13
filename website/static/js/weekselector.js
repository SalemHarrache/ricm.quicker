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
      var dateFormat = inst.settings.dateFormat || $.datepicker._defaults.dateFormat;
      $('#startDate').text($.datepicker.formatDate(dateFormat, startDate, inst.settings));
      $('#endDate').text($.datepicker.formatDate(dateFormat, endDate, inst.settings));

      var today = new Date();
      var weekno = today.getWeek();
      var offset = startDate.getWeek() - weekno;
      offset = offset - ((startDate.getYear() - today.getYear())*52);
      window.location = "/schedule/ricm5/reseau/"+offset;
      
      selectCurrentWeek();
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
  
  selectCurrentWeek();
});


$(document).ready(function(){
	
});
