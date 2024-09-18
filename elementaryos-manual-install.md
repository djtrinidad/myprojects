Elementary OS - manual install when installer fails due to squashfs

I'm starting to feel like this is related to EFI BIOSs, I've tried
several workaround when partitioning the drive, none have worked.
When the installer is extracting files, it fails at 65%.

This is a working document, my last attempt yielded me an installed
Elementary OS that would constantly run the installer when I logged 
in, even after selecting Pantheon as the lightdm session.

So here goes attempt 10, after getting a different system working, now
I can reference install logs.

Boot USB installer to Live Demo Mode (works nicely in Demo mode)

** Partitioning the root drive
Open GParted and partition the drive.
I had some existing, and didn't care to wipe the drive so I deleted them all, and saved.
Click Device, Create Partition Table; Select gpt; Apply
Click Partition, New; Size 512MB, File system: fat32; Add (I don't add names or labels at this point)
Create another for the root filesystem, ext4 is default. 
Create one more 2000MB, linux-swap
Click Green Check Mark, and apply changes

** Format the partitions
My drives are /dev/sda
/dev/sda1 EFI
/dev/sda2 /
/dev/sda3 swap

$ lsblk
$ sudo mkfs.fat -F32 /dev/sda1
$ sudo mkfs.ext4 /dev/sda2
$ sudo mkswap /dev/sda3

** Install Elementary OS on root partition
$ sudo mount /dev/sda2 /mnt
$ sudo mkdir /mnt/cdrom
$ sudo mkdir -p /mnt/boot/efi
$ sudo unsquashfs -f -d /mnt /cdrom/casper/filesystem.squashfs
So far so good
$ for i in /cdrom /dev /dev/pts /proc /sys /run; do sudo mount --bind $i /mnt$i; done
$ sudo chroot /mnt
# update-locale --reset LANG=en_US.UTF-8
# cp /cdrom/casper/vmlinuz /mnt/

tried to add cdrom per adding apt-cdrom
but all packages were already installed
grub-common grub2-common grub-pc etc..

*** Remove packages
remove this long list of packages, apparently no longer needed after install
apt-get purge -y btrfs-progs casper cifs-utils discover discover-data distinst dmraid elementary-live expect f2fs-tools fatresize fina
lrd gettext gparted gparted-common io.elementary.installer io.elementary.installer-session keyutils kpartx kpartx-boot libatkmm-1.6-1v5:amd64 libca
iromm-1.0-1v5:amd64 libdiscover2 libdistinst libdmraid1.0.0.rc16:amd64 libglibmm-2.4-1v5:amd64 libgtkmm-3.0-1v5:amd64 libinih1:amd64 libnss-mymachi
nes:amd64 libpangomm-1.4-1v5:amd64 libsigc++-2.0-0v5:amd64 localechooser-data mokutil reiserfsprogs systemd-container tcl-expect:amd64 user-setup w
ingpanel xfsprogs

# localectl set-x11-keymap us
# /usr/bin/env -i SYSTEMCTL_SKIP_REDIRECT=_ openvt -- sh /etc/initrd.d/console-setup.sh reload
# ln -s /etc/console-setup/cached_UTF-8_del.kmap.gz /etc/console-setup/cached.kmap.gz

There's a line about deleteing update-initramfs and restoring from the .bak, but the .bak did 
not exist, hence I had to re-install.  Booting won't work right now, lets manual boot from grub 
and get user created

Rebooting

# exit
$ for i in /dev /dev/pts /proc /sys /run; do sudo umount /mnt$i; done
$ reboot

Boot from USB drive
grub> ls
find the partition
grub> ls (hd2,gpt2)/
grub> set root=(hd2,gpt2)
grub> linux /boot/vmlinuz root=/dev/sda2 ro quiet splash
grub> initrd /boot/initrd.gz
grub> boot

back to demo mode

ALMOST there I hope

I totally forgot to create the /etc/fstab BUT it booted!!

Boot to demo mode
From Terminal
mount the /dev/sda2 at /mnt again
mount binds and 
chroot

Trying to fix grub
# cd /cdrom
# cp -R EFI /boot/efi/

** Create user
# adduser <username>
# usermod -aG sudo <username>
# systemctl set-default graphical.target

trying grub once more, else boot manually again

got grub menu but no entrys
did a manual boot

looking for rulevel 5 and lightdm login, got it!

logged in

got the welcome! greeter

