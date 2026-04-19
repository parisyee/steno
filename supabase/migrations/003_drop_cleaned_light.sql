-- Drop the "light" cleanup variant and flatten the remaining "polished"
-- variant into its own nullable text column. Polished is now opt-in per
-- upload, so NULL means the user did not request it.

alter table transcriptions add column cleaned_polished text;

update transcriptions
set cleaned_polished = cleaned->>'polished'
where cleaned is not null;

alter table transcriptions drop column cleaned;
