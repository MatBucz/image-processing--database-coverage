run:
	docker-compose up

montage:
	montage  -geometry +1+1 -tile 2x2 output/*_delaunay.png output/delaunay_montage.png
	montage  -geometry +1+1 -tile 2x2 output/*_si_cf_plane.png output/si_cf_plane_montage.png
	montage  -geometry +1+1 -tile 2x2 output/*_convex_hull.png output/convex_hull_montage.png

clean:
	rm -rf output/*.png