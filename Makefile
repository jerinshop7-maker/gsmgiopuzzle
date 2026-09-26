.DEFAULT_GOAL := help

PYTHON ?= python3
PYTEST ?= $(PYTHON) -m pytest

PUZZLE_URL ?= https://gsmg.io/puzzle
PUZZLE_IMAGE ?= raw/github/puzzlehunt-gsmgio-5btc-puzzle/working/puzzle.png
GITHUB_REPO ?= puzzlehunt/gsmgio-5btc-puzzle

.PHONY: help all offline check test test-all test-repository verify crypto \
	 reproduce transcribe analyze salphaseion bitcoin grid inventory hash \
	 intake intake-web intake-github gf256-probe gf256-matrix hint161-probe \
	 front-prefix-probe esrever-binary-probe full-password-synthesis-probe \
	 prime-basic-position-probe lead-triangle-matrix-probe \
	 lead-triangle-tail-selector-probe

help:
	@awk 'BEGIN {FS = ":.*##"; print "GSMG forensic workspace targets:\n"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "  %-18s %s\n", $$1, $$2} END {print "\nNetwork access is limited to intake-web and intake-github."}' $(MAKEFILE_LIST)

all: check ## Run the local verification suite.

offline: verify crypto reproduce transcribe analyze salphaseion bitcoin grid test ## Run all local, read-only checks.

check: verify crypto grid test-repository ## Run the fast integrity, crypto, image, and repository checks.

test: test-all ## Run the complete Python test suite.

test-all: ## Run every test file; useful for auditing the whole worktree.
	$(PYTEST)

test-repository: ## Run the tests belonging to this forensic repository.
	$(PYTEST) tests/test_repository.py

verify: ## Verify hashes recorded in the raw-artifact manifest.
	$(PYTHON) -m scripts.verify_repository

crypto: ## Run known-answer cryptographic controls.
	$(PYTHON) -m scripts.crypto_vectors

reproduce: ## Reproduce the established public puzzle claims from local captures.
	$(PYTHON) -m scripts.reproduce_public_claims

transcribe: ## Transcribe the captured SalPhaseIon page.
	$(PYTHON) -m scripts.transcribe_salphaseion

analyze: ## Analyze SalPhaseIon regions and derived structure.
	$(PYTHON) -m scripts.analyze_salphaseion

salphaseion: transcribe analyze ## Run both SalPhaseIon local analysis steps.

bitcoin: ## Run offline Bitcoin/WIF/address verification controls.
	$(PYTHON) -m scripts.bitcoin_verify

grid: ## Extract and verify the canonical 14x14 puzzle grid.
	$(PYTHON) -m scripts.extract_grid $(PUZZLE_IMAGE)

hash: ## Append hashes for newly captured raw artifacts to the manifest.
	$(PYTHON) -m scripts.hash_artifacts

inventory: hash ## Refresh the human-readable raw-artifact inventory.
	$(PYTHON) -m scripts.build_inventory

intake: intake-web ## Backward-compatible alias for the puzzle web capture.

intake-web: ## Capture the puzzle page (network access; never run implicitly).
	$(PYTHON) -m scripts.intake_web "$(PUZZLE_URL)" --label puzzle

intake-github: ## Capture a GitHub repository and issues (network access; REPO=owner/name).
	$(PYTHON) -m scripts.intake_github "$(GITHUB_REPO)"

gf256-probe: ## Reproduce the finite GF(256) interpolation scan.
	$(PYTHON) experiments/next_stage/gf256_full_scan.py

gf256-matrix: ## Test clue-backed 4x16 matrix readings of GF(256) level 3.
	$(PYTHON) experiments/next_stage/gf256_matrix_probe.py

hint161-probe: ## Test the recovered 161-token 7x23 hint matrix.
	$(PYTHON) experiments/next_stage/hint161_matrix_probe.py

front-prefix-probe: ## Test the author-recorded ``giveit in front`` rule.
	$(PYTHON) experiments/next_stage/front_prefix_probe.py

esrever-binary-probe: ## Apply the known whole-bitstream reversal to Bifid objects.
	$(PYTHON) experiments/next_stage/esrever_binary_probe.py

full-password-synthesis-probe: ## Test source-order 16-item and seven-token synthesis forms.
	$(PYTHON) experiments/next_stage/full_password_synthesis_probe.py

prime-basic-position-probe: ## Test literal 2,3,5,7 source-position reinsertion forms.
	$(PYTHON) experiments/next_stage/prime_basic_position_probe.py

lead-triangle-matrix-probe: ## Test 1+...+13 triangular LEAD91 matrix-sum forms.
	$(PYTHON) experiments/next_stage/lead_triangle_matrix_probe.py

lead-triangle-tail-selector-probe: ## Use triangular LEAD sums as direct TAIL indices.
	$(PYTHON) experiments/next_stage/lead_triangle_tail_selector_probe.py
