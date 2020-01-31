List of known bugs
- built in manual partitioner is TERRIBLE
  - built in auto-partitioner isn't great but it works
- No slideshow or installation segment progress bar, or some other form of progress indicator
- Consistent false positives
- `chroot` is not opening when user requests access to it post-install
- systems with 16+ drives in them cannot have root on the 16th drive during installation
	- This is due to a parsing issue when installing to the correct NVMe drive
	- See Step 12 during GRUB installation in MASTER.sh for what is causing this issue
- installer.sh only supports default.config for now