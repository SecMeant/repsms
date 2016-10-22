																			<!--Skrypcik kopiujacy formularz-->
							function copyForm(x) {
								if(x.checked){
									  var text = document.getElementById("ulica").value;
									  document.getElementById("ulica2").value = text;
									  
									  text = document.getElementById("nr_dom").value;
									  document.getElementById("nr_dom2").value = text;
									  
									  text = document.getElementById("kod_p1").value;
									  document.getElementById("kod_p12").value = text;
									  
									  text = document.getElementById("kod_p2").value;
									  document.getElementById("kod_p22").value = text;
									  
									  text = document.getElementById("Miejscowosc").value;
									  document.getElementById("Miejscowosc2").value = text;
									  }
								else{
									  text='';
									  document.getElementById("ulica2").value = text;
									  document.getElementById("nr_dom2").value = text;
									  document.getElementById("kod_p12").value = text;
									  document.getElementById("kod_p22").value = text;
									  document.getElementById("Miejscowosc2").value = text;
									  }
								}

							function show_criterias(x,kryt){
								if(x.checked){
								document.getElementById(kryt).style.display='block';

								}else{
								document.getElementById(kryt).style.display='none';

								}
							}
