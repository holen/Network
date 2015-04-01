################################################################################
#                             V A R I A B L E S
#
# Files in the export directory on which the firewall script does not depend
IGNOREFILES =  firewall% Makefile% trace% %~

# Remote Firewall system
HOST = 192.168.7.222
#PORT = 222
PORT = 22

# Save some typing
LITEDIR = /var/lib/shorewall-lite



################################################################################
#                                T A R G E T S
#
all: firewall

# Only generate the capabilities file if it doesn't already exist
capabilities: 
	ssh -v -p $(PORT) root@$(HOST) "/sbin/shorewall-lite show -f capabilities > $(LITEDIR)/capabilities"
	scp -v -P $(PORT) root@$(HOST):$(LITEDIR)/capabilities .

# Compile the firewall script. Using the 'wildcard' function causes "*" to be expanded so that
# 'filter-out' will be presented with the list of files in this directory rather than "*"
firewall: $(filter-out $(IGNOREFILES) capabilities , $(wildcard *) ) capabilities
	shorewall compile -e . firewall

# Only reload on demand.
install: firewall
	scp -P $(PORT) firewall firewall.conf root@$(HOST):$(LITEDIR)
	ssh -v -p $(PORT) root@$(HOST) "/sbin/shorewall-lite restart"

# Save running configuration
save:
	ssh -v -p $(PORT) root@$(HOST) "/sbin/shorewall-lite save"

# Remove generated files
clean: 
	rm -f capabilities firewall firewall.conf reload
