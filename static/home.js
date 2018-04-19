function check_bid_form()
{
	var elements = document.forms['bid_form'].elements;
	var IZ_number = elements['IZ_number']; 
	console.log(IZ_number);
}

function add_citizen_IZ(event)
{
	var elements = document.forms['get_all_bids_form'].elements;
	var IZ_number = elements['IZ_number'].value;
	var req = new XMLHttpRequest();
	console.log(document.get_all_bids_form.action + '/'+IZ_number);
	req.open('GET', document.get_all_bids_form.action +'/'+IZ_number, true);
	req.onreadystatechange = function () 
	{
  		if(req.readyState === 4) 
  		{
    		console.log(req.responseText);
    	}
	}
	req.send();
}