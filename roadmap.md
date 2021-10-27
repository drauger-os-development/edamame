# todo

- [ ] Implement pylint, unit/doc tests and type hinting
- [ ] Document how to conduct tests
- [ ] Include testing in the development page as a "to do" checklist before creating a pull request

# system-installer

## si-utlities
| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| eprint |     |     |     |

## auto_partitioner.py
| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| MAIN |     |     |     |
| gb_to_bytes |     |     |     |
| bytes_to_gb |     |     |     |
| size_of_part |    |     |     |
| get_min_root_size |     |     |     |
| check_disk_state |     |     |     |
| mkfs |     |     |     |
| mkfs_fat |     |     |     |
| make_efi |     |     |     |
| sectors_to_size |     |     |     |
| make_root |     |     |     |
| make_home |     |     |     |
| generate_return_data |     |     |     |
| make_root_boot |     |     |     |
| make_part_boot |     |     |     |
| clobber_disk |     |     |     |
| delete_part |     |     |     |
| partition |     |     |     |
| make_raid_array |     |     |     |

## check_internet.py

| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| ping |     |     |     |
| has_internet |     |     |     |

## check_kernel_versions.py

| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| get_file_version |     |     |     |
| get_installed_version |     |     |     |
| check_kernel_versions |    |     |     |

## chroot.py

| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| mount |     |     |     |
| unmount |     |     |     |
| arch_chroot |    |     |     |
| de_chroot |     |     |     |

## common.py

| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| unique |     |     |     |
| eprint |     |     |     |
| real_number |    |     |     |

## engine.py

| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| MAIN |     |     |     |

## installer.py

| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| mount |     |     |     |
| update |     |     |     |
| install |    |     |     |

## progress.py

| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| MAIN |     |     |     |

## success.py

| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| MAIN |     |     |     |

# Modules

## __init__.py

| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| MAIN |     |     |     |

## auto_login_set.py

| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| eprint |     |     |     |
| auto_login_set |     |     |     |

## install_extras.py

| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| eprint |     |     |     |
| install_extras |     |     |     |

## install_updates.py

| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| eprint |     |     |     |
| update_system |     |     |     |

## make_swap.py

| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| eprint |     |     |     |
| make_swap |     |     |     |

## make_user.py

| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| eprint |     |     |     |
| fix_home |     |     |     |
| make_user |    |     |     |

## master.py

| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| eprint |     |     |     |
| update |     |     |     |
| MainInstallation.init |    |     |     |
| MainInstallation.time_set |     |     |     |
| MainInstallation.locale_set |     |     |     |
| MainInstallation.set_networking |     |     |     |
| MainInstallation.make_user | | | |
| MainInstallation.mk_swap |     |     |     |
| MainInstallation.apt |     |     |     |
| MainInstallation.set_passwd |     |     |     |
| MainInstallation.lightdm.config |     |     |     |
| MainInstallaion.set_keyboard |     |     |     |
| MainInstallation.remove_launcher |     |     |     |
| set_plymouth_theme |     |     |     |
| install_kernel |     |     |     |
| install_bootloader |     |     |     |
| install_grub |     |     |     |
| install_systemd_boot |     |     |     |
| setup_lowlevel |     |     |     |
| check_systemd_boot |     |     |     |
| check_for_laptop |     |     |     |
| handle_laptops |     |     |     |
| install |     |     |     |

## purge.py

| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| purge_package |     |     |     |
| autoremove |     |     |     |

## set_locale.py

| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| eprint |     |     |     |
| set_locale |     |     |     |
| _set_locale |    |     |     |

## set_time.py

| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| eprint |     |     |     |
| link |     |     |     |
| set_time |    |     |     |

## set_wallpaper.py

| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| eprint |     |     |     |
| set_wallpaper |     |     |     |


## verify_install.py

| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| eprint |     |     |     |
| verify |     |     |     |

# OEM

## __init__.py
| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| MAIN |     |     |     |

## pre_install.py
| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| eprint |     |     |     |
| has_special_charater | | | |
| Main.init |     |     |     |
| Main.set_default_margins |     |     |     |
| Main.auto_partition |    |     |     |
| Main.define_array |     |     |     |
| Main.assign_raid_disk_1 |     |     |     |
| Main.assign_raid_disk_2 |     |     |     |
| Main.assign_raid_disk_3 |     |     |     |
| Main.assign_raid_disk_4 |     |     |     |
| Main.change_raid_type |     |     |     |
| Main.confirm_raid_array |     |     |     |
| Main.cement_raid_array |     |     |     |
| Main.auto_home_setup |     |     |     |
| Main.auto_home_setup2 |     |     |     |
| Main.select_home_part |     |     |     |
| Main.set_root_part |     |     |     |
| Main.confirm_auto_part |     |     |     |
| Main.complete |     |     |     |
| Main.exit |     |     |     |
| Main._exit |     |     |     |
| Main.clear_window |     |     |     |
| Main.return_data |     |     |     |
| show_main |     |     |     |

# OEM Post Install

## __init__.py
| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| MAIN |     |     |     |

## UI.py
| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| eprint |     |     |     |
| has_special_character |     |     |     |
| Main.init | | | |
| Main.set_default_margins |    |     |     |
| Main.reset |     |     |     |
| Main.user |     |     |     |
| Main.on_user_completed |     |     |     |
| Main.locale |     |     |     |
| Main.update_subregion |     |     |     |
| Main.on_locale_completed |     |     |     |
| Main.keyboard |     |     |     |
| Main.varient_narrower |     |     |     |
| Main.on_keyboard_completed |     |     |     |
| Main.complete |     |     |     |
| Main.clear_window |     |     |     |
| Main.exit |     |     |     |
| set_passwd |     |     |     |
| show_main |     |     |     |
| configure_locale |     |     |     |
| configure_keyboard |     |     |     |
| monitor_procs |     |     |     |
| make_kbd_names |     |     |     |

