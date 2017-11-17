trim: $(patsubst data/%_aligned.fasta, data/%_paml.fasta, \
	$(wildcard data/*_aligned.fasta))

data/%_cleaned.fasta: data/%_aligned.fasta data/wanted_species.txt
	cd data/ ; python ../scripts/1_paml_cleaner.py $(notdir $^)

data/%_cleaned_aligned.fasta: data/%_cleaned.fasta
	cd data/ ; muscle -in $(notdir $^) -out $(notdir $@)

data/%_paml.fasta: data/%_cleaned_aligned.fasta
	cd data/ ; trimal -in $(notdir $^) -out $(notdir $@) -gappyout

.PHONY: trim
