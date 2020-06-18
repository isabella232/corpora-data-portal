SHELL=/bin/bash -o pipefail
tests:=$(wildcard tests/test*.py)

.PHONY: new-deploy
new-deploy:
	$(MAKE) deploy -C chalice

.PHONY: deploy
deploy:
	$(MAKE) retrieve-deployed -C chalice
	$(MAKE) deploy -C chalice

.PHONY: destroy
destroy:
	$(MAKE) destroy -C chalice

.PHONY: clean
clean:
	$(MAKE) clean -C chalice

.PHONY: package
package:
	$(MAKE) package -C chalice

.PHONY: local-server
local-server:
	$(MAKE)  local-server -C chalice