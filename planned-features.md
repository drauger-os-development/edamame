List of Planned Features
 - Modularity
   - Should make it so that `system-installer` is usable on more distros and is far more flexible.
 - `btrfs` RAID support
   - This will need some limitations, as `/boot/efi` doesn't need to be massive (so letting it have it's own drive is kinda ridiculous), and `btrfs` RAID isn't supported in most UEFI/BIOS. Limit to `/home`?