/* Homepage registration UI. Verification is client-side; submission prepares an email draft. */
(function () {
  'use strict';
  var form = document.querySelector('[data-registration-form]');
  if (!form) return;
  var root = form.closest('.registration');
  var data = window.UWA_FORM_DATA || {campuses:{}};
  var cities = {
    'Andaman and Nicobar Islands':['Port Blair'], 'Andhra Pradesh':['Visakhapatnam','Vijayawada','Tirupati'],
    'Arunachal Pradesh':['Itanagar'], 'Assam':['Guwahati','Dibrugarh'], 'Bihar':['Patna','Gaya'],
    'Chandigarh':['Chandigarh'], 'Chhattisgarh':['Raipur','Bhilai'],
    'Dadra and Nagar Haveli and Daman and Diu':['Daman','Silvassa','Diu'], 'Delhi':['New Delhi','Delhi'],
    'Goa':['Panaji','Margao'], 'Gujarat':['Ahmedabad','Surat','Vadodara'], 'Haryana':['Gurugram','Faridabad'],
    'Himachal Pradesh':['Shimla','Dharamshala'], 'Jammu and Kashmir':['Jammu','Srinagar'],
    'Jharkhand':['Ranchi','Jamshedpur'], 'Karnataka':['Bengaluru','Mysuru','Mangaluru'],
    'Kerala':['Kochi','Thiruvananthapuram','Kozhikode'], 'Ladakh':['Leh','Kargil'],
    'Lakshadweep':['Kavaratti'], 'Madhya Pradesh':['Bhopal','Indore'],
    'Maharashtra':['Mumbai','Pune','Nagpur','Thane','Navi Mumbai'], 'Manipur':['Imphal'],
    'Meghalaya':['Shillong'], 'Mizoram':['Aizawl'], 'Nagaland':['Kohima','Dimapur'],
    'Odisha':['Bhubaneswar','Cuttack'], 'Puducherry':['Puducherry','Karaikal'],
    'Punjab':['Amritsar','Ludhiana','Jalandhar'], 'Rajasthan':['Jaipur','Jodhpur','Udaipur'],
    'Sikkim':['Gangtok'], 'Tamil Nadu':['Chennai','Coimbatore','Madurai','Tiruchirappalli'],
    'Telangana':['Hyderabad','Warangal'], 'Tripura':['Agartala'],
    'Uttar Pradesh':['Lucknow','Noida','Ghaziabad','Varanasi'], 'Uttarakhand':['Dehradun','Haridwar'],
    'West Bengal':['Kolkata','Howrah','Siliguri'], 'Outside India':[]
  };
  var state = form.elements.state, city = form.elements.city;
  var campus = form.elements.campus, program = form.elements.program, course = form.elements.course;
  function options(select, placeholder, values) {
    select.replaceChildren(new Option(placeholder,''));
    values.forEach(function (value) { select.add(new Option(value,value)); });
    select.disabled = !values.length;
  }
  options(state,'Select State',Object.keys(cities).sort());
  function otherCity() {
    var other = city.value === 'Other (please specify)';
    form.querySelector('[data-other-city]').hidden = !other;
    form.elements.otherCity.disabled = !other;
    form.elements.otherCity.required = other;
  }
  state.addEventListener('change',function () {
    options(city,state.value ? 'Select City' : 'Select State first',state.value ? cities[state.value].concat(['Other (please specify)']) : []);
    otherCity();
  });
  city.addEventListener('change',otherCity);
  campus.addEventListener('change',function () {
    options(program,campus.value ? 'Select Program' : 'Select Campus first',Object.keys(data.campuses[campus.value] || {}));
    options(course,'Select Program first',[]);
  });
  program.addEventListener('change',function () {
    var choices=(data.campuses[campus.value] || {})[program.value] || [];
    options(course,program.value ? 'Select Course' : 'Select Program first',choices);
  });
  function nameLabel() {
    var labels={Student:['Student Name','Enter student name'],'Parent/Guardian':['Parent/Guardian Name','Enter parent/guardian name'],Others:['Your Name','Enter your name']};
    var value=labels[form.elements.enquiringAs.value];
    form.querySelector('[data-registration-name-label]').textContent=value[0];
    form.elements.name.placeholder=value[1];
  }
  form.querySelectorAll('[name="enquiringAs"]').forEach(function (radio) { radio.addEventListener('change',nameLabel); });
  root.querySelectorAll('[data-audience]').forEach(function (tile) {
    tile.addEventListener('click',function () {
      root.querySelectorAll('[data-audience]').forEach(function (button) {button.setAttribute('aria-pressed',String(button===tile));});
      form.elements.audience.value=tile.dataset.audience;
      form.elements.enquiringAs.value=tile.dataset.audience.startsWith('Prospective') ? 'Student' : 'Others';
      nameLabel();
    });
  });
  var canvas=form.querySelector('[data-registration-captcha]'),context=canvas.getContext('2d'),code='';
  function refresh() {
    var characters='ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789';
    var random=new Uint32Array(6);window.crypto.getRandomValues(random);
    code=Array.from(random,function (value) {return characters[value%characters.length];}).join('');
    context.clearRect(0,0,canvas.width,canvas.height);context.fillStyle='#0032ff';context.font='italic 700 28px "TT Norms Pro", sans-serif';context.textBaseline='middle';
    for(var i=0;i<code.length;i++)context.fillText(code[i],4+i*25,23+(i%2 ? -2 : 2));
    context.strokeStyle='#0032ff';context.lineWidth=1;context.beginPath();context.moveTo(0,28);context.lineTo(170,16);context.stroke();
    canvas.setAttribute('aria-label','Verification code: '+code.split('').join(' '));
    form.elements.captcha.value='';form.elements.captcha.setCustomValidity('');
  }
  form.querySelector('[data-refresh-captcha]').addEventListener('click',refresh);
  form.elements.captcha.addEventListener('input',function () {this.setCustomValidity('');});
  form.elements.phone.addEventListener('input',function () {this.setCustomValidity('');});
  form.elements.countryCode.addEventListener('change',function () {form.elements.phone.setCustomValidity('');});
  if(document.fonts && document.fonts.ready)document.fonts.ready.then(refresh);else refresh();
  form.addEventListener('submit',function (event) {
    event.preventDefault();
    var digits=form.elements.phone.value.replace(/\D/g,'');
    var validPhone=form.elements.countryCode.value==='+91' ? digits.length===10 : digits.length>=6 && digits.length<=15;
    form.elements.phone.setCustomValidity(validPhone ? '' : (form.elements.countryCode.value==='+91' ? 'Enter a 10-digit mobile number.' : 'Enter a phone number with 6 to 15 digits.'));
    form.elements.captcha.setCustomValidity(form.elements.captcha.value.trim()===code ? '' : 'The verification code does not match. Please try again.');
    if(!form.reportValidity())return;
    var values=new FormData(form);
    var selectedCity=values.get('city')==='Other (please specify)' ? values.get('otherCity') : values.get('city');
    var message=['Enquiry type: '+values.get('audience'),'Enquiring as: '+values.get('enquiringAs'),'Name: '+values.get('name'),'Email: '+values.get('email'),'Mobile: '+(values.get('countryCode')==='Other' ? '' : values.get('countryCode')+' ')+values.get('phone'),'State: '+values.get('state'),'City: '+selectedCity,'Campus: '+values.get('campus'),'Program: '+values.get('program'),'Course: '+values.get('course'),'Intake: '+values.get('intake'),'','Message: '+(values.get('message') || 'Please contact me about studying at UWA India.')].join('\n');
    var subject='Register your interest — UWA India';
    form.querySelector('[data-registration-email]').href='mailto:info.uwaindia@uwa.edu.au?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(message);
    form.querySelector('[data-registration-draft-text]').value='To: info.uwaindia@uwa.edu.au\nSubject: '+subject+'\n\n'+message;
    form.querySelector('[data-registration-draft]').hidden=false;
    form.querySelector('.form-status').textContent='Your registration enquiry draft is ready. Open your email app and send it to complete your enquiry. Nothing has been submitted from this page.';
    form.querySelector('[data-registration-email]').focus();
  });
})();
