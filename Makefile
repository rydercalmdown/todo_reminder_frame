PI_IP_ADDRESS=10.0.2.112
PI_USERNAME=pi


.PHONY: install
install:
	@cd scripts && bash install_pi.sh


.PHONY: copy
copy:
	@echo "For development only"
	@rsync -a $(shell pwd) --exclude env --exclude training $(PI_USERNAME)@$(PI_IP_ADDRESS):/home/$(PI_USERNAME)

.PHONY: shell
shell:
	@echo "For development only"
	@ssh $(PI_USERNAME)@$(PI_IP_ADDRESS)
 
 .PHONY: run
 run:
	@. env/bin/activate && cd src && python app.py
