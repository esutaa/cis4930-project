install-dependencies:
	@if ! command -v pip3 >/dev/null 2>&1; then \
		echo "pip3 not installed, installing...";\
		sudo apt-get install python3-pip --yes;\
	fi
	sudo -H pip3 install pygame\
