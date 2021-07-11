# QPI
## _Using Holo to better understand Quantum_



Please feel free to watch the demo video :

[![N|Solid](https://github.ibm.com/qpi/qpi/blob/master/misc/video.png)](https://ibm.ent.box.com/embed/s/h69iu0ul42yvz5n9v90q08mekxb6jzr2?sortColumn=date&view=list")

[![N|Solid](https://github.ibm.com/qpi/qpi/blob/master/misc/down.png)](https://ibm.box.com/s/ovs9cy4r1t6r3o0fj63yycz6h8xt23yc)

  <iframe src="https://ibm.ent.box.com/embed/s/h69iu0ul42yvz5n9v90q08mekxb6jzr2?sortColumn=date&view=list" width="800" height="550" frameborder="0" allowfullscreen webkitallowfullscreen msallowfullscreen></iframe> 


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


1. Download Raspberry [pi Imager](https://www.raspberrypi.org/software/) and Install Raspberry OS, and access it via ssh. More information can be found here :

    -[Getting Started](https://projects.raspberrypi.org/en/projects/raspberry-pi-getting-started) 

    -[SSH](https://www.raspberrypi.org/documentation/remote-access/ssh/) 

    -[Set Up a Headless Raspberry Pi](https://www.tomshardware.com/reviews/raspberry-pi-headless-setup-how-to,6028.html)
-
1. Connect using SSH to RPi and Update the OS 
    ```sh
    sudo apt update && sudo apt -y upgrade && sudo apt -y dist-upgrade
    ```
1. Create a swap space of 1 GB
    ```sh
    pi@qpi:~ $ sudo sed -i 's/CONF_SWAPSIZE=100/CONF_SWAPSIZE=1024/' /etc/dphys-swapfile
    pi@qpi:~ $ sudo /etc/init.d/dphys-swapfile stop
    pi@qpi:~ $ sudo /etc/init.d/dphys-swapfile start
    ```
1. Configure the RPI to use Python 3 
    ```sh
    pi@qpi:~ $ sudo rm /usr/bin/python 
    pi@qpi:~ $ sudo ln -s /usr/bin/python3 /usr/bin/python
    ```
1. Install and upgrade the python package manager pip

    ```sh
    pi@qpi:~ $ sudo apt-get install python3-pip 
    pi@qpi:~ $ sudo pip3 install --upgrade pip

    ```

1. Install Node JS and the Proxy 
    ```sh
    pi@qpi:~ $ sudo su
    root@qpi:/home/pi# curl -fsSL https://deb.nodesource.com/setup_14.x | bash -
    root@qpi:/home/pi# apt-get install -y nodejs
    root@qpi:/home/pi# sudo npm install -g configurable-http-proxy
    ```
    go back to pi user 
    ```sh
    root@qpi:/home/pi# exit
    pi@qpi:~ $
    ```
1. Install Jupyter Notebook and JupyterHub
    ```sh
    pi@qpi:~ $ sudo -H pip3 install notebook jupyterhub
    ```
    Generate Jupyterhub Config and move it to root folder
    ```sh
    pi@qpi:~ $ jupyterhub --generate-config 
    ```
    Writing default config to: jupyterhub_config.py
    ```sh
    pi@qpi:~ $ sudo mv jupyterhub_config.py /root
    ```
    Creating Qpi folder 
    ```sh
    pi@qpi:~ $ mkdir qpi
    pi@qpi:~ $ cd qpi/
    ```

1. Manual installation of some dependencies
    ```sh
    pi@qpi:~ $ sudo -H pip install setuptools-rust
    pi@qpi:~ $ curl -o get_rustup.sh -s https://sh.rustup.rs
    pi@qpi:~ $ sudo sh ./get_rustup.sh -y
    pi@qpi:~ $ sudo -H pip install --prefer-binary retworkx
    ```
    Installing libcint, pyscf and cython
    ```sh
    pi@qpi:~ $ sudo apt -y install cmake libatlas-base-dev git
    pi@qpi:~/qpi $ git clone https://github.com/sunqm/libcint.git
    pi@qpi:~/qpi $ mkdir -p libcint/build && cd libcint/build
    pi@qpi:~/qpi/libcint/build $ cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr/local/ ..
    pi@qpi:~/qpi/libcint/build $ sudo make install
    pi@qpi:~/qpi/libcint/build $ sudo -H pip install --prefer-binary pyscf cython
    ```

1. Installation of the latest versions of Qiskit elements
    ```sh
    pi@qpi:~/qpi/libcint/build $ sudo -H pip install --prefer-binary six
    pi@qpi:~/qpi/libcint/build $ sudo -H pip install --prefer-binary 'qiskit[visualization]'
    ```
    Verify qiskit installation 
    ```sh
    pi@qpi:~/qpi/libcint/build $ pip list | grep qiskit
     ```
    
     You should get something like that (version may vary dependin)
    ```sh
    qiskit               0.26.2
    qiskit-aer           0.8.2
    qiskit-aqua          0.9.1
    qiskit-ibmq-provider 0.13.1
    qiskit-ignis         0.6.0
    qiskit-terra         0.17.4
    ```
1. Set up JupyterHub as a system service
    ```sh
    pi@qpi:~/qpi/libcint/build $ sudo nano /lib/systemd/system/jupyterhub.service
    ```
    and paste the following configuration 
    ```sh
    [Unit]
    Description=JupyterHub Service
    After=multi-user.target
    [Service]
    User=root
    ExecStart=/usr/local/bin/jupyterhub --config=/root/jupyterhub_config.py
    Restart=on-failure
    [Install]
    WantedBy=multi-user.target
    ```
    Type ctrl + x, then Y and enter to save the file and exit
     ```sh
    pi@qpi:~/qpi/libcint/build $ sudo systemctl daemon-reload
    pi@qpi:~/qpi/libcint/build $ sudo systemctl start jupyterhub
    pi@qpi:~/qpi/libcint/build $ sudo systemctl enable jupyterhub 
    Created symlink /etc/systemd/system/multi-user.target.wants/jupyterhub.service → /lib/systemd/system/jupyterhub.service.
    ```
    Verify the status of the service
    ```sh
    pi@qpi:~/qpi/libcint/build $ sudo systemctl status jupyterhub.service
     ```
    You should get something like
    ```sh
    ● jupyterhub.service - JupyterHub Service
   Loaded: loaded (/lib/systemd/system/jupyterhub.service; enabled; vendor preset: enabled)
   Active: active (running) since Sun 2021-05-23 15:57:45 CDT; 15s ago
    Main PID: 9578 (jupyterhub)
    Tasks: 11 (limit: 4915)
   CGroup: /system.slice/jupyterhub.service
           ├─9578 /usr/bin/python3 /usr/local/bin/jupyterhub --config=/root/jupyterhub_config.py
           └─9583 node /usr/bin/configurable-http-proxy --ip --port 8000 --api-ip 127.0.0.1 --api-port 8001 --error-target http://127.0.0.1:8081/hub/error
    May 23 15:57:48 qpi jupyterhub[9578]: 15:57:48.767 [ConfigProxy] info: Proxy API at http://127.0.0.1:8001/api/routes
    May 23 15:57:49 qpi jupyterhub[9578]: 15:57:49.319 [ConfigProxy] info: 200 GET /api/routes
    May 23 15:57:49 qpi jupyterhub[9578]: [I 2021-05-23 15:57:49.319 JupyterHub app:2778] Hub API listening on http://127.0.0.1:8081/hub/
    May 23 15:57:49 qpi jupyterhub[9578]: 15:57:49.325 [ConfigProxy] info: 200 GET /api/routes
    May 23 15:57:49 qpi jupyterhub[9578]: [I 2021-05-23 15:57:49.326 JupyterHub proxy:347] Checking routes
    May 23 15:57:49 qpi jupyterhub[9578]: [I 2021-05-23 15:57:49.327 JupyterHub proxy:432] Adding route for Hub: / => http://127.0.0.1:8081
    May 23 15:57:49 qpi jupyterhub[9578]: 15:57:49.333 [ConfigProxy] info: Adding route / -> http://127.0.0.1:8081
    May 23 15:57:49 qpi jupyterhub[9578]: 15:57:49.335 [ConfigProxy] info: Route added / -> http://127.0.0.1:8081
    May 23 15:57:49 qpi jupyterhub[9578]: 15:57:49.337 [ConfigProxy] info: 201 POST /api/routes/
    May 23 15:57:49 qpi jupyterhub[9578]: [I 2021-05-23 15:57:49.338 JupyterHub app:2853] JupyterHub is now running at http://:8000
    ```
    Open a web browser and point to : http://[Your Pi hostname or IP adress]:8000/ 
    
    Then login using pi user and password 

    ![N|Solid](https://github.ibm.com/qpi/qpi/blob/master/misc/login.png)

    You can go ahead and test that Qiskit is runing on JupyterHub, by creating a new Python 3 file 






1. 
    ```sh

    ```
1. 
    ```sh

    ```
1. 
    ```sh

    ```
1. 
    ```sh

    ```
1. 
    ```sh

    ```
1. 
    ```sh

    ```
1. 
    ```sh

    ```
1. 
    ```sh

    ```
1. 
    ```sh

    ```
1. 
    ```sh

    ```
1. 
    ```sh

    ```
1. 
    ```sh

    ```
1. 
    ```sh

    ```
1. 
    ```sh

    ```
1. 
    ```sh

    ```
1. 
    ```sh

    ```
1. 
    ```sh

    ```
1. 
    ```sh

    ```
1. 
    ```sh

    ```
1. 
    ```sh

    ```
1. 
    ```sh

    ```
1. 
    ```sh

    ```
1. 
    ```sh

    ```
1. 
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

