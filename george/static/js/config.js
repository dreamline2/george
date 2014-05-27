window._skel_config = {
	prefix: '/static/css/style',
	preloadStyleSheets: true,
	resetCSS: true,
	boxModel: 'border',
	grid: { gutters: 30 },
	breakpoints: {
		wide: { range: '1200-', containers: '90%', grid: { gutters: 0 } },
		narrow: { range: '961-1199', containers: 960 },
		narrower: { range: '481-960', containers: 'fluid', lockViewport: true, grid: { collapse: true, gutters: 0 }},
		mobile: { range: '-480', containers: 'fluid', lockViewport: true, grid: { collapse: true, gutters: 0 } }
	}
};

window._skel_panels_config = {
	panels: {
		rightPanel: {
			breakpoints: 'narrower,mobile',
			position: 'right',
			size: 250,
			html: '<div data-action="moveCell" data-args="right-sidebar,content"></div>'
		},
		bottomPanel: {
			position: 'bottom',
			size: 420
			/*
				Since this panel is a bit more complicated, we're omitting its 'html' option and
				defining it inline (ie. in index.html).
			*/
		}
	},
	overlays: {
		titleBar: {
			breakpoints: 'wide,narrow,narrower,mobile',
			position: 'top-center',
			width: '100%',
			height: 44,
			html: '<div data-action="copyHTML" data-args="title"></div>'
		},
		// contactBar: {
		// 	position: 'bottom-center',
		// 	width: '100%',
		// 	height: 60,
		// 	html:	'<a href="http://twitter.com/n33co" class="icon-twitter"></a>' +
		// 			'<a href="#" class="toggle icon-envelope" data-action="togglePanel" data-args="bottomPanel"></a>' +
		// 			'<a href="http://twitter.com/n33co" class="icon-facebook"></a>'
		// },
		rightPanelButton: {
			breakpoints: 'narrower,mobile',
			position: 'top-right',
			width: 80,
			height: 60,
			html: '<div class="toggle icon-reorder" data-action="togglePanel" data-args="rightPanel"></div>'
		}
	}
};