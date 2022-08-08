# QPI
## _Using Holo to better understand Quantum_



Please feel free to watch the [demo video](https://youtu.be/BiD5429jMis) and the [assembly video](https://youtu.be/lVraOgavMDs)

<!--[![N|Solid](https://github.com/zouppa/qpi/blob/main/resources/down.png)](https://github.com/zouppa/qpi/blob/main/resources/down.png)-->


QPi is an implementation of the Qiskit platform meant to facilitate learning by visualising the Qsphere from different views.

To build a QPi you will need:

- Raspberry Pi 4
- Power Supply for the Raspberry Pi
- Micro SD card with at least 8GB of storage
- 5 inch screen (or bigger) [Like This one](https://es.aliexpress.com/item/4000285089550.html?spm=a2g0s.9042311.0.0.532063c0x1I59N)
- Ready to use holo pyramid (or you can build your own) [Like This one](https://es.aliexpress.com/item/4000081968339.html?spm=a2g0s.9042311.0.0.274263c0gowY0M)
- [Optional] Raspberry Pi Battery Hat 
- [Optional] 3D printer 
- ✨Magic ✨

## Features

- Visualise QSphere in 3 dimentions (with 4 views)
- Wifi Access point to allow you to use it in uknown territory (without internet connection)

## Get Started 
You can get QPi in 2 different way

- Follow the Tutorial to install it yourself
- Contact us to provide you with the ready to use image and write it in the SD	


## Installation Tutorial 

This tutorial is inspired, and use the knowledge from : 

- [RasQberry: Quantum Computing is the Coolest Project for Raspberry](https://medium.com/qiskit/rasqberry-quantum-computing-is-the-coolest-project-for-raspberry-pi-3f64bec5a133)
- [Setup your home JupyterHub on a Raspberry Pi](https://towardsdatascience.com/setup-your-home-jupyterhub-on-a-raspberry-pi-7ad32e20eed)


1. Download Raspberry [pi Imager](https://www.raspberrypi.org/software/) and Install Raspberry OS, and access it via ssh. More information can be found here :

    -[Getting Started](https://projects.raspberrypi.org/en/projects/raspberry-pi-getting-started) 

    -[SSH](https://www.raspberrypi.org/documentation/remote-access/ssh/) 

    -[Set Up a Headless Raspberry Pi](https://www.tomshardware.com/reviews/raspberry-pi-headless-setup-how-to,6028.html)

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

1. <span style="color:red"> *Optional* </span>  Installing and configuring the screen

    Please refer to the tutorial related to your screen manufucturer. In our case we are using a 5 inch HDMI capacitive screen. 
    ```sh
    pi@qpi:~ $ git clone https://github.com/goodtft/LCD-show.git
    pi@qpi:~ $ cd LCD-show/
    pi@qpi:~ $ sudo ./LCD5-show
    ```
1. Disable the screen save 
    Please find here different ways to [disable the screensave](https://www.raspberrypi.org/documentation/configuration/screensaver.md) 


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

    ![N|Solid](https://github.com/zouppa/qpi/blob/main/resources/login.png)

    You can go ahead and test that Qiskit is runing on JupyterHub, by creating a new Python 3 file , and run the following 

    ```python
    pip list | grep qiskit
    ```
    you should get 

    ![N|Solid](https://github.com/zouppa/qpi/blob/main/resources/pqiskit.png)

1. Create the auto start script 

    create the folder 

    ```sh
    pi@qpi:~ $ mkdir /home/pi/.config/autostart
    ```
    <span style="color:red"> *importent* </span> : 
    Choose a png file that you want your raspberry pi to display after starting up (like the chandelier in the video) rename it to and copy it to start.png and upload it to the Raspberry pi filesysten under the folder /home/pi/.config/autostart

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

    Then run the following commad to make the script executable 
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

1. <span style="color:red"> *Optional* </span>  Configure the Raspberry Pi as an Access point 
    In case you are connected to your RPi through ethernet and want to enable it as an access point to be able to use QPi even when without internet.

    <span style="color:red"> *Importent* </span>  If your raspberry pi is connected to your network via wifi, you will need an aditional usb wifi interface, otherwise you may loose connection to your raspberry through your LAN.

    We used [RaspAP](https://raspap.com)

    In case you did not already set up a WiFi country, please run 
    ```sh
    sudo raspi-config
    ```
    And navigate to 1 System Options -> S1 Wireless LAN and you will prompt to select a country. After that just cancel 

    Installing RaspAP

    ```sh
    pi@qpi:~ $ curl -sL https://install.raspap.com | bash
    ```
    Answer Y to all the question

    Go to http://[Your Pi hostname or IP adress]

    The defualt username and password are
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
    http://[Your Pi hostname or IP adress]:8080

    You can also change the SSID of you raspberry Pi , for more details please refer to [RaspAP](https://raspap.com) 

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

1. Runing QPi

    Open a web browser and point to : http://[Your Pi hostname or IP adress]:8000/ 
    
    Then login using pi user and password 

    ![N|Solid](https://github.com/zouppa/qpi/blob/main/resources/login.png)

    You can go ahead and creayte a new Python 3 file, and import the needed library 

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
    To visualise any circuit on the QPi you can run 

    ```python
    qsphere_funcs.plot_qsphere_full(qc)
    ```
# Please feel free to check Intoduction to Qpi so you can build your own and Quantum Operations with Qpi for a guide in your firsts circuits!

- [Intoduction to Qpi](https://github.com/zouppa/qpi/blob/main/Introduction_to_QPI.ipynb)
- [Quantum Operations with Qpi](https://github.com/zouppa/qpi/blob/main/Quantum_Operations_with_QPi.ipynb) 

# Please feel free to reach out to the team:

-[Zouppa : Mohamed Zouhaier Ramadhane](https://www.linkedin.com/in/zouppa)

-[Catalina Albornoz Anzola](https://www.linkedin.com/in/catalinaalbornoz)

-[El Serch : Sergio Inurreta](https://www.linkedin.com/in/el-serch/)

-[Ana Vialeny Mota Gómez](https://www.linkedin.com/in/vialeny)

-[Jaime Jesús Ambrosio Mallqui](https://www.linkedin.com/in/jaime-ambrosio)
