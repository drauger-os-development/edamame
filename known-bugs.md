List of known bugs
- built in manual partitioner is TERRIBLE
  - This is disabled, in favor of using `gparted`
  - built in auto-partitioner isn't great but it works

- systems with 16+ drives in them cannot have root on the 16th drive during installation
	- This is due to a parsing issue when installing to the correct NVMe drive
	- See Step 12 during GRUB installation in MASTER.sh for what is causing this issue
	- This issue will **NOT** be fixed because
		- This issue pertains to BIOS systems ONLY because GRUB is only used with BIOS
		- Most systems do not have more than 2-3 drives at max
		- What few systems do have enough drives for this issue to arise are either;
			- A server (which Drauger OS should not be running on)
			- A SUPER high-end machine which likely supports UEFI
			
- installer.py only supports default.json for now

- Auto Partitioner is broken on BIOS
	- Have not yet gotten to figuring out how to fix this
