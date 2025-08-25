const apiPath = "akf_education.akf_education.page.executive_dashboard.executive_dashboard";
frappe.pages["executive-dashboard"].on_page_load = function (wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: "Executive Dashboard",
        single_column: true,
    });
    // const content = frappe.render_template("demopage", {});
    // $(content).appendTo(page.main);
    load_scripts_sequentially();
    serverCall.cards(page, {})
    // // On-Scroll Animation
    load_on_scroll_animation();
    add_necessary_css();

};

serverCall = {
    cards: function (page, filters) {
        frappe.call({
            method: `${apiPath}.get_executive_dashboard`,
            args: {},
            callback: function (r) {
                console.log("API response:", r.message);

                let data = r.message;
                design.cards(page, data);
                renderHighcharts(data);
                renderPakistanMap(data);
                APRs(data);
            }
        })
    }
}


design = {
    cards: function (page, data) {
        $("#demopage_id").remove();
        const content = frappe.render_template("executive_dashboard", data);
        const main = page.main;
        $(content).appendTo(main);
    }
}

function load_on_scroll_animation() {
    // On-Scroll Animation
    setTimeout(() => {
        jQuery(function ($) {
            var doAnimations = function () {
                var windowHeight = $(window).height(),
                    scrollTop = $(window).scrollTop(),
                    $animatables = $(".fade-up:not(.show)"),
                    $animatablesBounce = $(".bounce:not(.show)");

                if ($animatables.length === 0 && $animatablesBounce.length === 0) {
                    $(window).off("scroll", doAnimations); // Stop listening when all elements are animated
                    return;
                }

                $animatables.each(function () {
                    var $animatable = $(this);
                    var elementTop = $animatable.offset().top;
                    var elementBottom = elementTop + $animatable.outerHeight();

                    if (elementBottom > scrollTop && elementTop < scrollTop + windowHeight) {
                        $animatable.addClass("show");
                    }
                });

                $animatablesBounce.each(function () {
                    var $animatableBounce = $(this);
                    var elementTop = $animatableBounce.offset().top;
                    var elementBottom = elementTop + $animatableBounce.outerHeight();

                    if (elementBottom > scrollTop && elementTop < scrollTop + windowHeight) {
                        $animatableBounce.addClass("show");
                    }
                });
            };

            $(window).on("scroll", doAnimations);
            $(window).trigger("scroll");
        });
    }, 500);
}

function add_necessary_css() {
    $("<style>")
        .prop("type", "text/css")
        .html(
            `
              .highcharts-figure, .highcharts-data-table table {
                  min-width: 310px; 
                  max-width: 800px;
                  margin: 1em auto;
              }
              #container {
                  height: 400px;
                  width: 100%;
                  min-width: 310px;
              }
          `
        )
        .appendTo("head");
}

function load_scripts_sequentially() {
    // Clear any previous Highcharts instance
    if (window.Highcharts) {
        delete window.Highcharts;
    }

    // Use vanilla JavaScript to load scripts sequentially
    loadScriptPromise("https://code.highcharts.com/highcharts.js")
        .then(() =>
            loadScriptPromise("https://code.highcharts.com/highcharts-more.js")
        )
        .then(() =>
            loadScriptPromise("https://code.highcharts.com/modules/solid-gauge.js")
        )
        .then(() =>
            loadScriptPromise("https://code.highcharts.com/modules/bullet.js")
        )
        .then(() =>
            loadScriptPromise("https://code.highcharts.com/maps/highmaps.js")
        )
        .then(() =>
            loadScriptPromise("https://code.highcharts.com/maps/modules/exporting.js")
        )
        .then(() =>
            loadScriptPromise(
                "https://code.highcharts.com/maps/modules/offline-exporting.js"
            )
        )
        .then(() =>
            loadScriptPromise("https://code.highcharts.com/modules/exporting.js")
        )
        .then(() =>
            loadScriptPromise("https://code.highcharts.com/modules/export-data.js")
        )
        .then(() =>
            loadScriptPromise("https://code.highcharts.com/modules/accessibility.js")
        )
        .then(() =>
            loadScriptPromise("https://unpkg.com/leaflet@1.7.1/dist/leaflet.js")
        )
        .then(() =>
            loadScriptPromise(
                "https://unpkg.com/leaflet.markercluster@1.4.1/dist/leaflet.markercluster.js"
            )
        )

        .then(() => {
            // Add a slight delay to ensure everything is registered
            setTimeout(() => {
                if (
                    typeof Highcharts !== "undefined" &&
                    Highcharts.seriesTypes &&
                    Highcharts.seriesTypes.solidgauge
                ) {
                    renderCharts();
                } else {
                    console.error(
                        "Highcharts or solidgauge module not properly loaded",
                        typeof Highcharts,
                        Highcharts?.seriesTypes?.solidgauge
                    );
                }
            }, 300);
        })
        .catch((error) => {
            console.error("Script loading failed:", error);
        });
}

