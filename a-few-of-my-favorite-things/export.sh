#!/bin/bash -eu

CDN="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.1.0"
jupyter \
	nbconvert A\ few\ of\ my\ favorite\ things.ipynb \
	--to slides \
	--SlidesExporter.reveal_url_prefix=$CDN
