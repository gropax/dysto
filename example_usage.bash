if [ -d ./output ]; then
  rm -r ./output
fi

dysto data/estrep-694882.parsed_bonsai3_2_malt.conll \
      --token-limit 1000000 \
      --stopwords data/stopwords_fr.txt \
      --tags "V:50,NC:100" \
      --bag-of-words \
      --span 3 \
      --context-occurence 5 \
      --similarity cosine \
      --outdir output \

cat ./output/$(ls output | tail -n 1)/thesaurus_V | head -n 20