# OEM Post Install configure

## __init__.py
| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| MAIN |     |     |     |

## auto_login_set.py
| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| eprint |     |     |     |
| auto_login_set |     |     |     |

## keyboard.py
| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| configure |     |     |     |

## set_locale.py
| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| eprint |     |     |     |
| set_locale |     |     |     |
| _set_locale |    |     |     |

## set_time.py
| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| eprint |     |     |     |
| link |     |     |     |
| set_time |    |     |     |

# UI

## __init__.py
| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| MAIN |     |     |     |

## confirm.py
| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| eprint |     |     |     |
| Main.init |     |     |     |
| Main.onnextclicked |    |     |     |
| Main.set_default_margins |     |     |     |
| Main.exit |     |     |     |
| Main.return_install |     |     |     |
| show_confirm |     |     |     |

## error.py
| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| Main.init |     |     |     |
| Main.main_menu |     |     |     |
| show_error |    |     |     |

## main.py
| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| has_special_character |     |     |     |
| Main.init |    |     |     |
| Main.set_default_margins |     |     |     |
| Main.quick_install_warning |     |     |     |
| Main.reset |     |     |     |
| Main.oem_startup |     |     |     |
| Main.select_config |     |     |     |
| Main.add_filters |     |     |     |
| Main.main_menu |     |     |     |
| Main.user |     |     |     |
| Main.onnext2clicked |     |     |     |
| Main.partitioning |     |     |     |
| Main.auto_partition |     |     |     |
| Main.define_array |     |     |     |
| Main.assign_raid_disk_1 |     |     |     |
| Main.assign_raid_disk_2 |     |     |     |
| Main.assign_raid_disk_3 |     |     |     |
| Main.assign_raid_disk_4 |     |     |     |
| Main.change_raid_type |     |     |     |
| Main.confirm_raid_array |     |     |     |
| Main.cement_raid_array |     |     |     |
| Main.make_space |     |     |     |
| Main.make_space_parts |     |     |     |
| Main.confirm_remove_part |     |     |     |
| Main.remove_part |     |     |     |
| Main.auto_home_setup |     |     |     |
| Main.auto_home_setup2 |     |     |     |
| Main.select_home_part |     |     |     |
| Main.set_root_part |     |     |     |
| Main.confirm_auto_part |     |     |     |
| Main.input_part |     |     |     |
| Main.onnext4clicked |     |     |     |
| Main.opengparted |     |     |     |
| Main.options |     |     |     |
| Main.options_next |     |     |     |
| Main.locale |     |     |     |
| Main.update_subregion |     |     |     |
| Main.on_locale_completed |     |     |     |
| Main.keyboard |     |     |     |
| Main.varent_narrower |     |     |     |
| Main.on_keyboard_completed |     |     |     |
| Main.done |     |     |     |
| Main.complete |     |     |     |
| Main.exit |     |     |     |
| Main._exit |     |     |     |
| Main.clear_window |     |     |     |
| Main.return_data |     |     |     |
| show_main |     |     |     |
| make_kbd_names |     |     |     |

## progress.py
| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| Main.init |     |     |     |
| Main.set_default_margins |     |     |     |
| Main.read_file |    |     |     |
| Main.pulse |     |     |     |
| Worker.init |     |     |     |
| Worker.do_startup |     |     |     |
| Worker.do_activate |     |     |     |
| show_progress |     |     |     |
| handle_sig_term |     |     |     |

## report.py
| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| MAIN |     |     |     |
| Main.init |     |     |     |
| Main.clear_window |    |     |     |
| Main.set_default_margin |     |     |     |
| Main.cpu_toggle |     |     |     |
| Main.cpu_explanation |     |     |     |
| Main.gpu_toggle |     |     |     |
| Main.gpu_explanation |     |     |     |
| Main.ram_toggle |     |     |     |
| Main.ram_explanation |     |     |     |
| Main.disk_toggle |     |     |     |
| Main.disk_explanation |     |     |     |
| Main.log_toggle |     |     |     |
| Main.log_explanation |     |     |     |
| Main.exit |     |     |     |
| Main.message_handler |     |     |     |
| Main.send_report |     |     |     |
| Main.preview_message |     |     |     |
| Main.generate_message |     |     |     |
| Main.message_accept |     |     |     |
| Main.toggle_ui |     |     |     |
| Main.main |     |     |     |
| cpu_info |     |     |     |
| RAM_info |     |     |     |
| disk_info |     |     |     |
| get_info |     |     |     |
| send_to |     |     |     |

## success.py
| Function Name | Pylint | Unit/Doc Tests | Type Hinting |
| --- | --- | --- | --- |
| MAIN |     |     |     |
| Main.init |     |     |     |
| Main.set_default_margins |     |     |     |
| Main.main_menu |    |     |     |
| Main.onadvclicked |     |     |     |
| Main.ondeletewarn |     |     |     |
| Main.delete_install |     |     |     |
| Main.add_ppa |     |     |     |
| Main.add_ppa_backend |     |     |     |
| Main.exit |     |     |     |
| Main.clear_window |     |     |     |
| Main.dump_settings_dialog |     |     |     |
| Main.dump_settings_file_dialog |     |     |     |
| dump_settings |     |     |     |
| adv_dump_settings |     |     |     |
| unique |     |     |     |
| show_success |     |     |     |
| reboot |     |     |     |
| poweroff |     |     |     |
