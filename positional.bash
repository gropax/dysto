dysto data/estrep-694882.parsed_bonsai3_2_malt.conll \
      --token-limit 100000000 \
      --stopwords data/stopwords_fr.txt \
      --tags "V:500,NC:1000" \
      --positional \
      --span 4 \
      --context-occurence 4 \
      --similarity cosine \
      --outdir output \
      --verbose

#cat ./output/$(ls output | tail -n 1)/thesaurus_V | head -n 20
