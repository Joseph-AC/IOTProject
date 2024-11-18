var animateValue = function animateValue (newPercent, elem) {
  elem = elem || $('#gauge__cover');
  const val = parseInt(elem.text(), 10);
  //console.log('Updating...' + val + '|' + parseInt(newPercent, 10));
  if(val !== parseInt(newPercent, 10)) {
      let diff = newPercent < val ? -1 : 1;
      elem.text(val + diff);
      setTimeout(animateValue.bind(null, newPercent, elem), 5);
  }
}; 

function setGaugeValue(value) {
  if (value < 0 || value > 1) {
    return;
  }

  $('#gauge__fill').css('transform', `rotate(${ value / 2 }turn)`);
  let newTemp = Math.round(value * 100);
  animateValue(newTemp)

  if (value < 0.5) {
    document.querySelector("#gauge__fill").style.backgroundColor = 'blue';
  } else {
    document.querySelector("#gauge__fill").style.backgroundColor = 'red';
  }

}

setGaugeValue(0.87); //To set the value of the temperature
