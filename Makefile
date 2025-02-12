artifact:
	git tag -d $(VERSION) || true
	git tag -a $(VERSION) -m ""
	git push origin master --tags

generateHD:
	manim -pqh $(FILE) $(CLASS)

generateSD:
	manim -pq $(FILE) $(CLASS)

conda:
	conda activate fenwick_manim
	cd lib/fenwick_manim && maturin develop && cd ../..
