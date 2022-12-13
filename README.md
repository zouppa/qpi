# QPI
## _Using Holo to better understand Quantum_



Please feel free to watch the [demo video](https://youtu.be/BiD5429jMis) and the [assembly video](https://youtu.be/lVraOgavMDs)

You can download the ready to use [disk image](https://zouppa.com/qpi/Qpi_1.0_C.zip)

<!--[![N|Solid](https://github.com/zouppa/qpi/blob/main/resources/down.png)](https://github.com/zouppa/qpi/blob/main/resources/down.png)-->


QPi is an implementation of the Qiskit platform meant to facilitate learning by visualizing the Qsphere from different views.

To build a QPi you will need:

- Raspberry Pi 4
- Power Supply for the Raspberry Pi
- Micro SD card with at least 8GB of storage (We recommend 16 GB)
- 5 inch screen (or bigger) [Like This one](https://aliexpress.com/item/4000285089550.html)
- Ready to use holo pyramid (or you can build your own) [Like This one](https://aliexpress.com/item/4000081968339.html)
- [Optional] Raspberry Pi Battery Hat : in case you want to use the QPi anywhere without the need to connect it to a power source
- ✨Magic ✨

## Features

- Visualize QSphere in 3 dimensions (with 4 views)
- Wi-Fi Access point to allow you to use it in unknown territory (without internet connection)

## Get Started 
You can get QPi in 2 different ways

- Follow the Tutorial to install it yourself
- Contact us to provide you with the ready to use image and write it in the SD	


## Installation Tutorial 

In this tutorial we will
- [Install and configure the Raspberry Pi Operating System and Python ](#install-raspberry-pi-os)
- [Install Jupyter Hub](#install-jupyter-hub)
- [Install Qiskit and feh](#install-qiskit-and-feh)
- [Set up JupyterHub as a system service](#set-up-jupyterhub-as-a-system-service)
- [Create the auto start script](#create-the-auto-start-script)
- [<span style="color:red"> *Optional* </span>  Configure the Raspberry Pi as an Access point](#optional-configure-the-raspberry-pi-as-an-access-point)




This tutorial is inspired, and use the knowledge from : 

- [RasQberry: Quantum Computing is the Coolest Project for Raspberry](https://medium.com/qiskit/rasqberry-quantum-computing-is-the-coolest-project-for-raspberry-pi-3f64bec5a133)
- [Setup your home JupyterHub on a Raspberry Pi](https://towardsdatascience.com/setup-your-home-jupyterhub-on-a-raspberry-pi-7ad32e20eed)
- [Install Qiskit](#install-qiskit)

### install Raspberry Pi OS

1. Download Raspberry [pi Imager](https://www.raspberrypi.org/software/), Install Raspberry OS, and access it via ssh. More information can be found here :

    -[Getting Started](https://projects.raspberrypi.org/en/projects/raspberry-pi-getting-started) 

    -[SSH](https://www.raspberrypi.com/documentation/computers/remote-access.html) 

    -[Set Up a Headless Raspberry Pi](https://www.raspberrypi.com/documentation/computers/configuration.html#setting-up-a-headless-raspberry-pi)

1. Connect using SSH to RPi and Update the OS. This is the standard procedure to make sure that you are up to date
    ```sh
    sudo apt update && sudo apt -y upgrade && sudo apt -y dist-upgrade
    ```
1. Create a swap space of 1 GB. 

As some of the compilation and installation tasks require more than the 512 MB of RAM that are available on smaller Raspberry Pi models, we increase the swap space to 1 GB. The size of the configured swap space can be checked with free -m.

    ```sh
    pi@qpi:~ $ sudo sed -i 's/CONF_SWAPSIZE=100/CONF_SWAPSIZE=1024/' /etc/dphys-swapfile
    pi@qpi:~ $ sudo /etc/init.d/dphys-swapfile stop
    pi@qpi:~ $ sudo /etc/init.d/dphys-swapfile start
    ```

1. <span style="color:red"> *Optional* </span>  Installing and configuring the screen

 Some screen have very specific resolution and features (like touch screen, controlling the brightness etc.) and need to have specific drivers to enable those features.
    Please refer to the tutorial related to your screen manufacturer. In our case we are using a 5-inch HDMI capacitive screen. 
    ```sh
    pi@qpi:~ $ git clone https://github.com/goodtft/LCD-show.git
    pi@qpi:~ $ cd LCD-show/
    pi@qpi:~ $ sudo ./LCD5-show
    ```
1. Disable the screen save 

When using the QPi usually we interact with it remotely using the Jupyter Notebook and feh to display the QSphere. As a result, after a certain time of using the QPi, the screen may go dark or start using the screensaver. To avoid that, we recommend disabling the screensaver and screen blanking.

    Please find here different ways to [disable the screensaver](https://www.raspberrypi.com/documentation/computers/configuration.html#configuring-screen-blanking) 


1. Configure the RPI to use Python 3 

Qiskit supports Python 3.7 or later

    ```sh
    pi@qpi:~ $ sudo rm /usr/bin/python 
    pi@qpi:~ $ sudo ln -s /usr/bin/python3 /usr/bin/python
    ```
1. Install and upgrade the python package manager pip

Pip is the package installer / manager for Python. We will need to install and update needed software like : notebook, jupyterHub, setuptools-rust, pyscf, cython ect. You can identify all the dependencies that pip support us to install by searching "pip3 install" in this tutorial.

    ```sh
    pi@qpi:~ $ sudo apt-get install python3-pip 
    pi@qpi:~ $ sudo pip3 install --upgrade pip

    ```

### Install Jupyter Hub

1. Install Node JS and the Proxy 

To be able to run Jupyter hub, we need a proxy that routes the user requests to the hub and the notebook servers. In this tutorial, we will use [configurable-http-proxy](https://www.npmjs.com/package/configurable-http-proxy) that run on [NodeJS](https://nodejs.org/)

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

In the QPi project, we use the main screen of the device to display a projection of a QSphere. As a result, the only way to interact with the QPi (a part of having a second screen) will be remotely. Since Qiskit is based on python, and most of it is tutorials uses Jupyter notebook, we wanted this project to have a familiar interface and allow anyone to easily start experimenting with Quantum computing and Qiskit. Having this set of tools will allow the user to access a jupyter notebook in his personal device (laptop/smartphone), create a circuit and watch the QPi display it as a hologram.  

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

### Install Qiskit and feh

The main idea of the QPi project is to be abe to use your personal device to connect to the QPi. Open a Jupyter notebook remotely, and allow the user to create any Quantum circuit and visualize its QSphere as a hologram projection. To be able to do that, we have created a python library that when used will create an image composed by 4 different views of the Qsphere and save it with a specific name in a specific folder. We then use feh a lightweight image viewer to display this image with a specified refresh rate (in this tutorial we use 1 second). To have a good user experience, we recommend running feh at startup.

1. Manual installation of some [dependencies for Qiskit](https://medium.com/qiskit/rasqberry-quantum-computing-is-the-coolest-project-for-raspberry-pi-3f64bec5a133#acc1) 
    ```sh
    pi@qpi:~ $ sudo -H pip install setuptools-rust
    pi@qpi:~ $ curl -o get_rustup.sh -s https://sh.rustup.rs
    pi@qpi:~ $ sudo sh ./get_rustup.sh -y
    pi@qpi:~ $ sudo -H pip install --prefer-binary retworkx
    pi@qpi:~ $ sudo -H pip install --prefer-binary cvxpy
    ```
    Installing libcint, pyscf and cython
    ```sh
    pi@qpi:~ $ sudo apt -y install cmake libatlas-base-dev git feh unclutter
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
    
     You should get something like that (version may vary)
    ```sh
    qiskit               0.26.2
    qiskit-aer           0.8.2
    qiskit-aqua          0.9.1
    qiskit-ibmq-provider 0.13.1
    qiskit-ignis         0.6.0
    qiskit-terra         0.17.4
    ```
1. ### Set up JupyterHub as a system service

Setting up JupyterHub as a service will allow us to start it automatically

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
    Open a web browser and point to: http://[Your Pi hostname or IP address]:8000/ 
    
    Then login using pi user and password 

    ![N|Solid](https://github.com/zouppa/qpi/blob/main/resources/login.png)

    You can go ahead and test that Qiskit is running on JupyterHub, by creating a new Python 3 file, and run the following 

    ```python
    pip list | grep qiskit
    ```
    you should get 

    ![N|Solid](https://github.com/zouppa/qpi/blob/main/resources/pqiskit.png)

1. ### Create the auto start script 

This script will auto start feh when the QPi start. for more details about that, please refer to [Install Qiskit and feh](#install-qiskit-and-feh)

    create the folder 

    ```sh
    pi@qpi:~ $ mkdir /home/pi/.config/autostart
    ```
    <span style="color:red"> *important* </span> : 
    Choose a png file that you want your raspberry pi to display after starting up (like the chandelier in the video) rename it to and copy it to start.png and upload it to the Raspberry pi filesystem under the folder /home/pi/.config/autostart

    You can upload the file using any [SFTP client](https://www.raspberrypi.org/documentation/remote-access/ssh/sftp.md) like [filezilla](https://www.youtube.com/watch?v=EBFGMcWftLA) or [SCP](https://www.raspberrypi.org/documentation/remote-access/ssh/scp.md) 


    ```sh
    pi@qpi:~ $ mkdir /home/pi/.config/autostart
    pi@qpi:~ $ nano /home/pi/.config/autostart/start.sh
    ```
    and paste the following 
    ```sh
    export DISPLAY=:0 
    mkdir -p /home/pi/qpi/tmp 
    cp /home/pi/.config/autostart/start.png /home/pi/qpi/figures/qpi.png 
    feh --scale-down --auto-zoom --fullscreen --reload 1 /home/pi/qpi/figures/qpi.png 
    unclutter -idle 0
    ```
    Type ctrl + x, then Y and enter to save the file and exit

    Then run the following command to make the script executable 
    ```sh
    pi@qpi:~ $ chmod +x /home/pi/.config/autostart/start.sh
    ```
    and make it run at start up by executing 
    ```sh
    pi@qpi:~ $ nano /home/pi/.config/autostart/start.desktop
    ```
    and pasting 
    ```sh
    [Desktop Entry]
    Type=Application
    Name=Start
    Exec=/home/pi/.config/autostart/start.sh
    ```
    Type ctrl + x, then Y and enter to save the file and exit

### <span style="color:red"> *Optional* </span>  Configure the Raspberry Pi as an Access point 

    In case you are connected to your RPi through ethernet and want to enable it as an access point to be able to use QPi even when without internet.

    <span style="color:red"> *Important* </span>  If your raspberry pi is connected to your network via Wi-Fi, you will need an additional USB Wi-Fi interface, otherwise you may lose connection to your raspberry through your LAN.

    We used [RaspAP](https://raspap.com)

    In case you did not already set up a Wi-Fi country, please run 
    ```sh
    sudo raspi-config
    ```
    And navigate to 1 System Options -> S1 Wireless LAN and you will prompt to select a country. After that just cancel 

    Installing RaspAP

    ```sh
    pi@qpi:~ $ curl -sL https://install.raspap.com | bash
    ```
    Answer Y to all the question

    Go to http://[Your Pi hostname or IP address]

    The default username and password are
    - Username : admin 
    - Password : secret

    Use the web interface to change them and save

   ![N|Solid](https://github.com/zouppa/qpi/blob/main/resources/rapap.png)

    To change the port of RaspAp run  

    ```sh
    pi@qpi:~ $ sudo nano /etc/lighttpd/lighttpd.conf
    ```
    and locate 
    ```sh
    server.port                 = 80
    ```
    Change it to 
    ```sh
    server.port                 = 8080
    ```
    Type ctrl + x, then Y and enter to save the file and exit
    
    then reboot 
    ```sh
    pi@qpi:~ $ sudo reboot
    ```
    Verify that the changes to the port and credential worked by accessing 
    http://[Your Pi hostname or IP address]:8080

    You can also change the SSID of you raspberry Pi, for more details please refer to [RaspAP](https://raspap.com) 

1. Installing QPi Library

    Download the whl file using the commands below. In case you are not able to use wget, please download the file [QPi_lib-0.2.7-py3-none-any.whl](https://github.com/zouppa/qpi/tree/main/QPi_Library/QPi_lib-0.2.7-py3-none-any.whl) and upload it to the QPi under the path /home/pi/qpi

    ```sh
    cd /home/pi/qpi
    wget https://github.com/zouppa/qpi/tree/main/QPi_Library/QPi_lib-0.2.7-py3-none-any.whl
    ```
    Install the library 

    ```sh
    pip install QPi_lib-0.2.7-py3-none-any.whl
    ```

1. Running QPi

    Open a web browser and point to : http://[Your Pi hostname or IP address]:8000/ 
    
    Then login using pi user and password 

    ![N|Solid](https://github.com/zouppa/qpi/blob/main/resources/login.png)

    You can go ahead and create a new Python 3 file, and import the needed library 

    ```python
    import qpi_lib
    import warnings
    from qpi_lib import qsphere_funcs
    from qiskit import QuantumCircuit
    warnings.filterwarnings('ignore')
    ```

    Create a circuit and draw it 


    ```python
    qc = QuantumCircuit(3)
    # Apply H-gate to the first:
    qc.h(1)
    qc.x(0)

    # Apply a CNOT:
    qc.cx(0,1)
    qc.cx(0,2)

    qc.z(0)
    qc.z(1)

    qc.draw(output='mpl')
    ```
    To visualize any circuit on the QPi you can run 

    ```python
    qsphere_funcs.plot_qsphere_full(qc)
    ```
# Please feel free to check Introduction to Qpi so you can build your own and Quantum Operations with Qpi for a guide in your firsts circuits!

- [Introduction to Qpi](https://github.com/zouppa/qpi/blob/main/Introduction_to_QPI.ipynb)
- [Quantum Operations with Qpi](https://github.com/zouppa/qpi/blob/main/Quantum_Operations_with_QPi.ipynb) 

# Please feel free to reach out to the team:

- [Zouppa : Mohamed Zouhaier Ramadhane](https://www.linkedin.com/in/zouppa)

- [Catalina Albornoz Anzola](https://www.linkedin.com/in/catalinaalbornoz)

- [El Serch : Sergio Inurreta](https://www.linkedin.com/in/el-serch/)

- [Ana Vialeny Mota Gómez](https://www.linkedin.com/in/vialeny)

- [Jaime Jesús Ambrosio Mallqui](https://www.linkedin.com/in/jaime-ambrosio)
