# HPLIP 3.25.2 - Enhanced for Python 3.12 and Modern Linux Distributions

This repository contains a modified version of HP Linux Imaging and Printing (HPLIP) 3.25.2, optimized to work with Python 3.12 and modern Linux systems. The modifications address compatibility issues with Python 3.12, recent CUPS versions, and D-Bus dependencies, enabling network printing for HP printers like the LaserJet P1102w and many others.

## Key Modifications
- **Python 3.12 Compatibility**: 
  - Updated `pcard/pcardext/pcardext.c` to use Python 3.x APIs (`PyBytes_*` instead of `PyString_*`, `PyLong_*` instead of `PyInt_*`)
  - Implemented modern module initialization with `PyModuleDef` and `PyInit_pcardext()`
  - Fixed type declarations in `prnt/hpps/pserror.c` to avoid compilation errors
- **Enhanced CUPS Compatibility**: Added missing function declarations to avoid errors with recent CUPS versions
- **D-Bus-free Configuration**: Option to remove D-Bus dependency, avoiding the need for `libdbus-1-dev` and Polkit/systemd interactions
- **Build System Fixes**: Resolved various issues to ensure successful compilation with current development tools

## Compatibility
- **Linux Distributions**: Works on most modern distributions (Ubuntu 24.04/24.10, Fedora, Debian, Arch, etc.)
- **Desktop Environments**: Compatible with X11, Wayland, and other graphical environments
- **Python Versions**: Optimized for Python 3.12, but compatible with Python 3.8+
- **Printers**: Supports most HP printers, including USB and network models

## Dependencies
Install the following packages before building (names for Debian/Ubuntu-based distributions):
```bash
sudo apt update
sudo apt install build-essential libsnmp-dev avahi-utils libcups2-dev python3-dev \
libusb-1.0-0-dev libavahi-client-dev libavahi-common-dev libjpeg-dev libnetsnmp-dev
```

For Fedora/RHEL-based distributions:
```bash
sudo dnf install gcc gcc-c++ make snmp-devel avahi-tools cups-devel python3-devel \
libusb1-devel avahi-devel libjpeg-turbo-devel net-snmp-devel
```

## Build & Installation

### Standard Configuration
```bash
./configure --with-hpppddir=/usr/share/ppd/HP \
  --libdir=/usr/lib64 \
  --prefix=/usr \
  --enable-network-build \
  --disable-scan-build \
  --disable-fax-build \
  --disable-dbus-build \
  --disable-qt4 \
  --disable-qt5 \
  --disable-class-driver \
  --disable-doc-build \
  --disable-policykit \
  --disable-libusb01_build \
  --disable-udev_sysfs_rules \
  --enable-hpcups-install \
  --disable-hpijs-install \
  --disable-foomatic-ppd-install \
  --disable-foomatic-drv-install \
  --disable-cups-ppd-install \
  --enable-cups-drv-install \
  --enable-apparmor_build

make
sudo make install
```

### Additional Options
- For systems without AppArmor, omit `--enable-apparmor_build`
- For 32-bit systems, use `--libdir=/usr/lib` instead of `--libdir=/usr/lib64`
- To enable scanning functionality (requires additional dependencies): omit `--disable-scan-build`

## Graphical Interface Support (Optional)

### For Ubuntu 24.10 with Wayland
If you need graphical tools like `hp-wificonfig` or `hp-toolbox`, you'll need to enable Qt5 support:

1. Install additional dependencies:
```bash
sudo apt install python3-pyqt5 python3-pyqt5.qtsvg python3-dbus.mainloop.pyqt5 qt5-qmake qtbase5-dev qtbase5-dev-tools
```

2. Configure HPLIP with the `--enable-qt5` option:
```bash
./configure --with-hpppddir=/usr/share/ppd/HP \
  --libdir=/usr/lib64 \
  --prefix=/usr \
  --enable-network-build \
  --disable-scan-build \
  --disable-fax-build \
  --disable-dbus-build \
  --disable-qt4 \
  --enable-qt5 \
  --disable-class-driver \
  --disable-doc-build \
  --disable-policykit \
  --disable-libusb01_build \
  --disable-udev_sysfs_rules \
  --enable-hpcups-install \
  --disable-hpijs-install \
  --disable-foomatic-ppd-install \
  --disable-foomatic-drv-install \
  --disable-cups-ppd-install \
  --enable-cups-drv-install \
  --enable-apparmor_build
```

