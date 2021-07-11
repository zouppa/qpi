# QPI
## _Using Holo to better understand Quantum_



Please feel free to watch the demo video :

[![N|Solid](https://github.ibm.com/qpi/qpi/blob/master/misc/video.png)](https://ibm.ent.box.com/embed/s/h69iu0ul42yvz5n9v90q08mekxb6jzr2?sortColumn=date&view=list")

[![N|Solid](https://github.ibm.com/qpi/qpi/blob/master/misc/down.png)](https://ibm.box.com/s/ovs9cy4r1t6r3o0fj63yycz6h8xt23yc)


QPi is an implementation of the Qiskit platform meant to facilitate learning by visualising the Bloch Sphere from different views.

To build a QPi you will need:

- Raspberry Pi 4
- Power Supply for the Raspberry Pi
- Micro SD card with at least 8GB of storage
- 5 inch screen (or bigger) [Like This one](https://es.aliexpress.com/item/4000285089550.html?spm=a2g0s.9042311.0.0.532063c0x1I59N)
- Ready to use holo pyramid (or you can build your own)
- [Optional] Raspberry Pi Battery Hat 
- [Optional] 3D printer 
- ✨Magic ✨

## Features

- Visualise Bloch Sphere in 3 dimention (with 4 views)
- Wifi Access point to allow you to use it in uknown territory (without internet connection)

## Get Started 
You can get QPi in 2 different way

- Download the ready to use image and write it in the SD 
- Follow the Tutorial to install it yourself


## Installation Tutorial 

This tutorial is inspired, and use the knowlodges from : 

- [RasQberry: Quantum Computing is the Coolest Project for Raspberry](https://medium.com/qiskit/rasqberry-quantum-computing-is-the-coolest-project-for-raspberry-pi-3f64bec5a133)
- [Setup your home JupyterHub on a Raspberry Pi](https://towardsdatascience.com/setup-your-home-jupyterhub-on-a-raspberry-pi-7ad32e20eed)


1) Download Raspberry [pi Imager](https://www.raspberrypi.org/software/) and Install Raspberry OS 

2) Update the OS 
```sh
sudo apt update && sudo apt -y upgrade && sudo apt -y dist-upgrade
```

3)Create a swap space of 1 GB
```sh
pi@qpi:~ $ sudo sed -i 's/CONF_SWAPSIZE=100/CONF_SWAPSIZE=1024/' /etc/dphys-swapfile
pi@qpi:~ $ sudo /etc/init.d/dphys-swapfile stop
pi@qpi:~ $ sudo /etc/init.d/dphys-swapfile start
```

```sh

```

## Templates

- [QPi](https://github.ibm.com/qpi/qpi) - QPi 



## Table

| T1 | T2 |
| ------ | ------ |
| 1 | test |
| 2 | test |
| 3  | test |
| 4 | test |

