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
            args: {
                // filters: filters
            },
            callback: function (r) {
                let data = r.message;
                design.cards(page, data);
                renderHighcharts(data);
            }
        })
    }
}

design = {
    cards: function (page, data) {
        $("#demopage_id").remove();
        const content = frappe.render_template("demopage", data);
        const main = page.main;
        $(content).appendTo(main);
    }
}

function load_on_scroll_animation(){
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
            $(window).trigger("scroll"); // Run once on page load
        });
    }, 500);
}
  
function add_necessary_css(){
    // Add necessary CSS
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

function load_scripts_sequentially(){
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
    renderPakistanMap();
    renderIcons();
}

function renderPakistanMap() {
    var mapContainer = document.getElementById("container-map");

    if (!mapContainer) {
    console.error("Map container not found!");
    return;
    }

    var map = L.map("container-map", {
    center: [30.3753, 69.3451], // Center Pakistan
    zoom: 6,
    scrollWheelZoom: false,
    });

    if (typeof L === "undefined") {
    console.error("Leaflet JS not loaded properly!");
    return;
    }

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors",
    maxZoom: 18,
    }).addTo(map);

    setTimeout(() => {
    map.invalidateSize();
    }, 500);

    var markers = L.markerClusterGroup();

    var locations = [
    { coords: [31.5204, 74.3587], name: "Lahore" },
    { coords: [33.6844, 73.0479], name: "Islamabad" },
    { coords: [24.8607, 67.0011], name: "Karachi" },
    { coords: [30.1575, 71.5249], name: "Multan" },
    { coords: [25.3969, 68.3578], name: "Hyderabad" },
    // { coords: [19.0760, 72.8777], name: "Mumbai"},
    // { coords: [40.730610,73.935242], name: "newYork"},
    ];

    locations.forEach((location) => {
    var customMarker = L.divIcon({
        className: "custom-marker",
        html: `<div class="marker-pin"></div><div class="marker-label">${location.name}</div>`,
        iconSize: [30, 42],
        iconAnchor: [15, 42],
    });

    markers.addLayer(L.marker(location.coords, { icon: customMarker }));
    });

    map.addLayer(markers);
}

// Run the function after DOM is loaded
window.onload = renderPakistanMap;

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

function renderHighcharts(data) {
    Highcharts.setOptions({
        navigation: {
            buttonOptions: {
                enabled: false  // Disable context menu
            }
        }
    });
    
    const aghoshContainer = document.getElementById("container-aghosh");
    if (!aghoshContainer) {
        console.error("Aghosh Homes chart container not found");
        return;
    }
    const chartData = data.charts_data;

    function children_statistics(){
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
    
    function aghosh_home_statuses(){
        const trackColors = Highcharts.getOptions().colors.map(color =>
            new Highcharts.Color(color).setOpacity(0.3).get()
        );


        let guage = chartData.aghosh_home_status;

        // Default values
        let operational = 0;
        let underConstruction = 0;
        let Inactive = 0;

        guage.forEach(item => {
            if (item.status === 'Operational') {
                operational = item.total;
            } else if (item.status === 'Under Construction') {
                underConstruction = item.total;
            } else if (item.status === 'Inactive') {
                Inactive = item.total;
            }
        });

        Highcharts.chart('speedygauge', {
            chart: {
                type: 'solidgauge',
                height: Math.min(window.innerHeight * 0.5, 250),
                spacing: [0, 0, 0, 0],
                events: {
                    render: renderIcons
                }
            },

            title: {
                text: null
            },

            tooltip: {
                borderWidth: 0,
                backgroundColor: 'none',
                shadow: false,
                style: {
                    fontSize: '14px',
                    textAlign: 'center'
                },
                valueSuffix: '%',
                pointFormat: '{series.name}<br>' +
                    '<span style="font-size: 2em; color: {point.color}; ' +
                    'font-weight: bold">{point.y}</span>',
                positioner: function (labelWidth) {
                    return {
                        x: (this.chart.chartWidth - labelWidth) / 2,
                        y: (this.chart.plotHeight / 3.5) + 12
                    };
                }
            },

            pane: {
                startAngle: 0,
                endAngle: 360,
                background: [{
                    outerRadius: '94%',
                    innerRadius: '80%',
                    backgroundColor: trackColors[0],
                    borderWidth: 0
                }, {
                    outerRadius: '79%',
                    innerRadius: '65%',
                    backgroundColor: trackColors[1],
                    borderWidth: 0
                }, {
                    outerRadius: '64%',
                    innerRadius: '50%',
                    backgroundColor: trackColors[2],
                    borderWidth: 0
                }]
            },

            yAxis: {
                min: 0,
                max: 100,
                lineWidth: 0,
                tickPositions: []
            },

            plotOptions: {
                solidgauge: {
                    dataLabels: {
                        enabled: false
                    },
                    linecap: 'round',
                    stickyTracking: false,
                    rounded: true
                }
            },

            series: [{
                name: 'Operational',
                data: [{
                    color: Highcharts.getOptions().colors[0],
                    radius: '94%',
                    innerRadius: '80%',
                    y: operational
                }],
            }, {
                name: 'Under <br> Construction',
                data: [{
                    color: Highcharts.getOptions().colors[1],
                    radius: '79%',
                    innerRadius: '65%',
                    y: underConstruction
                }],
            }, {
                name: 'Inactive',
                data: [{
                    color: Highcharts.getOptions().colors[2],
                    radius: '64%',
                    innerRadius: '50%',
                    y: Inactive
                }],
            }]
        });
    } 

    function aghosh_homes_per_week(){
        const ahic = chartData.aghosh_homes_interval_count;
        const areaspline = ahic.map(row => [ `Week ${row.Week_No}`, row.Total_Homes]);

        Highcharts.chart("container-aghosh", {
            chart: { type: "areaspline" },
            title: { text: "Aghosh Homes per Week" },
            xAxis: {
                type: "category",
                title: { text: "Week Number" }
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

    function childens_registrations(){
        let cregister = chartData.childens_registration;

        let weeks = cregister.map(row => "Week " + row.week_no);
        let totals = cregister.map(row => row.total_students);

        Highcharts.chart("container-children", {
            chart: { type: "areaspline" },
            title: { text: "Weekly Student Registrations" },
            xAxis: {
                categories: weeks,
                title: { text: "Week Number" }
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
        children_statistics()
    }, 10);
    setTimeout(() => {
        aghosh_home_statuses()
    }, 100);
    setTimeout(() => {
        aghosh_homes_per_week()
    }, 10);
    setTimeout(() => {
        childens_registrations()
    }, 10);
}