Note: According to HP's official documentation, you must specifically use `--enable-qt5` to enable Qt5 support (simply omitting `--disable-qt5` is not sufficient).

### Available GUI Tools
When Qt5 support is enabled, you'll have access to these additional tools:
- `hp-toolbox`: Comprehensive printer management interface
- `hp-wificonfig`: Configure printer wireless settings
- `hp-devicesettings`: Adjust printer-specific settings
- `hp-diagnose_queues`: Interactive problem-solving tool
- `hp-firmware`: Firmware upgrade utility

### Verifying Installation
After installation, you can verify that everything is correctly set up by running:
```bash
hp-check -r
```

This command performs a comprehensive health check of your HPLIP installation and will:
- Verify all required dependencies are installed
- Check that necessary files are in their correct locations
- Confirm printer discovery services are working
- Report any issues that need to be addressed

You can also check the version of the installed HPLIP package with:
```bash
hp-check -v
```

### Uninstallation and Reinstallation
If you need to uninstall HPLIP and then reinstall it (for example, to change configuration options):

1. **Uninstall the current installation**:
```bash
cd /path/to/hplip-3.25.2
sudo make uninstall
```

2. **Clean up any remaining files**:
```bash
sudo rm -f /etc/hp/hplip.conf
sudo rm -rf /usr/share/hplip
sudo rm -f /etc/xdg/autostart/hplip-systray.desktop
```

3. **Reset build environment**:
```bash
make distclean
```

4. **Reconfigure with new options** (for example, to enable Qt5):
```bash
./configure --with-hpppddir=/usr/share/ppd/HP \
  --libdir=/usr/lib64 \
  --prefix=/usr \
  --enable-network-build \
  --disable-scan-build \
  --disable-fax-build \
  --disable-dbus-build \
  --enable-qt5 \
  --disable-qt4 \
  --disable-class-driver \
  --disable-doc-build \
  --disable-policykit \
  --disable-libusb01_build \
  --disable-udev_sysfs_rules \
  --enable-hpcups-install \
  --disable-hpijs-install \
  --disable-foomatic-ppd-install \
  --disable-foomatic-drv-install \
  --disable-cups-ppd-install \
  --enable-cups-drv-install \
  --enable-apparmor_build
```

5. **Rebuild and reinstall**:
```bash
make
sudo make install
```

6. **Fix permissions if needed**:
If you encounter permission errors during the build process:
```bash
sudo chown -R $(whoami):$(whoami) /path/to/hplip-3.25.2
chmod -R u+w /path/to/hplip-3.25.2
```

### Setting Up Your Printer
After installation, you'll need to configure your printer:

```bash
sudo hp-setup -i
```

This will launch the interactive printer setup utility that will:
1. Discover available HP printers on your network or connected via USB
2. Install the appropriate drivers and PPD files
3. Create print queues in CUPS
4. Configure printer-specific options
5. Print a test page to verify the setup

For network printers, you can specify the IP address directly:
```bash
sudo hp-setup -i 192.168.1.100
```

For more advanced options, see the help:
```bash
hp-setup --help
```

## Troubleshooting
- **Python compilation error**: Ensure you have `python3-dev` (or `python3-devel`) installed matching your Python version
- **CUPS error**: Verify that `cups-devel` (or `libcups2-dev`) is installed
- **Printer detection issues**: Check that `avahi-utils` is installed and Avahi service is running
- **Missing dependencies**: Run `hp-check --fix` to automatically install missing dependencies (requires root)
- **Wayland warning messages**: If you see warnings like `qt.qpa.wayland: Wayland does not support QWindow::requestActivate()` when running GUI tools on Wayland, this is normal and can be safely ignored. It's just informing you that certain window activation functions work differently between Wayland and X11.

## Contributors
- Original HPLIP developed by HP Inc.
- Modified by Daniel Ignacio Fernández ([DannetStudio.com](https://dannetstudio.com/))
  - Python 3.12 compatibility
  - Optional D-Bus dependency removal
  - CUPS compatibility improvements
  - Build system fixes

## License
Same as original HPLIP. See COPYING file for details.