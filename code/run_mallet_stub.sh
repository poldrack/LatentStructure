BASE_DIR="/scratch/01329/poldrack/textmining/paper/topic_modeling/${LABEL}"
OUTPUT_DIR="$BASE_DIR/${LABEL}_lda_$NTOPICS"
ORIGDATA_DIR="/scratch/01329/poldrack/textmining/paper/fulltext_${LABEL}"

MALLETBIN='/scratch/01329/poldrack/textmining/mallet-2.0.6/bin'

if [ -f ${BASE_DIR}/${LABEL}_data.mallet ]; then
  echo "Using existing data file"
else
  ${MALLETBIN}/mallet import-dir --input $ORIGDATA_DIR --output ${BASE_DIR}/${LABEL}_data.mallet --keep-sequence --token-regex '[\p{L}\p{N}_]+|[\p{P}]+'
fi

mkdir $OUTPUT_DIR

${MALLETBIN}/mallet train-topics --input ${BASE_DIR}/${LABEL}_data.mallet --num-topics $NTOPICS --num-top-words 31 --output-topic-keys $OUTPUT_DIR/topic_keys.txt --output-doc-topics $OUTPUT_DIR/doc_topics.txt --topic-word-weights-file $OUTPUT_DIR/word_weights.txt --word-topic-counts-file $OUTPUT_DIR/word_topic_counts.txt --num-iterations 5000 --alpha $ALPHA


