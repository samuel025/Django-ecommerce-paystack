const searchField = document.querySelector("#searchField");
const productlist = document.querySelector(".product-list");
const tableOutput = document.querySelector(".output");
const pagination = document.querySelector(".pagination-container")
tableOutput.style.display = "none";

searchField.addEventListener('keyup',(e)=>{
	const searchValue = e.target.value;

	if (searchValue.trim().length>0) {
		pagination.style.display = "none";
		console.log("searchValue", searchValue);

		fetch("/search-products/", {
			body: JSON.stringify({ searchText: searchValue }),
			method: "POST",
		})
		 .then((res) => res.json())
		 .then((data) => {
		 	console.log("data", data);
		 	productlist.style.display = "none";
		 	tableOutput.style.display='block'

		 	if(data.length === 0) {
		 		tableOutput.innerHTML='No result found'
		 	}else{

		 		data.forEach(item => {
		 			tableOutput.innerHTML+=`
		 	<div class="row wow fadeIn">

	            <!--Grid column-->
	            
	            <div class="col-lg-3 col-md-6 mb-4">

	              <!--Card-->
	              <div class="card">

	                <!--Card image-->
	                <div class="view overlay">
	                  <img src="${item.image.url}" height="200" width="70" class="card-img-top"
	                    alt="">
	                  <a href="{{ item.get_absolute_url }}">
	                    <div class="mask rgba-white-slight"></div>
	                  </a>
	                </div>
	                <!--Card image-->

	                <!--Card content-->
	                <div class="card-body text-center">
	                  <!--Category & Title-->
	                  <a href="" class="grey-text">
	                    <h5>{{ item.get_category_display }}</h5>
	                  </a>
	                  <h5>
	                    <strong>
	                      <a href="{{ item.get_absolute_url }}" class="dark-grey-text">{{ item.title }}
	                        <span class="badge badge-pill {{ item.get_label_display }}-color">NEW</span>
	                      </a>
	                    </strong>
	                  </h5>

	                  <h4 class="font-weight-bold blue-text">
	                  
	                   <strong>
	                      ${item.price}
	                    
	                  </strong>
	                  </h4>

	                </div>
	                <!--Card content-->

	              </div>
	              <!--Card-->

	            </div>
	            <!--Grid column-->
	            {% endfor %}


	          </div>
	        </div>



		 		`
		 		})

		 		
		 	}
		 });


	}else {
		productlist.style.display = "block";
		pagination.style.display = "block";
		tableOutput.style.display='none'
	}
})