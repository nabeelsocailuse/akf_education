frappe.pages["executive-dashboard"].on_page_load = function (wrapper) {
  var page = frappe.ui.make_app_page({
    parent: wrapper,
    title: "Executive Dashboard",
    single_column: true,
  });

  const content = frappe.render_template("executive_dashboard", {});
  $(content).appendTo(page.main);
  // On-Scroll Animation

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
};

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
  renderHighcharts();
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
        if (!series.icon) {
            series.icon = this.renderer
                .text(
                    `<i class="fa fa-${series.options.custom.icon}"></i>`,
                    0,
                    0,
                    true
                )
                .attr({
                    zIndex: 10
                })
                .css({
                    color: series.options.custom.iconColor,
                    fontSize: '1.5em'
                })
                .add(this.series[2].group);
        }
        series.icon.attr({
            x: this.chartWidth / 2 - 15,
            y: this.plotHeight / 2 -
                series.points[0].shapeArgs.innerR -
                (
                    series.points[0].shapeArgs.r -
                    series.points[0].shapeArgs.innerR
                ) / 2 +
                8
        });
    });
}

function renderHighcharts() {
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

  // Data for No. of Aghosh Homes (example data, update accordingly)
  const aghoshData = [
    [2006, 16],
    [2007, 3],  // Up
    [2008, 22],  // Down
    [2009, 6],  // Up
    [2010, 55],  // Down
    [2011, 11], // Up
    [2012, 19],  // Down
    [2013, 16], // Up
    [2014, 14], // Down
    [2015, 22], // Up
    [2016, 20], // Down
    [2017, 20], // Up
    [2018, 33], // Up
    [2019, 30], // Down
    [2020, 42], // Up
    [2021, 47], // Up
    [2022, 30], // Down
    [2023, 58], // Up
    [2024, 55]  // Down
];



Highcharts.chart("container-aghosh", {
    chart: { type: "areaspline" },
    title: { text: null },
    xAxis: {
        type: "category",
        title: { text: "Year" }
    },
    tooltip: {
        shared: false,
        crosshairs: false
    },
    plotOptions: {
        areaspline: {
            marker: {
                enabled: false,  // Hide markers by default
                radius: 0,       // Ensures markers are not visible initially
                states: {
                    hover: { 
                        enabled: true, 
                        radius: 5  // Show marker on hover with size 5
                    }
                }
            },
            lineWidth: 2,
            fillOpacity: 1
        }
    },
    yAxis: {
        title: { text: null }
    },
    series: [{
        name: "Aghosh Homes",
        data: aghoshData,
        color: "#007BFF",
        fillColor: {
            linearGradient: [0, 0, 0, 300],
            stops: [
                [0, "rgba(0, 123, 255, 0.8)"],  
                [0.4, "rgba(0, 123, 255, 0.4)"], 
                [0.7, "rgba(0, 123, 255, 0)"],  
            ]
        }
    }]
});


  Highcharts.chart("container-children", {
    chart: { 
        type: "areaspline" 
    },
    title: { 
        text: null
    },
    xAxis: {
        categories: [
            "2006", "2008", "2010", "2012", "2014", 
            "2016", "2018", "2020", "2022", "2024"
        ],
        title: { text: "Year" }
    },
    yAxis: {
        title: { text: null }
    },
    plotOptions: {
        areaspline: {
            marker: {
                enabled: false,  // Hide markers by default
                radius: 0,       // Ensures markers are not visible initially
                states: {
                    hover: { 
                        enabled: true, 
                        radius: 5  // Show marker on hover with size 5
                    }
                }
            },
            lineWidth: 2,
            fillOpacity: 1 // Ensure full control over gradient
        }
    },
    series: [{
        name: "Children",
        data: [50,  500,4200, 1200, 2300, 3500, 200, 4800, 5300, 6000],
        color: "#DC0505", // Changed to red
        fillColor: {
            linearGradient: [0, 0, 0, 300],
            stops: [
                [0, "rgba(220, 5, 5, 0.8)"],  // 80% opacity at the bottom
                [0.4, "rgba(220, 5, 5, 0.4)"], // 40% in the middle
                [0.7, "rgba(220, 5, 5, 0)"]   // 0% (completely transparent at the top)
            ]
        }
    }]
});


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
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: "pointer",
            dataLabels: {
                enabled: window.innerWidth > 700, // Disable labels on small screens
                format: "<b>{point.name}</b>: {point.y} ({point.percentage:.1f}%)",
                distance: 15, // Move labels slightly away from the pie
                style: {
                    textOutline: "none", // Remove text stroke
                    color: "#000" // Ensure text is visible
                }
            },
            showInLegend: window.innerWidth <= 600 // Show legend instead of labels on small screens
        }
    },
    series: [{
        name: "Children Count",
        colorByPoint: true,
        data: [
            { name: "Orphaned", y: 3000, color: "#FF5733" },
            { name: "In Shelter Homes", y: 2500, color: "#36A2EB" },
            { name: "Sponsored", y: 1800, color: "#28a745" },
            { name: "Unsponsored", y: 1200, color: "#dc3545" },
            { name: "Awaiting Adoption", y: 800, color: "#FFC107" }
        ]
    }]
});









const trackColors = Highcharts.getOptions().colors.map(color =>
    new Highcharts.Color(color).setOpacity(0.3).get()
);

Highcharts.chart('speedygauge', {
    chart: {
        type: 'solidgauge',
        height: Math.min(window.innerHeight * 0.5, 250), // 30% of viewport height but max 250px
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
            y: 80
        }],
    }, {
        name: 'Under <br> Construction',
        data: [{
            color: Highcharts.getOptions().colors[1],
            radius: '79%',
            innerRadius: '65%',
            y: 65
        }],
    }, {
        name: 'Planning',
        data: [{
            color: Highcharts.getOptions().colors[2],
            radius: '64%',
            innerRadius: '50%',
            y: 50
        }],
    }]
});





}
