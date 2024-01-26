List of known bugs
- built in manual partitioner is TERRIBLE
  - This needs a rewrite, to stop relying on Gparted

- systems with 16+ drives in them cannot have root on the 16th drive during installation
	- This is due to a parsing issue when installing to the correct NVMe drive
	- See Step 12 during GRUB installation in master.py for what is causing this issue
	- This issue will **NOT** be fixed because
		- This issue pertains to BIOS systems ONLY because GRUB is only used with BIOS
		- Most systems do not have more than 2-3 drives at max
		- What few systems do have enough drives for this issue to arise are either;
			- A server (which Drauger OS should not be running on)
			- A SUPER high-end machine which likely supports UEFI
			
- Wi-Fi passwords stored in a KDE Wallet Keychain do not get copied to a newly installed system
	- **WORK AROUND** - When adding a Wi-Fi password to a live system, have the Wi-Fi network be added for the entire system. This will ensure the network configuration will be carried over
	- **FIX** - Disable the KDE Wallet Subsystem before building your ISO. This will force all Wi-Fi networks to be added for the entire system.
