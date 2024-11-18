var animatePercentChange = function animatePercentChange (newPercent, elem) {
      elem = elem || $('#fu-percent span');
      const val = parseInt(elem.text(), 10);

      if(val !== parseInt(newPercent, 10)) {
          let diff = newPercent < val ? -1 : 1;
          elem.text(val + diff);
          setTimeout(animatePercentChange.bind(null, newPercent, elem), 5);
      }
}; 

function updateHumidity(newHum)
{
  const amount = Math.ceil(newHum || 25);
  const currentPercent = $('#fu-percent span').text();
  const waterAnimSpeed = (Math.abs(currentPercent - amount) / 50) * 10;
  const waterPercent = 100 - amount;
  animatePercentChange(amount);
  $('#water').css({
    top : waterPercent + '%'
  });
}

updateHumidity(90) //Sets the new value for humidity.