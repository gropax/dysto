dysto data/estrep-694882.parsed_bonsai3_2_malt.conll \
      --token-limit 1000000 \
      --stopwords data/stopwords_fr.txt \
      --tags "V:500,NC:1000" \
      --bag-of-words \
      --span 5 \
      --context-occurence 2 \
      --similarity cosine \
      --outdir output \
      --verbose
