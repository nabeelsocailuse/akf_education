let filters = {};
frappe.pages['aghosh-home-details'].on_page_load = function (wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Aghosh Home Details',
		single_column: true
	});
	// serverCall.cards(page, {});
	filters.add(page);
};
filters = {
	add: function (page) {
		let branch = page.add_field({
			fieldname: "aghosh_home",
			label: __("Aghosh Homes"),
			fieldtype: "Link",
			options: "Aghosh Home",
			default: "",
			reqd: 1,
			change: (e) => {
				// fetchDashboardData(page);
				serverCall.cards(page, {});
			},
		});
	}
}

const serverCall = {
	cards: function (page, filters) {
		frappe.call({
			method: 'akf_education.akf_education.page.aghosh_home_details.aghosh_home_details.get_aghosh_home_dashboard',
			args: { filters: filters },
			callback: function (r) {
				let data = r.message;
				design.cards(page, data);
			}
		});
	}
};

const design = {
	cards: function (page, data) {
		$("#container-fluid").remove();
		const content = frappe.render_template("aghosh_home_details", data);
		const main = page.main;
		$(content).appendTo(main);

		// ⬅️ Call chart rendering after DOM is ready
		setTimeout(() => {
			renderHighcharts();
		}, 0);
	}
};

function renderHighcharts() {
	// frappe.call({
	//     method: "frappe.client.get_list",
	//     args: {
	//         doctype: "Aghosh Home",
	//         fields: ["name"],
	//         filters: {
	//             status: "Operational"
	//         },
	//         limit_page_length: 100
	//     },
	//     callback: function (r) {
	//         const dropdown = document.getElementById("aghosh-dropdown");
	//         dropdown.innerHTML = ""; // clear placeholder

	//         if (r.message.length === 0) {
	//             dropdown.innerHTML = `<a class="dropdown-item disabled">No Operational Homes</a>`;
	//             return;
	//         }

	//         r.message.forEach(home => {
	//             const item = document.createElement("a");
	//             item.className = "dropdown-item";
	//             item.href = `/app/aghosh-home/${home.name}`; // or use onclick to handle logic
	//             item.textContent = home.name;
	//             dropdown.appendChild(item);
	//         });
	//     }
	// });

	// frappe.call({
	//     method: "frappe.client.get_list",
	//     args: {
	//         doctype: "Aghosh Home",
	//         fields: ["name","aghosh_home_name"],
	//         filters: {
	//             status: "Operational"
	//         },
	//         limit_page_length: 100
	//     },
	//     callback: function (r) {
	//         const dropdown = document.getElementById("aghosh-list");
	//         dropdown.innerHTML = ""; // clear previous options

	//         if (!r.message || r.message.length === 0) {
	//             dropdown.innerHTML = `<li><a class="dropdown-item disabled">No Operational Homes</a></li>`;
	//             return;
	//         }

	//         r.message.forEach(home => {
	//             dropdown.innerHTML += `<li aria-selected="true">
	//               <a><p title="${home.name}"><strong>${home.name}</strong></p></a>
	//             </li>`;
	//         });
	//     }
	// });


	// Chart: Class-wise Summary
	if (document.getElementById('classChart')) {
		Highcharts.chart('classChart', {
			chart: { type: 'pie', backgroundColor: 'transparent' },
			title: { text: null },
			exporting: { enabled: false },
			tooltip: { pointFormat: '{series.name}: <b>{point.y}</b>' },
			plotOptions: {
				pie: {
					allowPointSelect: true,
					cursor: 'pointer',
					dataLabels: {
						enabled: true,
						format: '{point.name}: {point.y}',
						style: { fontSize: '13px' }
					}
				}
			},
			series: [{
				name: 'Students',
				colorByPoint: true,
				data: [
					{ name: 'Class 1-3', y: 85 },
					{ name: 'Class 4-6', y: 92 },
					{ name: 'Class 7-9', y: 78 },
					{ name: 'Class 10-12', y: 45 }
				]
			}]
		});

	}

	// Chart: Age-wise Summary
	if (document.getElementById('ageChart')) {
		Highcharts.chart('ageChart', {
			chart: { type: 'column', backgroundColor: 'transparent' },
			title: { text: null },
			exporting: { enabled: false },
			xAxis: {
				categories: ['5-8 years', '9-12 years', '13-16 years', '17-20 years'],
				crosshair: true
			},
			yAxis: { min: 0, title: { text: null } },
			tooltip: {
				shared: true,
				useHTML: true,
				headerFormat: '<b>{point.key}</b><br>',
				pointFormat: 'count: <b>{point.y}</b>'
			},
			plotOptions: {
				column: { pointPadding: 0.2, borderWidth: 0, borderRadius: 4 }
			},
			series: [{
				name: 'Children',
				data: [65, 98, 87, 40],
				color: '#f15b2a'
			}]
		});
	}

	// Chart: Donor-wise Summary
	if (document.getElementById('donorChart')) {
		Highcharts.chart('donorChart', {
			chart: { type: 'line', backgroundColor: 'transparent' },
			title: { text: null },
			exporting: { enabled: false },
			xAxis: { categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'] },
			yAxis: { title: { text: null } },
			tooltip: { shared: true, valueSuffix: '' },
			plotOptions: {
				line: { marker: { enabled: true, radius: 5 } }
			},
			series: [
				{ name: 'individual', data: [45, 52, 48, 55, 60, 65], color: '#1a5df0' },
				{ name: 'corporate', data: [22, 25, 29, 28, 32, 35], color: '#f68a0a' },
				{ name: 'government', data: [15, 18, 20, 23, 25, 27], color: '#d43f3a' }
			]
		});
	}

	// Chart: Sponsorship Summary
	if (document.getElementById('sponsorshipChart')) {
		Highcharts.chart('sponsorshipChart', {
			chart: { type: 'column', backgroundColor: 'transparent' },
			title: {
				text: 'Children by Sponsorship Type',
				align: 'left',
				style: { fontWeight: 'bold', fontSize: '16px' }

			},
			exporting: { enabled: false },
			xAxis: {
				categories: ['Head Office', 'Single Sponsored', 'Double Sponsored', 'Triple Sponsored', 'Local Sponsored', 'Regional Sponsored'],
				labels: { rotation: -35 }
			},
			yAxis: { min: 0, title: { text: null } },
			tooltip: { pointFormat: 'Count: <b>{point.y}</b>' },
			plotOptions: { column: { borderRadius: 4 } },
			series: [{
				name: 'Children',
				data: [45, 68, 52, 33, 74, 22],
				color: '#f39c12'
			}]
		});
	}

	// Chart: Staff Distribution Pie
	if (document.getElementById('pieChart')) {
		Highcharts.chart('pieChart', {
			chart: { type: 'pie' },
			title: { text: '' },
			exporting: { enabled: false },
			series: [{
				name: 'Staff',
				colorByPoint: true,
				data: [
					{ name: 'Permanent Staff', y: 28, color: '#f4a261' },
					{ name: 'Contractual Staff', y: 12, color: '#f4b261' },
					{ name: 'Interns', y: 5, color: '#f4c261' }
				]
			}]
		});
	}

	// Chart: Staff by Department
	if (document.getElementById('barChart')) {
		Highcharts.chart('barChart', {
			chart: { type: 'column' },
			title: { text: '' },
			exporting: { enabled: false },
			xAxis: { categories: ['Administration', 'Education', 'Healthcare', 'Maintenance'] },
			yAxis: { title: { text: '' } },
			series: [{
				name: 'Staff',
				data: [10, 15, 8, 7],
				color: '#f4a261',
				dataLabels: { enabled: true, color: '#333' }
			}]
		});
	}

	// Chart: Academic Performance
	if (document.getElementById('performanceChart')) {
		Highcharts.chart('performanceChart', {
			chart: { type: 'areaspline', backgroundColor: 'transparent' },
			title: { text: null },
			exporting: { enabled: false },
			xAxis: {
				categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
				tickmarkPlacement: 'on',
				title: { enabled: false }
			},
			yAxis: { title: { text: null }, labels: { format: '{value}' } },
			tooltip: { shared: true, valueSuffix: '' },
			credits: { enabled: false },
			plotOptions: { areaspline: { fillOpacity: 0.3 } },
			series: [
				{ name: 'avgScore', data: [78, 82, 81, 85, 87, 89], color: '#007bff' },
				{ name: 'passRate', data: [85, 86, 84, 88, 90, 91], color: '#28a745' },
				{ name: 'attendance', data: [92, 90, 95, 96, 97, 98], color: '#9b59b6' }
			]
		});
	}
}
