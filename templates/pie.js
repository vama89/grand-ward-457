<script>
					var height = 400,
						width = 600,
						radius = 200,
						colors = d3.scale.category20c();

					var piedata = {{allocation}}

					var pie = d3.layout.pie()
						.value(function(d) {
							return d.value;
						})

					var arc = d3.svg.arc()
						.outerRadius(radius)

					var myChart = d3.select('#chart').append('svg')
						.attr('width', width)
						.attr('height', height)
						.append('g')
						.attr('transform', 'translate('+(width-radius)+' , '+(height-radius)+')')
						.selectAll('path').data(pie(piedata))
						.enter().append('g')
							.attr('class', 'slice')

					var slices = d3.selectAll('g.slice')
						.append('path')
								.attr('fill', function(d, i) {
									return colors(i);
								})
								.attr('d', arc)

					var text = d3.selectAll('g.slice')
						.append('text')
						.text(function(d, i) {
							return d.data.label;
						})
						.attr('text-anchor', 'middle')
						.attr('fill', 'white')
						.attr('transform', function(d) {
							d.innerRadius = 0;
							d.outerRadius = radius;
							return 'translate('+ arc.centroid(d)+')'
						})

				</script>