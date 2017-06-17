$(document).ready(function(){
		$(".optionDodajKlase").click(function(){
			$("#dodajKlaseModal").modal();
		});

		$(".optionDodajProfil").click(function(){
			$("#dodajProfilModal").modal();
		});

		$(".optionDodajUcznia").click(function(){
			$("#dodajUczniaModal").modal();
		});

		$(".optionDodajAlgorytm").click(function(){
			$("#dodajAlgorytmModal").modal();
		});

		$(".optionWypelnijKlase").click(function(){
			$("#wypelnijKlaseModal").modal();
		});

		$(".optionZrobKopie").click(function(){
			$("#zrobKopieModal").modal();
		});

		$( document ).ready(function(){
			$("#classIndexOF").modal();
		});

		$("#saferRemoveCopyButton").click(function(){
			result = 0;
			result = confirm("Jesteś pewny ?\nTa akcja bezpowrotnie usunie kopie zapasową.");
			if(result)
				$("#finalRemoveCopyButton").click();
			});

		$("#saferRestoreCopyButton").click(function(){
			result = 0;
			result = confirm("Jesteś pewny ?\n\nTa akcja bezpowrotnie przyróci kopie zapasową.\nPowrót do aktualnej nie bedzie już możliwy jeżeli jej stan nie został zapisany !");
			if(result)
				$("#finalRestoreCopyButton").click();
			});

		$("#btn-safe-delete-class-yes").click(function(){
			var elem = document.getElementById("btn-safe-delete-class-yes");
			klasa = elem.dataset.delete;
			window.location.replace("/sms/extended/delklasa/"+klasa);
		});

		$("#btn-safe-delete-class-no").click(function(){
			$(".close").click();
		});
		
	});

function saferDeleteClass(klasa){
	var elem = document.getElementById("paragraphSafeDeleteClass");
	elem.innerHTML = "Potwierdzenie tej akcji spowoduję bezpowrotne usunięcie klasy " + klasa;
	elem = document.getElementById("btn-safe-delete-class-yes");
	elem.dataset.delete = klasa;
	$("#saferDeleteClassModal").modal();
} 