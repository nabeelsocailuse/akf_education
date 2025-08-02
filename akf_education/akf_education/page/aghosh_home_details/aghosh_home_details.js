let filters = {};
frappe.pages['aghosh-home-details'].on_page_load = function (wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Aghosh Home Details',
		single_column: true
	});
	// serverCall.cards(page, {});
	// const route = frappe.get_route();
	filters.add(page);
};
filters = {
	add: function (page) {
		const flag = localStorage.getItem('flag');
		const aghosh_home = localStorage.getItem('aghosh_home_id');

		let aghosh_home_id = page.add_field({
			fieldname: "aghosh_home_id",
			label: __("Aghosh Homes"),
			fieldtype: "Link",
			options: "Aghosh Home",
			default: aghosh_home,
			reqd: 1,
			get_query: function () {
                return {
                    filters: {
                        status: "Operational"  // Only show operational homes
                    }
                };
            },
			change: (e) => {
				// fetchDashboardData(page);
				serverCall.cards(page, {'aghosh_home_id': aghosh_home_id.get_value()});
			},
		});
		
		if(flag=="yes"){
			// console.log(typeof(flag));
			// console.log(aghosh_home);
			serverCall.cards(page, {'aghosh_home_id': aghosh_home});
			localStorage.setItem('flag', 'no');
			localStorage.setItem('aghosh_home_id', '');
		}
		
	}
	
}

const serverCall = {
	cards: function (page, filters) {
		
		frappe.call({
			method: 'akf_education.akf_education.page.aghosh_home_details.aghosh_home_details.get_aghosh_home_dashboard',
			args: filters,
			callback: function (r) {
				let data = r.message;
				design.cards(page, data);
			}
		});
	}
};

const design = {
	cards: function (page, data) {
		$("#aghosh_dashboard").remove();
		const content = frappe.render_template("aghosh_home_details", data);
		const main = page.main;
		$(content).appendTo(main);

		// ⬅️ Call chart rendering after DOM is ready
		setTimeout(() => {
			renderHighcharts(data);
		}, 0);
	}
};

function renderHighcharts(data) {
	dashboard_title.innerHTML = data.aghosh_home_name;
	total_students_count.innerHTML = data.total_students || 0;
	total_beds_count.innerHTML = data.total_beds || 0;
	total_rooms_count.innerHTML = data.total_rooms || 0;
	sponsored_childrens_count.innerHTML = data.sponsored_childrens || 0;
	total_cameras_count.innerHTML = data.total_cameras || 0;
	active_cameras_count.innerHTML = data.active_cameras || 0;
	inactive_cameras_count.innerHTML = data.inactive_cameras || 0;
	disabled_student_count.innerHTML = data.disabled_students || 0;
	children_with_glasses_count.innerHTML = data.children_with_glasses || 0;
	permanent_staff_count.innerHTML = data.permanent_staff || 0;
	contract_staff_count.innerHTML = data.contract_staff || 0;
	intern_staff_count.innerHTML = data.intern_staff || 0;
	head_office_count.innerHTML = data.sponsorship_breakdown[0]['data'][0] || 0;
	local_sponsored_count.innerHTML = data.sponsorship_breakdown[0]['data'][1] || 0;
	regional_sponsored_count.innerHTML = data.sponsorship_breakdown[0]['data'][2] || 0;
	single_sponsored_count.innerHTML = data.sponsorship_breakdown[0]['data'][3] || 0;
	double_sponsored_count.innerHTML = data.sponsorship_breakdown[0]['data'][4] || 0;
	triple_sponsored_count.innerHTML = data.sponsorship_breakdown[0]['data'][5] || 0;
	overall_pass_rate.innerHTML = data.overall_pass_rate ? data.overall_pass_rate + '%' : '0%';
	average_score.innerHTML = data.average_score ? data.average_score : '0';
	// staff_distributionPie.innerHTML = data.staff_distribution_pie;

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
						format: '{point.class_group}: {point.y}',
						style: { fontSize: '13px' }
					}
				}
			},
			series: [{
				name: 'Students',
				colorByPoint: true,
				data: data.class_wise_summary
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
				categories: data.age_wise_summary.categories,
				crosshair: true
			},
			yAxis: { min: 0, title: { text: null } },
			tooltip: {
				shared: true,
				useHTML: true,
				headerFormat: '<b>{point.key}</b><br>',
				pointFormat: 'Students: <b>{point.y}</b>'
			},
			plotOptions: {
				column: { pointPadding: 0.2, borderWidth: 0, borderRadius: 4 }
			},
			series: [{
				name: 'Students by Age',
				data: data.age_wise_summary.y,
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
			xAxis: { categories: data.donor_wise_summary.categories },
			yAxis: { title: { text: null } },
			tooltip: { shared: true, valueSuffix: '' },
			plotOptions: {
				line: { marker: { enabled: true, radius: 5 } }
			},
			series: data.donor_wise_summary.series
		});
	}

	// Chart: Sponsorship Summary
	if (document.getElementById('sponsorshipChart')) {
		Highcharts.chart('sponsorshipChart', {
			chart: { type: 'column', backgroundColor: 'transparent' },
			title: {
				text: 'Children by Sponsorship Type',
				align: 'center',
				style: { fontWeight: 'bold', fontSize: '16px' }

			},
			exporting: { enabled: false },
			xAxis: {
				categories: ['Single Sponsored', 'Double Sponsored', 'Triple Sponsored', 'Head Office', 'Local Sponsored', 'Regional Sponsored'],
				labels: { rotation: -35 }
			},
			yAxis: { min: 0, title: { text: null } },
			tooltip: { pointFormat: 'Count: <b>{point.y}</b>' },
			plotOptions: { column: { borderRadius: 4 } },
			series: data.sponsorship_breakdown
		});
	}

	// Chart: Staff Distribution Pie
	if (document.getElementById('staff_distributionPie')) {
		Highcharts.chart('staff_distributionPie', {
			chart: { type: 'pie' },
			title: { text: '' },
			exporting: { enabled: false },
			series: [{
				name: 'Staff',
				colorByPoint: true,
				data: data.staff_distribution_pie
			}]
		});
	}

	// Chart: Staff by Department
	if (document.getElementById('staff_by_department')) {
		Highcharts.chart('staff_by_department', {
			chart: { type: 'column' },
			title: { text: '' },
			exporting: { enabled: false },
			xAxis: { categories: data.staff_by_department["categories"] },
			yAxis: { title: { text: '' } },
			series: [{
				name: 'Staff',
				data: data.staff_by_department["counts"],
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
				categories: data.performance.categories,
				tickmarkPlacement: 'on',
				title: { enabled: false }
			},
			yAxis: { title: { text: null }, labels: { format: '{value}' } },
			tooltip: { shared: true, valueSuffix: '' },
			credits: { enabled: false },
			plotOptions: { areaspline: { fillOpacity: 0.3 } },
			series: data.performance.series
		});
	}
}
