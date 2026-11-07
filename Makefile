# One command for the whole repository. CPU only, no model, no network.
#   make check   every L0 check and every paper regenerated from its stored rows, compared with the committed files
#   make pdf     rebuild the PDFs (needs tectonic)
# Each folder has its own Makefile (the same targets); this one calls them in turn.
DIRS := papers/paper-jepa-world-model papers/paper-register-reproducibility papers/paper-reward-models-stopping-rule papers/paper-vla-edge-inference editlens-paper
export SOURCE_DATE_EPOCH := 1761955200
check:
	@for d in $(DIRS); do echo "== $$d"; $(MAKE) -C $$d l0 paper || exit 1; done
pdf:
	@for d in $(DIRS); do echo "== $$d"; $(MAKE) -C $$d pdf || exit 1; done
.PHONY: check pdf