// Helper function to load scripts as promises
function loadScriptPromise(src) {
    return new Promise((resolve, reject) => {
        const script = document.createElement("script");
        script.src = src;
        script.async = false; // Important to maintain loading order
        script.onload = () => {
            resolve();
        };
        script.onerror = () => reject(new Error(`Failed to load script ${src}`));
        document.head.appendChild(script);
    });
}

function renderCharts() {
    // Render all charts
    renderIcons();
}

function renderPakistanMap(data) {
    const mapContainer = document.getElementById("container-map");
    if (!mapContainer) return console.error("Map container not found!");

    if (typeof L === "undefined") return console.error("Leaflet JS not loaded!");

    const map = L.map("container-map", {
        center: [30.3753, 69.3451],
        zoom: 6,
        scrollWheelZoom: false,
    });

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors",
        maxZoom: 18,
    }).addTo(map);

    setTimeout(() => map.invalidateSize(), 500);

    const markers = L.markerClusterGroup();

    const iconColors = {
        "Operational": "green",
        "Under Construction": "yellow",
        "Inactive": "red"
    };

    const getMarkerIcon = (status) =>
        new L.Icon({
            iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-${iconColors[status] || "grey"}.png`,
            shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41]
        });

    // Group locations by lat,lng
    const groupedHomes = {};
    data.aghosh_home_locations.forEach(loc => {
        const key = `${loc.coords[0]},${loc.coords[1]}`;
        groupedHomes[key] = groupedHomes[key] || [];
        groupedHomes[key].push(loc);
    });

    Object.values(groupedHomes).forEach(locations => {
        const { coords } = locations[0];
        const icon = getMarkerIcon(locations[0].status);

        let tooltipContent;

        if (locations.length > 1) {
            tooltipContent = `
                <div class="custom-tooltip-card">
                    <h4>${locations.length} Aghosh Homes</h4>
                    <ul class="aghosh-list">
                        ${locations.map(l => `<li><strong>${l.name}</strong> <small>(${l.status})</small></li>`).join("")}
                    </ul>
                </div>
            `;
        } else {
            const loc = locations[0];
            tooltipContent = `
                <div class="custom-tooltip-card">
                    <h4>${loc.name}</h4>
                    <p>Status: ${loc.status}</p>
                </div>
            `;
        }

        const marker = L.marker(coords, { icon });
        marker.bindTooltip(tooltipContent, {
            permanent: false,
            direction: "top",
            opacity: 0.95,
            sticky: true,
            className: "leaflet-tooltip-card",
        });

        markers.addLayer(marker);
    });

    map.addLayer(markers);
}


// renderPakistanMap();

function renderIcons() {
    this.series.forEach(series => {
        if (!series.options.custom || !series.options.custom.icon) return;

        if (!series.icon) {
            series.icon = this.renderer
                .text(
                    '<i class="fa fa-' + series.options.custom.icon + '"></i>',
                    0,
                    0,
                    true
                )
                .attr({
                    zIndex: 10
                })
                .css({
                    color: series.options.custom.iconColor || "#000",
                    fontSize: '1.5em'
                })
                .add(series.group || this.series[0].group); // safe fallback
        }

        const point = series.points[0];
        if (point && point.shapeArgs) {
            const { innerR, r } = point.shapeArgs;
            series.icon.attr({
                x: this.chartWidth / 2 - 15,
                y: this.plotHeight / 2 - innerR - (r - innerR) / 2 + 8
            });
        }
    });
}
function APRs(data) {
    if (!data || !data.charts_data || !data.charts_data.aprs_data) {
        console.error("No APRs data available in API response!");
        return;
    }

    const aprsData = data.charts_data.aprs_data;


    const categories = aprsData.map(item => item.academic_year);


    const enrolledStudents = aprsData.map(item => item.total_enrolled_students);
    const finalTermResults = aprsData.map(item => item.total_final_term_results_submitted);

    Highcharts.chart('container_aghosh2', {
        chart: {
            type: 'column'
        },

        title: {
            text: 'Academic Year-wise Enrollment & Final Term Results',
            align: 'left'
        },

        xAxis: {
            categories: categories,
            title: {
                text: 'Academic Year'
            }
        },

        yAxis: {
            allowDecimals: false,
            min: 0,
            title: {
                text: 'Number of Students'
            },
            stackLabels: {
                enabled: true
            }
        },

        tooltip: {
            shared: true,
            pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b><br/>'
        },

        plotOptions: {
            column: {
                stacking: 'normal',
                dataLabels: {
                    enabled: true
                }
            }
        },

        series: [
            {
                name: 'Enrolled Students',
                data: enrolledStudents,
                color: '#007BFF'
            },
            {
                name: 'Final Term Results Submitted',
                data: finalTermResults,
                color: '#28a745'
            }
        ]
    });
}

function renderHighcharts(data) {
    // Highcharts.setOptions({
    //     navigation: {
    //         buttonOptions: {
    //             enabled: false  // Disable context menu
    //         }
    //     }
    // });

    const aghoshContainer = document.getElementById("container-aghosh");
    if (!aghoshContainer) {
        console.error("Aghosh Homes chart container not found");
        return;
    }
    const chartData = data.charts_data;

    function children_statistics() {
        // Aghosh Homes Chart
        Highcharts.chart("children-statistics", {
            chart: {
                type: "pie"
            },
            title: {
                text: null
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.y}</b>({point.percentage:.2f}%)'
            },
            exporting: {
                enabled: false
            },
            credits: {
                enabled: false
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: "pointer",
                    borderWidth: 2,
                    animation: { duration: 2000 }, // Apply animation
                    dataLabels: {
                        enabled: window.innerWidth > 700, // Disable labels on small screens
                        format: '<b>{point.name}</b>: {point.y} ({point.percentage:.1f}%)',
                        distance: 20, // Move labels slightly away from the pie
                        style: {
                            textOutline: "none", // Remove text stroke
                            color: "#000" // Ensure text is visible
                        }
                    },
                    showInLegend: window.innerWidth <= 600 // Show legend instead of labels on small screens
                }
            },
            series: [{
                colorByPoint: true,
                data: [
                    { name: "Orphaned", y: data.total_students },
                    { name: "In Shelter Homes", y: data.students_in_shilter },
                    { name: "Sponsored", y: data.sponsored_childrens },
                    { name: "Unsponsored", y: data.total_students - data.sponsored_childrens }
                ]
            }]
        });
    }

    function aghosh_home_statuses() {
        let guage = chartData.aghosh_home_status;

        // Default values
        let operational = 0;
        let underConstruction = 0;
        let inactive = 0;

        guage.forEach(item => {
            if (item.status === 'Operational') {
                operational = item.total;
            } else if (item.status === 'Under Construction') {
                underConstruction = item.total;
            } else if (item.status === 'Inactive') {
                inactive = item.total;
            }
        });

        Highcharts.chart('speedygauge', {
            chart: {
                type: 'pie',
                height: Math.min(window.innerHeight * 0.5, 300),
            },

            title: {
                text: null
            },

            tooltip: {
                pointFormat: '<b>{point.percentage:.1f}%</b> ({point.y})'
            },

            plotOptions: {
                pie: {
                    innerSize: '60%',
                    depth: 45,
                    dataLabels: {
                        enabled: true,
                        format: '{point.name}: {point.y}',
                        distance: 8,
                        style: {
                            fontSize: '13px'
                        }
                    }
                }
            },

            series: [{
                name: 'Homes',
                colorByPoint: true,
                data: [{
                    name: 'Operational',
                    y: operational,
                    color: Highcharts.getOptions().colors[0]
                }, {
                    name: 'Under Construction',
                    y: underConstruction,
                    color: Highcharts.getOptions().colors[1]
                }, {
                    name: 'Inactive',
                    y: inactive,
                    color: Highcharts.getOptions().colors[2]
                }]
            }]
        });
    }


    function aghosh_homes_per_week() {
        const ahic = chartData.aghosh_homes_interval_count;
        const areaspline = ahic.map(row => [`Year ${row.Year}`, row.aghosh_home]);

        Highcharts.chart("container-aghosh", {
            chart: { type: "areaspline" },
            title: { text: "Aghosh Homes per Year" },
            xAxis: {
                type: "category",
                title: { text: "Year" }
            },
            yAxis: {
                title: { text: "Total Homes Established" }
            },
            tooltip: {
                shared: false,
                crosshairs: false
            },
            plotOptions: {
                areaspline: {
                    marker: {
                        enabled: false,
                        radius: 0,
                        states: {
                            hover: {
                                enabled: true,
                                radius: 5
                            }
                        }
                    },
                    lineWidth: 2,
                    fillOpacity: 1
                }
            },
            series: [{
                name: "Aghosh Homes",
                data: areaspline,
                color: "#007BFF",
                fillColor: {
                    linearGradient: [0, 0, 0, 300],
                    stops: [
                        [0, "rgba(0, 123, 255, 0.8)"],
                        [0.4, "rgba(0, 123, 255, 0.4)"],
                        [0.7, "rgba(0, 123, 255, 0)"]
                    ]
                }
            }]
        });
    }
    //      function fetchOperationalAghoshHomes() {
    //     frappe.call({
    //       method: "akf_education.akf_education.page.executive_dashboard.executive_dashboard.get_operational_aghosh_homes",
    //       callback: function (r) {
    //         console.log("Operational Aghosh Homes:", r.message);
    //       },
    //       error: function (err) {
    //         console.error("Error fetching operational homes", err);
    //       }
    //     });
    //   }
    function childens_registrations() {
        let cregister = chartData.childens_registration;

        let years = cregister.map(row => row.Year);
        let totals = cregister.map(row => row.student_count);

        Highcharts.chart("container-children", {
            chart: { type: "areaspline" },
            title: { text: null },
            xAxis: {
                categories: years,
                title: { text: "Year" }
            },
            yAxis: {
                title: { text: "Total Students" }
            },
            plotOptions: {
                areaspline: {
                    marker: {
                        enabled: false,
                        radius: 0,
                        states: {
                            hover: {
                                enabled: true,
                                radius: 5
                            }
                        }
                    },
                    lineWidth: 2,
                    fillOpacity: 1
                }
            },
            series: [{
                name: "Students",
                data: totals,
                color: "#28a745",
                fillColor: {
                    linearGradient: [0, 0, 0, 300],
                    stops: [
                        [0, "rgba(40, 167, 69, 0.8)"],
                        [0.4, "rgba(40, 167, 69, 0.4)"],
                        [0.7, "rgba(40, 167, 69, 0)"]
                    ]
                }
            }]
        });
    }




    setTimeout(() => {
        children_statistics(),
            aghosh_home_statuses(),
            aghosh_homes_per_week(),
            childens_registrations(),
            APRs(data)
    }, 500)

}

// window.onload = renderPakistanMap;

window.fetchHomes = function ({ method, title, indicator }) {
    frappe.call({
        method: method,
        callback: function (r) {
            const data = r.message || [];

            if (data.length === 0) {
                frappe.msgprint(`No ${title} found.`);
                return;
            }

            //   const htmlList = `
            //     <div style="padding-left: 0.5rem;">
            //       <ul style="padding-left: 1.2rem; margin: 0; list-style-type: disc;">
            //         ${data.map(item => `<li><a href="/app/aghosh-home-details?aghosh_home_id=${item.name}" onclick="
            //              frappe.route_options = { aghosh_home_id: '${item.name}' };
            //              frappe.set_route('app/aghosh-home-details');
            //            ">${item.aghosh_home_name}</a></li>`).join("")}
            //       </ul>
            //     </div>
            //   `;
            const htmlList = `
        <div style="padding-left: 0.5rem;">
          <ul style="padding-left: 1.2rem; margin: 0; list-style-type: disc;">
            ${data.map(item => `<li><a href="/app/aghosh-home-details" onclick='openAghoshHomeDetails("${item.name}")'>${item.aghosh_home_name}</a></li>`).join("")}
          </ul>
        </div>
      `;

            frappe.msgprint({
                title: title,
                message: htmlList,
                indicator: indicator,
            });
        },
    });
};

function openAghoshHomeDetails(aghosh_home_id) {
    // frappe.set_route('aghosh-home-details');
    localStorage.setItem('flag', "yes");
    localStorage.setItem('aghosh_home_id', aghosh_home_id);
}

//operational
window.showOperationalHomes = function () {
    fetchHomes({
        method: "akf_education.akf_education.page.executive_dashboard.executive_dashboard.get_operational_aghosh_homes",
        title: "Operational Aghosh Homes",
        indicator: "green",
    });
};

//under construction
window.fetchUnderCounstructionHome = function () {
    fetchHomes({
        method: "akf_education.akf_education.page.executive_dashboard.executive_dashboard.get_underCounstruction",
        title: "Under Construction Aghosh Homes",
        indicator: "blue",
    });
};

//inactive
window.fetchInactiveHomes = function () {
    fetchHomes({
        method: "akf_education.akf_education.page.executive_dashboard.executive_dashboard.get_inactive_homes",
        title: "Inactive Aghosh Homes",
        indicator: "red",
    });
};
