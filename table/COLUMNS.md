# The current table: files and columns

`table/make_register.py` writes `register.csv`, `cells.csv`, `claims.csv` and `CURRENT.md`, and
`table/check_register.py` checks them. Their inputs are the closed records of phase 1 and phase 2, pinned by SHA-256 in
`closed_inputs.csv`, and one open file, `intake.csv`.
The intake holds the items in flight at phase 2's close and everything received or found since, each in its own row. The third-party files and claims that phase 2 recorded only in its notes, search records or
check logs stay there, and each is entered when its file has been fetched at a fixed address and checked here.
The rules are in `registration/REGISTRATION_intake.md`. The closed records are never rewritten. Their own labels are kept in the
columns `status_4_nov`, `label_phase2` and `label_in_phase`, with the meaning their registration gives them.

## register.csv: one row per file (claims with no file are in claims.csv)

| column | meaning |
|---|---|
| witness_id | `p1:` phase-1 ledger id, `p2:` phase-2 file name, `in:` intake id |
| cell | the Ramsey number's parameters, sorted |
| colors | number of colors |
| n | vertices of the file, as recorded (blank where no record gives it) |
| n_measured_here | vertices counted from the stored file by `make_register.py`, for phase-2 and intake rows. Blank for phase-1 rows, whose n was measured by the phase-1 run (`results/ledger.csv`), and for linked files |
| bound_from_witness | n + 1, the lower bound the file gives if it is a witness. Only rows whose `checks` is a passing value and whose `decision` is accepted count as witnesses |
| claimed_bound | the bound its source claims (intake rows) |
| origin | third party: public file, third party: sent by the author, third party: printed, transcribed here, built here from a published construction, or found here by search |
| file_credit | who made or published the file |
| public_date | the earliest dated public posting of the file (repository commit, Zenodo record, paper version), where recorded |
| construction_credit | the graphs or colorings the file was built from, and their authors |
| bound_credit | the survey's reference for the cell's value (revision 18), which may be a paper or a personal communication |
| survey_basis | for witnesses, compared with the survey's table only: in the survey table (the bound is at most the table's value), implied by the survey's own items (above the table, but given by items and entries of the survey itself), or above the survey table. Blank for rows that are not witnesses and for cells with no survey value |
| license | the license found for the file |
| held | stored here, or linked at its fixed address |
| file, url, sha256 | where the file is and its SHA-256 |
| canonical_hash | SHA-256 of a canonical form of the graph (pynauty certificate), so that two files of the same graph are recognized. Computed for intake rows |
| checks | two checkers, every color; two checkers, symmetry-reduced; two checkers and a cited theorem; one checker, every color; one checker, some colors; not completed; not checked; failed |
| check_scope | what was checked, in the words of the record |
| check_date | the date of the check run here, where recorded |
| check_record | where the logs are |
| label_in_phase | the label the phase record gives, unchanged |
| registration | the registration the row was checked under |
| entered_on | for phase rows, the date the row's record entered the repository (4 November 2026 for phase 1, the commit that added the file for phase 2). For intake rows, the date of the decision, or of receipt while the decision is pending |
| decision | accepted, pending, failed or withdrawn (intake rows), accepted for phase rows that are witnesses |
| record_of | the input the row comes from |
| notes | as in the record |

## cells.csv: one row per cell

`status_4_nov` and `label_phase2` are copied from the closed records. `status_now` says whether the survey's value has
a witness checked here, and by how many checkers. `best_*` describe the witness giving the largest bound. `same_bound`
lists other witnesses giving that bound. `received_not_counted` lists intake rows that are not accepted witnesses, and
`claims` the claims recorded for the cell.

## claims.csv

Claims of a bound with no file checked here, with who made them, where, and why they were not checked.
