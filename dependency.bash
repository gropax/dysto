dysto data/estrep-694882.parsed_bonsai3_2_malt.conll \
      --token-limit 100000000 \
      --tags "V:500,NC:1000" \
      --dependency \
      --context-occurence 3 \
      --similarity cosine \
      --outdir output \
      --verbose
      #--backup \
      #--relations data/relations.txt \
      #--stopwords data/stopwords_fr.txt \
