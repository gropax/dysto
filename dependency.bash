if [ -d ./output ]; then
  rm -r ./output
fi

dysto data/estrep-694882.parsed_bonsai3_2_malt.conll \
      --token-limit 10000000 \
      --tags "V:500,NC:500,ADJ:500,ADV:200" \
      --dependency \
      --relations data/relations.txt \
      --context-occurence 3 \
      --similarity cosine \
      --outdir output \
      --test data/tests.txt \
      --verbose
      #--backup \
      #--stopwords data/stopwords_fr.txt \

cat ./output/$(ls output | tail -n 1)/contexts | head -n 20
